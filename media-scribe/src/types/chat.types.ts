export interface DataChat {
  id: string;
  knowledge: string;
}

export interface TableChat {
  data: DataChat[];
}

export type ChatMessages = [string, string];
