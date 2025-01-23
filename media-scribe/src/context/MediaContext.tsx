import { createContext } from "react";
import { TableData } from "../types/table.types";
import { TableChat } from "../types/chat.types";

export type MediaContextProps = {
  chats: TableChat | null;
  knowledges: TableData | null;
};

export const MediaContext = createContext<MediaContextProps>(
  {} as MediaContextProps
);
