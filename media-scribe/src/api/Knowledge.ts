import React from "react";
import { DataItem, TableData } from "../types/table.types";

interface createKnowledgeInterface {
  event: React.FormEvent<HTMLFormElement>;
  file: File | null;
}

interface indexKnowledgeInt {
  media_path: string | null;
}

export const createKnowledge = async ({
  event,
  file,
}: createKnowledgeInterface) => {
  event.preventDefault();

  try {
    if (!file) {
      console.log("no file error");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
      "http://127.0.0.1:8000/diarization/save_diarization_azure",
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const intervals = await response.json();

    formData.append("intervals", intervals.message);

    const responseDetection = await fetch(
      "http://127.0.0.1:8000/speaker/save_detection",
      {
        method: "POST",
        body: formData,
      }
    );

    const Detection = await responseDetection.json();

    console.log(Detection);
  } catch (error) {
    alert(error);
  }
};

export const indexKnowledge = async ({ media_path }: indexKnowledgeInt) => {
  if (!media_path) {
    console.log("no question or session error");
    return;
  }

  const jsonData = { media_path: media_path };

  const response = await fetch(
    "http://127.0.0.1:8001/langchain_rag/index_knowledge",
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
};

export const getAllKnoweldges = async (): Promise<TableData | null> => {
  try {
    const response = await fetch(
      "http://127.0.0.1:8000/diarization/get_all_knoledges"
    );

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const responseJson = await response.json();

    const allData = responseJson.message.replace(/'/g, '"');

    const jsondata = JSON.parse(allData);

    const data: DataItem[] = jsondata.map((item: DataItem) => ({
      id: item.id,
      knowledge_name: item.knowledge_name,
      type: item.type,
      created_at: new Date(item.created_at),
      ready: item.ready,
    }));

    const tableData: TableData = {
      data,
    };

    return tableData;
  } catch (error) {
    console.log(error);
    return null;
  }
};
