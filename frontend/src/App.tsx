import { useState, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { Message, ProjectFormData, LLMResponse } from '@/types';
import { ChatMessage } from '@/components/ChatMessage';
import { ChatInput } from '@/components/ChatInput';
import { FileUpload } from '@/components/FileUpload';
import { ProjectForm } from '@/components/ProjectForm';
import { VBACodeDisplay } from '@/components/VBACodeDisplay';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Separator } from '@/components/ui/separator';
import { MessageSquare, Code } from 'lucide-react';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('chat');
  const [excelFile, setExcelFile] = useState<File | null>(null);
  const [vbaCode, setVbaCode] = useState<string | null>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);

  useEffect(() => {
    const createSession = async () => {
      try {
        const response = await fetch(`${API_URL}/api/session`, {
          method: 'POST',
        });
        
        if (!response.ok) {
          throw new Error('セッションの作成に失敗しました');
        }
        
        const data = await response.json();
        setSessionId(data.session_id);
        
        const welcomeMessage: Message = {
          id: data.message.id,
          role: 'assistant',
          content: data.message.content,
          timestamp: new Date(data.message.timestamp),
        };
        setMessages([welcomeMessage]);
      } catch (error) {
        console.error('Error creating session:', error);
        
        const welcomeMessage: Message = {
          id: uuidv4(),
          role: 'assistant',
          content: 'こんにちは！Mastra AIへようこそ。工事の安全施工計画書とリスクアセスメントの作成をサポートします。Excelファイルをアップロードするか、チャットで情報を提供してください。',
          timestamp: new Date(),
        };
        setMessages([welcomeMessage]);
      }
    };
    
    createSession();
  }, []);

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || !sessionId) return;

    const userMessage: Message = {
      id: uuidv4(),
      role: 'user',
      content,
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);

    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat/${sessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: content
        }),
      });

      if (!response.ok) {
        throw new Error('APIリクエストに失敗しました');
      }

      const data: LLMResponse = await response.json();

      const assistantMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: data.content,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, assistantMessage]);

      if (data.vbaCode) {
        setVbaCode(data.vbaCode);
        setActiveTab('code');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: 'メッセージの送信中にエラーが発生しました。もう一度お試しください。',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFileUpload = async (file: File) => {
    if (!sessionId) return;
    
    setExcelFile(file);

    const formData = new FormData();
    formData.append('file', file);

    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/upload/${sessionId}`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('ファイルのアップロードに失敗しました');
      }

      await response.json();

      const systemMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: `ファイル「${file.name}」が正常にアップロードされました。Excelファイルの解析が完了しました。確定事項入力フォームに情報を入力するか、チャットで詳細情報を提供してください。`,
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, systemMessage]);

      setActiveTab('chat');
    } catch (error) {
      console.error('Error uploading file:', error);
      
      const errorMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: 'ファイルのアップロード中にエラーが発生しました。もう一度お試しください。',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFormSubmit = async (formData: ProjectFormData) => {
    if (!sessionId) return;
    
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/form/${sessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('フォームの送信に失敗しました');
      }

      await response.json();

      const systemMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: '確定情報が正常に送信されました。追加情報についてチャットでお聞きします。',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, systemMessage]);

      setActiveTab('chat');
    } catch (error) {
      console.error('Error submitting form:', error);
      
      const errorMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: 'フォームの送信中にエラーが発生しました。もう一度お試しください。',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };
  
  const handleGenerateVBACode = async () => {
    if (!sessionId) return;
    
    setIsLoading(true);
    
    try {
      const response = await fetch(`${API_URL}/api/generate-vba/${sessionId}`, {
        method: 'POST',
      });
      
      if (!response.ok) {
        throw new Error('VBAコードの生成に失敗しました');
      }
      
      const data = await response.json();
      
      setVbaCode(data.vba_code);
      
      const systemMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: 'VBAコードの生成が完了しました。「VBAコード」タブで確認できます。',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, systemMessage]);
      
      setActiveTab('code');
    } catch (error) {
      console.error('Error generating VBA code:', error);
      
      const errorMessage: Message = {
        id: uuidv4(),
        role: 'assistant',
        content: 'VBAコードの生成中にエラーが発生しました。もう一度お試しください。',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-gray-100">
      <div className="flex-1 flex flex-col max-w-6xl mx-auto p-4">
        <header className="text-center py-6">
          <h1 className="text-3xl font-bold text-gray-900">Mastra AI</h1>
          <p className="text-gray-600 mt-2">
            複数のLLMを連携させたExcel VBAコード生成アシスタント
          </p>
        </header>

        <main className="flex-1 grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Left sidebar - File upload and form */}
          <div className="md:col-span-1 space-y-6">
            <FileUpload onFileUpload={handleFileUpload} />
            <ProjectForm onSubmit={handleFormSubmit} isLoading={isLoading} />
          </div>

          {/* Main content area - Chat and code */}
          <div className="md:col-span-2">
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="chat" className="flex items-center gap-2">
                  <MessageSquare className="h-4 w-4" />
                  チャット
                </TabsTrigger>
                <TabsTrigger value="code" className="flex items-center gap-2" disabled={!vbaCode}>
                  <Code className="h-4 w-4" />
                  VBAコード
                </TabsTrigger>
              </TabsList>
              
              <TabsContent value="chat" className="mt-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-xl">チャット</CardTitle>
                    <CardDescription>
                      AIアシスタントとチャットして、工事情報を提供してください
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="p-0">
                    <div className="flex flex-col h-[500px]">
                      <div className="flex-1 overflow-y-auto p-4 space-y-4">
                        {messages.map((message) => (
                          <ChatMessage key={message.id} message={message} />
                        ))}
                      </div>
                      <Separator />
                      <div className="p-4 space-y-4">
                        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
                        {excelFile && sessionId && (
                          <button
                            onClick={handleGenerateVBACode}
                            disabled={isLoading}
                            className="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded-md disabled:opacity-50"
                          >
                            VBAコードを生成
                          </button>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
              
              <TabsContent value="code" className="mt-4">
                {vbaCode ? (
                  <VBACodeDisplay code={vbaCode} />
                ) : (
                  <Card>
                    <CardContent className="p-6 text-center text-gray-500">
                      VBAコードはまだ生成されていません。
                      チャットで情報を提供し、Excelファイルをアップロードしてください。
                    </CardContent>
                  </Card>
                )}
              </TabsContent>
            </Tabs>
          </div>
        </main>

        <footer className="py-6 text-center text-sm text-gray-500">
          © 2025 Mastra AI - 安全施工計画書とリスクアセスメント自動生成システム
        </footer>
      </div>
    </div>
  );
}

export default App;
