import { Params } from "react-router-dom";
import { DataChat, TableChat, ChatMessages } from "../types/chat.types";

interface createSessionInterface {
  event: React.FormEvent<HTMLFormElement>;
  knowledge: string | null;
}

export interface sendMessageInt {
  question: string | null;
  sessionId: string | undefined;
}

export interface open_session_int {
  sessionId: string | undefined;
}

interface getSession {
  sessionId: string | undefined;
}

export const createSession = async ({
  event,
  knowledge,
}: createSessionInterface) => {
  try {
    event.preventDefault();

    if (!knowledge) {
      console.log("no file error");
      return;
    }

    const formData = new FormData();
    formData.append("media_path", knowledge);

    const response = await fetch(
      "http://127.0.0.1:8001/langchain_rag/new_session",
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const responseJson = await response.json();

    const SessionId = responseJson.message;

    return SessionId;
  } catch (error) {
    alert(error);
  }
};

//http://127.0.0.1:8001/langchain_rag/open_session

export const open_session = async ({ sessionId }: open_session_int) => {
  try {
    if (!sessionId) {
      console.log("no session error");
      return;
    }

    const jsonData = { session_id: sessionId };

    const response = await fetch(
      "http://127.0.0.1:8001/langchain_rag/open_session",
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData),
      }
    );

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const responseJson = await response.json();

    const message = responseJson.message;

    return message;
  } catch (error) {
    alert(error);
  }
};

export const getSession = async ({ sessionId }: getSession) => {
  try {
    const response = await fetch(
      `http://127.0.0.1:8001/langchain_rag/get_session_messages/${sessionId}`
    );

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const responseJson = await response.json();

    const allData = responseJson.message.replace(/'/g, '"');

    const jsondata = JSON.parse(allData);

    const data: ChatMessages[] = jsondata.map((item: ChatMessages) => item);

    return data;
  } catch (error) {
    console.log(error);
    return null;
  }
};

export const sendMessage = async ({ question, sessionId }: sendMessageInt) => {
  try {
    if (!question || !sessionId) {
      console.log("no question or session error");
      return;
    }

    const jsonData = { session_id: sessionId, question: question };

    const response = await fetch(
      "http://127.0.0.1:8001/langchain_rag/send_prompt_user_langchain",
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(jsonData),
      }
    );

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const responseJson = await response.json();

    const message = responseJson.message;

    return message;
  } catch (error) {
    alert(error);
  }
};

export const getAllSessions = async () => {
  try {
    const response = await fetch(
      "http://127.0.0.1:8001/langchain_rag/get_all_session"
    );

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const responseJson = await response.json();

    const allData = responseJson.message.replace(/'/g, '"');

    const jsondata = JSON.parse(allData);

    const data: DataChat[] = jsondata.map((item: DataChat) => ({
      id: item.id,
      knowledge: item.knowledge,
    }));

    const tableData: TableChat = {
      data,
    };

    return tableData;
  } catch (error) {
    console.log(error);
    return null;
  }
};
