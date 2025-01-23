import { IoIosSend } from "react-icons/io";
import { useState } from "react";
import { sendMessageInt } from "../../api/Chats";

interface propsTyping {
  onsend: ({ question, sessionId }: sendMessageInt) => Promise<void>;
  sessionId: string | undefined;
}

function ChatTyping({ onsend, sessionId }: propsTyping) {
  const [question, setquestion] = useState<string | null>(null);
  const [loading, setLoading] = useState(false); // State for loading

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setquestion(event.target.value);
  };

  const handleSend = async () => {
    if (!question) return; 

    setLoading(true); 
    const currentQuestion = question;
    setquestion(""); 

    try {
      await onsend({ question: currentQuestion, sessionId });
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false); 
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex px-2 gap-2">
      <input
        type="text"
        placeholder="Message"
        value={question ? question : ""}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        disabled={loading} 
        className="flex-1 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-gray-500 focus:border-gray-500 block w-full p-2.5"
      />
      <button
        className="bg-orange-600 rounded-lg hover:bg-orange-800 w-10 flex items-center justify-center"
        onClick={handleSend}
        disabled={loading} 
      >
        <IoIosSend size={20} color="white" />
      </button>
    </div>
  );
}

export default ChatTyping;
