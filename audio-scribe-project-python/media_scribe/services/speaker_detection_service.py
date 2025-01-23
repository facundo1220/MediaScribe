import os
import cv2
from tempfile import NamedTemporaryFile, mkdtemp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import VideoFileClip, ImageSequenceClip
import json
import av
import torch
import numpy as np
from transformers import AutoProcessor, AutoModel
import re

os.environ["TOKENIZERS_PARALLELISM"] = "false"


class Speaker_Detector:
    def __init__(self, file, intervals):
        self.intervals, self.speakers = self._extract_intervals(intervals)

        self.file_path = self._create_temporary_file(file)

    def _extract_intervals(self, intervals):
        try:
            input_string = intervals.replace("'", '"')

            json_data = json.loads(input_string)

            intervals_data = []
            unique_speakers = set()

            for interval in json_data:
                intervals_data.append(
                    (interval["start"], interval["end"], interval["speaker"])
                )
                unique_speakers.add(interval["speaker"])

            unique_speakers_list = list(unique_speakers)

            return intervals_data, unique_speakers_list

        except Exception as e:
            print(f"Error extracting intervals {e}")

    def _extract_longest_interval(self, intervals):
        longest_intervals = {}

        for start, end, speaker in intervals:
            if speaker not in longest_intervals:
                longest_intervals[speaker] = (0.0, 0.0, "")

            current_start, current_end, _ = longest_intervals[speaker]
            current_length = current_end - current_start
            interval_length = end - start

            if interval_length > current_length:
                longest_intervals[speaker] = (start, end, speaker)

        return list(longest_intervals.values())

    def _create_temporary_file(self, file):
        with NamedTemporaryFile(suffix=".mov", delete=False) as tmp:
            tmp.write(file.file.read())
        return tmp.name

    def extract_frames(self, video_path, intervals, output_fps=20):
        longest_interval = self._extract_longest_interval(intervals)

        frames_data = []

        for start, end, speaker in longest_interval:

            video = VideoFileClip(video_path).subclip(start, end).set_fps(output_fps)
            frames = video.iter_frames()

            for frame_num, frame in enumerate(frames):
                frames_data.append((speaker, frame_num, frame))

            video.close()

        return frames_data

    def detect_faces(self, frames_data):
        face_data = {}
        for speaker, frame_num, frame in frames_data:
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.3, minNeighbors=10, minSize=(50, 50)
            )

            if len(faces) > 0:
                for i in range(0, len(faces)):
                    x, y, w, h = faces[i]
                    top, right, bottom, left = y, x + w, y + h, x
                    face_data[(f"{i}_possible_{speaker}", frame_num)] = (
                        frame,
                        (top, right, bottom, left),
                    )

        return face_data

    def evaluate_quality(self, face_data):
        scores = {}
        for key, (frame, face_location) in face_data.items():
            top, right, bottom, left = face_location

            face = frame[top:bottom, left:right]

            gray_face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            clarity = cv2.Laplacian(gray_face, cv2.CV_64F).var()

            size = (bottom - top) * (right - left)

            scores[key] = clarity * size
        return scores

    def save_best_photos(self, scores, face_data, output_folder=""):
        best_photos = {}
        for key, score in scores.items():
            speaker = key[0]
            if speaker not in best_photos or scores[best_photos[speaker]] < score:
                best_photos[speaker] = key

        # if not os.path.exists(output_folder):
        #    os.makedirs(output_folder)

        temp_dir = mkdtemp()

        export_photos = []

        for speaker, key in best_photos.items():
            frame, face_location = face_data[key]
            top, right, bottom, left = face_location
            face = frame[top:bottom, left:right]
            face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            # output_path = os.path.join(output_folder, f"{speaker}.jpg")
            # cv2.imwrite(output_path, face_rgb)

            with NamedTemporaryFile(
                dir=temp_dir,
                delete=False,
                mode="w",
                suffix=".jpg",
                prefix=f"{speaker}_",
            ) as temp_file:
                cv2.imwrite(temp_file.name, face_rgb)

            export_photos.append(temp_file.name)

        return export_photos

    def _save_faces_video(
        self, face_data, output_folder="", frame_rate=20, size=(128, 128)
    ):
        speaker_frames = {}

        for (speaker, _), (frame, face_location) in sorted(face_data.items()):

            if speaker not in speaker_frames:
                speaker_frames[speaker] = []

            top, right, bottom, left = face_location
            face = frame[top:bottom, left:right]
            face_resized = cv2.resize(face, size)
            speaker_frames[speaker].append(face_resized)

        speakers_videos = []

        temp_dir = mkdtemp()

        for speaker, frames in speaker_frames.items():
            # if not os.path.exists(output_folder):
            #    os.makedirs(output_folder)

            # output_video_path = os.path.join(output_folder, f"{speaker}.mp4")
            clip = ImageSequenceClip(frames, fps=frame_rate)
            # clip.write_videofile(output_video_path, codec="libx264")

            with NamedTemporaryFile(
                dir=temp_dir,
                delete=False,
                mode="w",
                suffix=".mp4",
                prefix=f"{speaker}_",
            ) as temp_file:
                clip.write_videofile(temp_file.name, codec="libx264")

            speakers_videos.append(temp_file.name)

        return speakers_videos

    def _read_video_pyav(self, container, indices):
        frames = []
        container.seek(0)
        start_index = indices[0]
        end_index = indices[-1]
        for i, frame in enumerate(container.decode(video=0)):
            if i > end_index:
                break
            if i >= start_index and i in indices:
                frames.append(frame)
        return np.stack([x.to_ndarray(format="rgb24") for x in frames])

    def _sample_frame_indices(self, clip_len, frame_sample_rate, seg_len):
        converted_len = int(clip_len * frame_sample_rate)
        end_idx = np.random.randint(converted_len, seg_len)
        start_idx = end_idx - converted_len
        indices = np.linspace(start_idx, end_idx, num=clip_len)
        indices = np.clip(indices, start_idx, end_idx - 1).astype(np.int64)
        return indices

    def _extract_speaker(self, videos_for_speaker):
        best_video = None
        highest_prob = 0.0

        for video_path in videos_for_speaker:
            container = av.open(video_path)

            indices = self._sample_frame_indices(
                clip_len=8,
                frame_sample_rate=1,
                seg_len=container.streams.video[0].frames,
            )
            video = self._read_video_pyav(container, indices)

            processor = AutoProcessor.from_pretrained("microsoft/xclip-base-patch32")
            model = AutoModel.from_pretrained("microsoft/xclip-base-patch32")

            inputs = processor(
                text=[
                    "Person talking",
                    "Silence",
                    "No conversation",
                    "No speech",
                    "No dialogue",
                    "Speechlessness",
                    "Quietude",
                    "No verbal activity",
                ],
                videos=list(video),
                return_tensors="pt",
                padding=True,
            )

            with torch.no_grad():
                outputs = model(**inputs)

            logits_per_video = outputs.logits_per_video
            prob = logits_per_video.softmax(dim=1)
            prob_value = (prob[0][0]).item()

            print(f"prob {prob_value} - video {video_path}")

            if prob_value > highest_prob:
                highest_prob = prob_value
                best_video = video_path

        return best_video

    def filter_face_data(self, face_data, real_speakers):
        filtered_face_data = {
            key: value for key, value in face_data.items() if key[0] in real_speakers
        }
        return filtered_face_data

    def validate_who_is_talking(self, face_data):
        try:
            speakers_videos = self._save_faces_video(face_data)

            real_speakers = []

            for speaker in self.speakers:

                videos_for_speaker = [
                    texto for texto in speakers_videos if speaker in texto
                ]

                print(f"best video for speaker:{speaker}")

                extract_speaker_video = self._extract_speaker(videos_for_speaker)
                filename_with_extension = os.path.basename(extract_speaker_video)
                filename = os.path.splitext(filename_with_extension)[0]

                match = re.match(r"^(.*?_\d+)_", filename)
                desired_part = match.group(1)
                real_speakers.append(desired_part)

            real_face_data = self.filter_face_data(face_data, real_speakers)

            return real_face_data

        except Exception as e:
            print(e)

        finally:
            for video in speakers_videos:
                os.remove(video)

    def process_video(self):
        try:
            frames_data = self.extract_frames(self.file_path, self.intervals)
            face_data = self.detect_faces(frames_data)
            face_data_validated = self.validate_who_is_talking(face_data)
            scores = self.evaluate_quality(face_data_validated)
            best_photos = self.save_best_photos(scores, face_data_validated)

            return best_photos

        except Exception as e:
            print(e)

        finally:
            os.remove(self.file_path)
