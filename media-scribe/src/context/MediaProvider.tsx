import { MediaContext } from "./MediaContext";
import { getAllKnoweldges } from "../api/Knowledge";
import { getAllSessions } from "../api/Chats";

import { TableData } from "../types/table.types";
import { TableChat } from "../types/chat.types";

import { useState, useEffect } from "react";
interface props {
  children: JSX.Element | JSX.Element[];
}

export const MediaProvider = ({ children }: props) => {
  const [tableData, settableData] = useState<TableData | null>(null);
  const [chatData, setchatData] = useState<TableChat | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getAllKnoweldges();

        const chats = await getAllSessions();

        settableData(data);
        setchatData(chats);
      } catch (error) {
        console.log(error);
      }
    };

    fetchData();
  }, []);

  return (
    <MediaContext.Provider value={{ chats: chatData, knowledges: tableData }}>
      {children}
    </MediaContext.Provider>
  );
};
