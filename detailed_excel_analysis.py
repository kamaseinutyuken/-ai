import pandas as pd
import os

excel_file_path = os.path.expanduser("~/attachments/c49c933d-c879-4bc7-9820-863924d20bc0/.xlsx")

def convert_excel_col_to_index(col_str):
    """Convert Excel column string to index (0-based)"""
    result = 0
    for char in col_str:
        result = result * 26 + (ord(char) - ord('A') + 1)
    return result - 1

def check_cell_ranges(df, sheet_name, columns, rows):
    """Check specific cell ranges and return non-empty values"""
    print(f"\nChecking {sheet_name} - Columns: {columns}, Rows: {rows}")
    non_empty_cells = {}
    
    for col in columns:
        col_idx = convert_excel_col_to_index(col)
        if col_idx >= df.shape[1]:
            print(f"Column {col} (index {col_idx}) is out of bounds for dataframe with {df.shape[1]} columns")
            continue
            
        for row in rows:
            row_idx = row - 1  # Convert to 0-based index
            if row_idx >= df.shape[0]:
                continue
                
            value = df.iloc[row_idx, col_idx]
            if pd.notna(value) and value != "":
                cell_ref = f"{col}{row}"
                non_empty_cells[cell_ref] = value
                print(f"{cell_ref}: {value}")
    
    return non_empty_cells

try:
    print(f"Analyzing Excel file: {excel_file_path}")
    
    xls = pd.ExcelFile(excel_file_path)
    print(f"Sheet names: {xls.sheet_names}")
    
    if "安全施工計画書" in xls.sheet_names:
        print("\n=== 安全施工計画書 シート ===")
        df = pd.read_excel(excel_file_path, sheet_name="安全施工計画書")
        
        fixed_cells = {
            "I9": "工事名",
            "I11": "施工場所",
            "I13": "工期",
            "Q15": "作業者数"
        }
        
        print("\nFixed cells:")
        for cell, description in fixed_cells.items():
            col = cell[0]
            row = int(cell[1:])
            col_idx = convert_excel_col_to_index(col)
            row_idx = row - 1
            
            if row_idx < df.shape[0] and col_idx < df.shape[1]:
                value = df.iloc[row_idx, col_idx]
                print(f"{description} ({cell}): {value}")
            else:
                print(f"{description} ({cell}): Out of bounds")
        
        columns = ["D", "AS", "BK"]
        
        rows1 = list(range(34, 44))
        check_cell_ranges(df, "安全施工計画書", columns, rows1)
        
        rows2 = list(range(54, 74))
        check_cell_ranges(df, "安全施工計画書", columns, rows2)
        
        rows3 = list(range(81, 101))
        check_cell_ranges(df, "安全施工計画書", columns, rows3)
        
        rows4 = list(range(108, 128))
        check_cell_ranges(df, "安全施工計画書", columns, rows4)
    
    if "リスクアセスメント" in xls.sheet_names:
        print("\n=== リスクアセスメント シート ===")
        df = pd.read_excel(excel_file_path, sheet_name="リスクアセスメント")
        
        columns = ["C", "O", "Y", "AI", "AS", "CC", "AV", "CF", "BE", "CL"]
        
        sample_rows = [34, 37, 40, 48, 51, 54, 57, 60, 63, 66, 69, 72, 75, 78, 81, 84, 87, 96, 99, 102]
        check_cell_ranges(df, "リスクアセスメント", columns, sample_rows)
        
        all_rows = []
        all_rows.extend(list(range(34, 38)))  # 34, 37
        all_rows.extend(list(range(40, 41)))  # 40
        all_rows.extend(list(range(48, 49)))  # 48
        all_rows.extend(list(range(51, 52)))  # 51
        
        print(f"\nTotal rows to check in リスクアセスメント: {len(all_rows)}")
        print(f"Sample of rows checked: {sample_rows[:10]}...")

except Exception as e:
    print(f"Error analyzing Excel file: {e}")
