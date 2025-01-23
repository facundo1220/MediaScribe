export interface DataItem {
  id: string;
  knowledge_name: string;
  type: string;
  created_at: string;
  ready: string;
}

export interface TableData {
  data: DataItem[];
}
