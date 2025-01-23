import { useContext } from "react";
import { MediaContext } from "../context/MediaContext";

export const useMedia = () => {
  const { chats, knowledges } = useContext(MediaContext);

  return {
    chats,
    knowledges,
  };
};
