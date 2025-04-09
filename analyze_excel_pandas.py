import pandas as pd
import os

excel_file_path = os.path.expanduser("~/attachments/c49c933d-c879-4bc7-9820-863924d20bc0/.xlsx")

try:
    print(f"Analyzing Excel file: {excel_file_path}")
    file_size = os.path.getsize(excel_file_path)
    print(f"File size: {file_size} bytes")
    
    print("\nAttempting to read with pandas...")
    xls = pd.ExcelFile(excel_file_path)
    print(f"Sheet names: {xls.sheet_names}")
    
    required_sheets = ["安全施工計画書", "リスクアセスメント"]
    for sheet_name in required_sheets:
        if sheet_name in xls.sheet_names:
            print(f"Found required sheet: {sheet_name}")
        else:
            print(f"WARNING: Required sheet '{sheet_name}' not found!")
    
    for sheet_name in xls.sheet_names:
        print(f"\nSample data from sheet '{sheet_name}':")
        df = pd.read_excel(excel_file_path, sheet_name=sheet_name, nrows=5)
        print(df.head())
        
        full_df = pd.read_excel(excel_file_path, sheet_name=sheet_name)
        print(f"Dimensions: {full_df.shape[0]} rows x {full_df.shape[1]} columns")
        
        if sheet_name == "安全施工計画書":
            try:
                fixed_cells = {
                    "I9": "工事名",
                    "I11": "施工場所",
                    "I13": "工期",
                    "Q15": "作業者数"
                }
                
                print("\nChecking fixed cells in 安全施工計画書:")
                for cell, description in fixed_cells.items():
                    col = ord(cell[0]) - ord('A')
                    row = int(cell[1:]) - 1
                    value = full_df.iloc[row, col] if row < full_df.shape[0] and col < full_df.shape[1] else "Out of bounds"
                    print(f"{description} ({cell}): {value}")
            except Exception as e:
                print(f"Error checking fixed cells: {e}")
                
            try:
                print("\nSample cells from D, AS, BK columns in 安全施工計画書:")
                for row in [33, 53, 80, 107]:  # 0-indexed for rows 34, 54, 81, 108
                    for col_letter in ['D', 'AS', 'BK']:
                        col = ord(col_letter[0]) - ord('A')
                        if len(col_letter) > 1:
                            col = 26 + (ord(col_letter[1]) - ord('A'))
                        value = full_df.iloc[row, col] if row < full_df.shape[0] and col < full_df.shape[1] else "Out of bounds"
                        print(f"{col_letter}{row+1}: {value}")
            except Exception as e:
                print(f"Error checking sample cells: {e}")

except Exception as e:
    print(f"Error analyzing Excel file: {e}")
