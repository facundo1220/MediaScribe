import { useMedia } from "../hooks/useMedia";

function Sessions() {
  const { knowledges, chats } = useMedia();

  console.log(knowledges);
  console.log(chats);

  return (
    <div className="flex flex-col items-center justify-center p-4">
      <p className="text-4xl font-bold text-center pb-14 flex gap-2">
        Welcome to <p className="text-orange-600">MediaScribe</p>
      </p>
      <p className="mt-4 text-lg text-center">
        MediaScribe is an advanced chatbot application designed to answer your
        questions based on video or audio files. Our chatbot leverages
        state-of-the-art technology to:
      </p>
      <ul className="mt-2 list-disc list-inside">
        <li>
          Analyze and extract meaningful insights from video and audio content.
        </li>
        <li>Identify and display speakers within videos.</li>
        <li>
          Provide time-lapse information to help you navigate through the
          content efficiently.
        </li>
      </ul>
      <p className="mt-4 text-lg text-center  pb-14">
        Whether you need detailed information or quick answers, MediaScribe is
        here to assist you by making the most out of your media files.
      </p>

      <img
        className=""
        src="https://img.freepik.com/premium-vector/video-streaming-concept-with-people-scene-flat-cartoon-style-man-films-process_198565-6805.jpg"
        alt=""
      />
    </div>
  );
}

export default Sessions;
