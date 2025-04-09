import requests
import json
import os
import time
from pathlib import Path

API_URL = "http://localhost:1337"

def test_api_workflow():
    """Test the complete API workflow"""
    print("Starting API workflow test...")
    
    print("\n1. Creating session...")
    session_response = requests.post(f"{API_URL}/api/session")
    if session_response.status_code != 200:
        print(f"Error creating session: {session_response.text}")
        return
    
    session_data = session_response.json()
    session_id = session_data["session_id"]
    print(f"Session created with ID: {session_id}")
    print(f"Welcome message: {session_data['message']['content']}")
    
    print("\n2. Uploading Excel file...")
    excel_file_path = Path("test_file.xlsx")
    if not excel_file_path.exists():
        print(f"Error: Test file not found at {excel_file_path}")
        return
    
    with open(excel_file_path, "rb") as f:
        files = {"file": (excel_file_path.name, f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
        upload_response = requests.post(f"{API_URL}/api/upload/{session_id}", files=files)
    
    if upload_response.status_code != 200:
        print(f"Error uploading file: {upload_response.text}")
        return
    
    upload_data = upload_response.json()
    print(f"File upload status: {upload_data['status']}")
    print(f"File upload message: {upload_data['message']}")
    
    print("Waiting for file processing...")
    time.sleep(2)
    
    print("\n3. Submitting form data...")
    form_data = {
        "projectName": "テスト工事",
        "location": "東京都渋谷区",
        "period": "2025年4月1日～2025年5月31日",
        "workerCount": 10
    }
    
    form_response = requests.post(
        f"{API_URL}/api/form/{session_id}",
        json=form_data,
        headers={"Content-Type": "application/json"}
    )
    
    if form_response.status_code != 200:
        print(f"Error submitting form: {form_response.text}")
        return
    
    form_result = form_response.json()
    print(f"Form submission status: {form_result['status']}")
    print(f"Form submission message: {form_result['message']}")
    
    print("\n4. Sending chat message (first round)...")
    chat_message = "これは建設現場での安全対策に関するテスト工事です。高所作業が含まれます。"
    
    chat_response = requests.post(
        f"{API_URL}/api/chat/{session_id}",
        json={"message": chat_message},
        headers={"Content-Type": "application/json"}
    )
    
    if chat_response.status_code != 200:
        print(f"Error sending chat message: {chat_response.text}")
        return
    
    chat_result = chat_response.json()
    print(f"Chat response: {chat_result['content']}")
    
    print("\n5. Sending chat message (second round)...")
    chat_message2 = "使用する主な機械は、クレーン、高所作業車、電動工具です。過去には転落事故が発生したことがあります。"
    
    chat_response2 = requests.post(
        f"{API_URL}/api/chat/{session_id}",
        json={"message": chat_message2},
        headers={"Content-Type": "application/json"}
    )
    
    if chat_response2.status_code != 200:
        print(f"Error sending second chat message: {chat_response2.text}")
        return
    
    chat_result2 = chat_response2.json()
    print(f"Chat response (second round): {chat_result2['content']}")
    
    print("\n6. Sending chat message (third round)...")
    chat_message3 = "安全対策として、全作業員にヘルメット、安全帯を着用させ、朝礼で危険予知活動を行います。緊急連絡先は現場責任者の携帯電話です。"
    
    chat_response3 = requests.post(
        f"{API_URL}/api/chat/{session_id}",
        json={"message": chat_message3},
        headers={"Content-Type": "application/json"}
    )
    
    if chat_response3.status_code != 200:
        print(f"Error sending third chat message: {chat_response3.text}")
        return
    
    chat_result3 = chat_response3.json()
    print(f"Chat response (third round): {chat_result3['content']}")
    
    print("\n7. Generating VBA code...")
    vba_response = requests.post(f"{API_URL}/api/generate-vba/{session_id}")
    
    if vba_response.status_code != 200:
        print(f"Error generating VBA code: {vba_response.text}")
        return
    
    vba_result = vba_response.json()
    vba_code = vba_result["vba_code"]
    print(f"VBA code generated successfully. Length: {len(vba_code)} characters")
    print("\nFirst 200 characters of VBA code:")
    print(vba_code[:200] + "...")
    
    print("\n8. Getting chat history...")
    history_response = requests.get(f"{API_URL}/api/chat-history/{session_id}")
    
    if history_response.status_code != 200:
        print(f"Error getting chat history: {history_response.text}")
        return
    
    history_data = history_response.json()
    chat_history = history_data["chat_history"]
    print(f"Chat history retrieved. {len(chat_history)} messages found.")
    
    print("\nAPI workflow test completed successfully!")

if __name__ == "__main__":
    test_api_workflow()
