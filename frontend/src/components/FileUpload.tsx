import React, { useState } from "react";
import { Upload, X, FileText } from "lucide-react";
import { Button } from "./ui/button";
import { Progress } from "./ui/progress";

interface FileUploadProps {
  onFileUpload: (file: File) => Promise<void>;
}

export function FileUpload({ onFileUpload }: FileUploadProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (
        selectedFile.type === "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" ||
        selectedFile.type === "application/vnd.ms-excel.sheet.macroEnabled.12" ||
        selectedFile.name.endsWith(".xlsx") ||
        selectedFile.name.endsWith(".xlsm")
      ) {
        setFile(selectedFile);
        setError(null);
      } else {
        setError("Excelファイル(.xlsx または .xlsm)のみアップロード可能です。");
        setFile(null);
      }
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    try {
      setUploading(true);
      setProgress(0);
      
      const interval = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 95) {
            clearInterval(interval);
            return 95;
          }
          return prev + 5;
        });
      }, 100);

      await onFileUpload(file);
      
      clearInterval(interval);
      setProgress(100);
      
      setTimeout(() => {
        setFile(null);
        setUploading(false);
        setProgress(0);
      }, 1000);
    } catch (error) {
      setError("ファイルのアップロードに失敗しました。");
      setUploading(false);
    }
  };

  const handleRemoveFile = () => {
    setFile(null);
    setError(null);
  };

  return (
    <div className="space-y-4 p-4 border rounded-lg bg-gray-50">
      <div className="text-sm font-medium">Excelファイルのアップロード</div>
      
      {!file ? (
        <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-lg p-6 bg-white">
          <Upload className="h-8 w-8 text-gray-400 mb-2" />
          <p className="text-sm text-gray-500 mb-2">
            ここにExcelファイル(.xlsm)をドラッグ＆ドロップ
          </p>
          <p className="text-xs text-gray-400 mb-4">または</p>
          <label className="cursor-pointer">
            <Button variant="outline" size="sm">
              ファイルを選択
            </Button>
            <input
              type="file"
              className="hidden"
              accept=".xlsx,.xlsm,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel.sheet.macroEnabled.12"
              onChange={handleFileChange}
            />
          </label>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="flex items-center justify-between p-3 border rounded bg-white">
            <div className="flex items-center gap-2">
              <FileText className="h-5 w-5 text-blue-500" />
              <div className="text-sm font-medium truncate max-w-xs">
                {file.name}
              </div>
              <div className="text-xs text-gray-500">
                {(file.size / 1024).toFixed(0)} KB
              </div>
            </div>
            <Button
              variant="ghost"
              size="icon"
              onClick={handleRemoveFile}
              disabled={uploading}
            >
              <X className="h-4 w-4" />
              <span className="sr-only">削除</span>
            </Button>
          </div>

          {uploading && (
            <div className="space-y-1">
              <Progress value={progress} className="h-2" />
              <div className="text-xs text-gray-500 text-right">
                {progress}%
              </div>
            </div>
          )}

          <Button
            onClick={handleUpload}
            disabled={uploading}
            className="w-full"
          >
            {uploading ? "アップロード中..." : "アップロード"}
          </Button>
        </div>
      )}

      {error && (
        <div className="text-sm text-red-500 mt-2">{error}</div>
      )}
    </div>
  );
}
