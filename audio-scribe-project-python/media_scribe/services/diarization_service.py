import whisper
from pyannote.audio import Pipeline
import os
from fastapi import UploadFile
import torch
from tempfile import NamedTemporaryFile
from moviepy.editor import VideoFileClip


class Diarizator:
    def __init__(self, file: UploadFile):
        try:
            device = torch.device("cpu")
            self.model = whisper.load_model("base", device=device)
            self.pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=os.getenv("HUGGING_FACE_TOKEN"),
            )
            self.file_path = self._create_temporary_file(file)
        except Exception as e:
            print(f"Error init Diarizator: {e}")

    def _create_temporary_file(self, file):
        with NamedTemporaryFile(suffix=".mov", delete=False) as tmp:
            tmp.write(file.file.read())
        return tmp.name

    def _is_overlapping(self, start1, end1, start2, end2):
        return start1 < end2 and start2 < end1

    def _video_to_audio(self, video_path):
        with NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
            temp_audio_filename = temp_audio_file.name

        video = VideoFileClip(video_path)

        audio = video.audio
        audio.write_audiofile(temp_audio_filename)

        video.close()
        return temp_audio_filename

    def extract_text_data(self):
        try:
            result = self.model.transcribe(self.file_path)

            return result

        except Exception as e:
            print(f"Error en extract_text_data: {e}")
            return None

    def extract_diarization_data(self):
        try:
            audio_path = self._video_to_audio(self.file_path)
            diarization = self.pipeline(audio_path)
            diarization_lab = diarization.to_lab().split("\n")
            diarization_lab = diarization_lab[:-1]

            diarization_data = []

            for diar_value in diarization_lab:
                diar_split = diar_value.split(" ")
                start = diar_split[0]
                end = diar_split[1]
                speaker = diar_split[2]

                diarization_data.append(
                    {"start": float(start), "end": float(end), "speaker": speaker}
                )

            return diarization_data
        except Exception as e:
            print(f"Error in extract_diarization: {e}")
            return None

        finally:
            os.remove(audio_path)

    def extract_diarization_result(self):
        try:
            whisper_data = self.extract_text_data()["segments"]
            diarization_data = self.extract_diarization_data()

            merged_data = []

            for whisper_segment in whisper_data:
                whisper_start = whisper_segment["start"]
                whisper_end = whisper_segment["end"]
                whisper_text = whisper_segment["text"]

                for diar_segment in diarization_data:
                    diar_start = diar_segment["start"]
                    diar_end = diar_segment["end"]
                    speaker = diar_segment["speaker"]

                    if self._is_overlapping(
                        whisper_start, whisper_end, diar_start, diar_end
                    ):
                        merged_data.append(
                            {
                                "speaker": speaker,
                                "start": whisper_start,
                                "end": whisper_end,
                                "text": whisper_text.replace("'", ""),
                            }
                        )
            return merged_data

        except Exception as e:
            print(e)

        finally:
            os.remove(self.file_path)

    def format_diarization_text(self, diarization_result):
        try:
            formatted_text = ""
            for entry in diarization_result:
                formatted_text += f"Speaker: {entry['speaker']} - Text: {entry['text']} (start: {entry['start']} - end: {entry['end']})\n"
            return formatted_text
        except Exception as e:
            print(f"Error formating diarization text {e}")
