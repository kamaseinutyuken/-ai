from typing import Dict, Any, List, Optional
import logging
from .models import FormData, Message
from .llm_service import generate_vba_code, USE_MOCK_RESPONSE

logger = logging.getLogger(__name__)

async def generate_vba_from_data(
    form_data: FormData,
    excel_data: Optional[Dict[str, Any]],
    chat_history: List[Message]
) -> str:
    """
    Generate VBA code based on form data, Excel data, and chat history
    """
    if USE_MOCK_RESPONSE:
        logger.warning("Using mock response for VBA code generation")
        mock_vba = f"""
Sub MastraAI_入力処理()
    ' 確定情報の入力
    Range("I9").Value = "{form_data.projectName}"
    Range("I11").Value = "{form_data.location}"
    Range("I13").Value = "{form_data.period}"
    Range("Q15").Value = {form_data.workerCount}
    
    ' 安全施工計画書シートの入力
    Sheets("安全施工計画書").Select
    
    ' 準備作業の入力
    Range("D34").Value = "資材搬入"
    Range("AS34").Value = "転倒・落下"
    Range("BK34").Value = "ヘルメット着用、安全靴着用"
    
    Range("D35").Value = "現場確認"
    Range("AS35").Value = "転倒・接触"
    Range("BK35").Value = "周囲確認、安全通路確保"
    
    ' 本作業の入力
    Range("D54").Value = "足場組立"
    Range("AS54").Value = "墜落・転落"
    Range("BK54").Value = "安全帯使用、手すり先行工法"
    
    ' リスクアセスメントシートの入力
    Sheets("リスクアセスメント").Select
    
    Range("C34").Value = "資材搬入時の事故"
    Range("O34").Value = "3"
    Range("Y34").Value = "4"
    
    Range("C48").Value = "高所作業時の墜落"
    Range("O48").Value = "5"
    Range("Y48").Value = "5"
    
    MsgBox "データの入力が完了しました。", vbInformation
End Sub
"""
        return format_vba_code(mock_vba)
    
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
