import { useParams } from "react-router-dom";
import ChatTyping from "../components/session/ChatTyping";
import ChatMessage from "../components/session/ChatMessage";
import { getSession, open_session } from "../api/Chats";
import { useEffect, useState, useRef } from "react";
import { ChatMessages } from "../types/chat.types";
import { sendMessage } from "../api/Chats";
import { sendMessageInt } from "../api/Chats";
import Loading from "../components/loading/Loading";

function Chat() {
  const { sessionId } = useParams();

  const [messages, setmessages] = useState<ChatMessages[] | null>(null);
  const [loading, setloading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setloading(true);
        const open = await open_session({ sessionId });

        const sessionMessages = await getSession({ sessionId });

        setmessages(sessionMessages);
      } catch (error) {
        console.log(error);
      } finally {
        setloading(false);
      }
    };

    fetchData();
  }, [sessionId]);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleSendMessage = async ({ question, sessionId }: sendMessageInt) => {
    try {
      const answer = await sendMessage({ question, sessionId });

      const new_question: ChatMessages = [question || "", answer];

      setmessages((prevMessages) =>
        prevMessages ? [...prevMessages, new_question] : [new_question]
      );
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <>
      {loading ? (
        <Loading />
      ) : (
        <div className="h-full flex flex-col">
          <div className="overflow-y-auto flex flex-col gap-3 flex-1 px-2">
            {messages?.map((item, index) => (
              <ChatMessage key={index} messages={item} />
            ))}
            <div ref={messagesEndRef} />
          </div>

          <div className="h-20 grid items-center">
            <ChatTyping onsend={handleSendMessage} sessionId={sessionId} />
          </div>
        </div>
      )}
    </>
  );
}

export default Chat;
