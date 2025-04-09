import { Message } from "../types";
import { cn } from "../lib/utils";

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  
  return (
    <div
      className={cn(
        "flex w-full items-start gap-2 p-4 rounded-lg",
        isUser ? "bg-blue-50 flex-row-reverse" : "bg-gray-50"
      )}
    >
      <div
        className={cn(
          "flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border shadow",
          isUser ? "bg-blue-600 text-white" : "bg-gray-100"
        )}
      >
        {isUser ? "U" : "AI"}
      </div>
      <div className="flex-1 space-y-2">
        <div className="prose prose-sm max-w-none">
          <p>{message.content}</p>
        </div>
        <div className="text-xs text-gray-500">
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}
