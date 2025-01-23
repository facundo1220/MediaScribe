interface chatBubbleInt {
  message: string;
  isUser: boolean;
}

function ChatBubble({ message, isUser }: chatBubbleInt) {
  const isTool = message.includes("Calling tool");

  if (!isTool) {
    return (
      <div
        className={`${isUser ? "bg-orange-600" : "bg-gray-50"} rounded-lg p-2`}
      >
        {<p className={`${isUser ? "text-white" : "text-black"}`}>{message}</p>}
      </div>
    );
  } else {
    const regex = /<([^>]+)>/;
    const match = message.match(regex);

    if (match) {
      const value = `${match[1]}?${
        import.meta.env.VITE_AZURE_STORAGE_SAS_TOKEN
      }`;

      return (
        <div
          className={`${
            isUser ? "bg-orange-600" : "bg-gray-100"
          } rounded-lg p-2 flex flex-col gap-2`}
        >
          <div>{message.split("<")[0]}</div>
          <div>
            <img className="h-32 w-32 rounded-full" src={value} alt="" />
          </div>
        </div>
      );
    }
  }
}

export default ChatBubble;
