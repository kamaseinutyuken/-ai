from typing import Dict, Any, List, Optional
from .models import FormData, Message
from .llm_service import generate_vba_code

async def generate_vba_from_data(
    form_data: FormData,
    excel_data: Optional[Dict[str, Any]],
    chat_history: List[Message]
) -> str:
    """
    Generate VBA code based on form data, Excel data, and chat history
    """
    vba_code = await generate_vba_code(form_data, excel_data, chat_history)
    
    formatted_vba = format_vba_code(vba_code)
    
    return formatted_vba

def format_vba_code(vba_code: str) -> str:
    """
    Format VBA code for better readability
    """
    vba_code = vba_code.replace("```vba", "").replace("```", "").strip()
    
    vba_code = vba_code.replace("\r\n", "\n").replace("\r", "\n")
    
    header = """
'*******************************************************************************
' Mastra AI によって生成されたVBAコード
' 生成日時: ' + Format(Now, "yyyy/mm/dd hh:nn:ss") + '
'*******************************************************************************

"""
    
    return header + vba_code
