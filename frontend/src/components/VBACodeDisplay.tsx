import { useState } from "react";
import { Copy, Check } from "lucide-react";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";

interface VBACodeDisplayProps {
  code: string;
}

export function VBACodeDisplay({ code }: VBACodeDisplayProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Card className="w-full">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">生成されたVBAコード</CardTitle>
        <Button
          variant="outline"
          size="sm"
          className="h-8 px-2 lg:px-3"
          onClick={handleCopy}
        >
          {copied ? (
            <>
              <Check className="h-4 w-4 mr-1" />
              コピー済み
            </>
          ) : (
            <>
              <Copy className="h-4 w-4 mr-1" />
              コピー
            </>
          )}
        </Button>
      </CardHeader>
      <CardContent>
        <div className="relative">
          <pre className="max-h-96 overflow-auto rounded-lg bg-gray-900 p-4 text-xs text-gray-50">
            <code>{code}</code>
          </pre>
        </div>
      </CardContent>
    </Card>
  );
}
