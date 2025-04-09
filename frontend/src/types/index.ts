export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ProjectFormData {
  projectName: string;     // 工事名（セルI9）
  location: string;        // 施工場所（セルI11）
  period: string;          // 工期（セルI13）
  workerCount: number;     // 作業者数（セルQ15）
}

export interface LLMResponse {
  content: string;
  vbaCode?: string;
}
