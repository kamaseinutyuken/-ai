import React, { useState } from "react";
import { ProjectFormData } from "../types";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";

interface ProjectFormProps {
  onSubmit: (data: ProjectFormData) => void;
  isLoading: boolean;
}

export function ProjectForm({ onSubmit, isLoading }: ProjectFormProps) {
  const [formData, setFormData] = useState<ProjectFormData>({
    projectName: "",
    location: "",
    period: "",
    workerCount: 0
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === "workerCount" ? parseInt(value) || 0 : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>確定事項入力フォーム</CardTitle>
        <CardDescription>
          以下の項目を入力してください。これらの情報はExcelファイルの指定されたセルに入力されます。
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="projectName">
              工事名 <span className="text-xs text-gray-500">(セルI9)</span>
            </Label>
            <Input
              id="projectName"
              name="projectName"
              value={formData.projectName}
              onChange={handleChange}
              placeholder="工事名を入力"
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="location">
              施工場所 <span className="text-xs text-gray-500">(セルI11)</span>
            </Label>
            <Input
              id="location"
              name="location"
              value={formData.location}
              onChange={handleChange}
              placeholder="施工場所を入力"
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="period">
              工期 <span className="text-xs text-gray-500">(セルI13)</span>
            </Label>
            <Input
              id="period"
              name="period"
              value={formData.period}
              onChange={handleChange}
              placeholder="工期を入力（例: 2025年4月1日～2025年5月31日）"
              required
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="workerCount">
              作業者数 <span className="text-xs text-gray-500">(セルQ15)</span>
            </Label>
            <Input
              id="workerCount"
              name="workerCount"
              type="number"
              min="0"
              value={formData.workerCount || ""}
              onChange={handleChange}
              placeholder="作業者数を入力"
              required
            />
          </div>
        </CardContent>
        <CardFooter>
          <Button type="submit" disabled={isLoading} className="w-full">
            {isLoading ? "送信中..." : "確定情報を送信"}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}
