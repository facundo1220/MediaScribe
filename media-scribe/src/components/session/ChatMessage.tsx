import ChatBubble from "./ChatBubble";

interface ChatMessageProps {
  messages: [string, string];
}

function ChatMessage({ messages }: ChatMessageProps) {
  return (
    <div className="flex flex-col  gap-3">
      <div className="flex justify-end">
        <ChatBubble isUser={true} message={messages[0]} />
      </div>
      <div className="">
        <ChatBubble isUser={false} message={messages[1]} />
      </div>
    </div>
  );
}

export default ChatMessage;
