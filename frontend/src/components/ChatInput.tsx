import React, { useState } from "react";
import { SendHorizontal } from "lucide-react";
import { Button } from "./ui/button";
import { Textarea } from "./ui/textarea";

interface ChatInputProps {
  onSendMessage: (content: string) => void;
  isLoading: boolean;
}

export function ChatInput({ onSendMessage, isLoading }: ChatInputProps) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim()) {
      onSendMessage(message);
      setMessage("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex items-end gap-2">
      <Textarea
        placeholder="メッセージを入力してください..."
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        className="min-h-24 flex-1 resize-none"
        disabled={isLoading}
      />
      <Button type="submit" size="icon" disabled={!message.trim() || isLoading}>
        <SendHorizontal className="h-4 w-4" />
        <span className="sr-only">送信</span>
      </Button>
    </form>
  );
}
