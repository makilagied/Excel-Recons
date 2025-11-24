import pandas as pd

def merge_excel_sheets(file_path, sheet1_name, sheet2_name, output_path, match_column='email'):
    """
    Reconcile two Excel sheets by merging them on a specified column.
    Creates three separate sheets:
    - 'Matched': Records found in both sheets
    - 'Left Only': Records found only in the first sheet
    - 'Right Only': Records found only in the second sheet
    """
    # Read sheets
    df1 = pd.read_excel(file_path, sheet_name=sheet1_name)
    df2 = pd.read_excel(file_path, sheet_name=sheet2_name)

    # Ensure the match column exists
    if match_column not in df1.columns or match_column not in df2.columns:
        raise ValueError(f"Column '{match_column}' not found in one of the sheets")

    # Merge data with outer join to get all records
    merged = pd.merge(df1, df2, on=match_column, how='outer', indicator=True, suffixes=('_left', '_right'))

    # Separate into three categories
    matched = merged[merged['_merge'] == 'both'].drop(columns=['_merge'])
    left_only = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])
    right_only = merged[merged['_merge'] == 'right_only'].drop(columns=['_merge'])

    # Write to new Excel file with three separate sheets
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        matched.to_excel(writer, sheet_name='Matched', index=False)
        left_only.to_excel(writer, sheet_name='Left Only', index=False)
        right_only.to_excel(writer, sheet_name='Right Only', index=False)

    print(f"Reconciliation completed! File saved to: {output_path}")
    print(f"Total records: {len(merged)}")
    print(f"  - Matched: {len(matched)}")
    print(f"  - Left only: {len(left_only)}")
    print(f"  - Right only: {len(right_only)}")


if __name__ == "__main__":
    # Example usage
    # You can modify these parameters based on your Excel file structure
    input_file = "recons.xlsx"
    sheet1 = "Sheet1"  # Change to your first sheet name
    sheet2 = "Sheet2"  # Change to your second sheet name
    output_file = "recons_output.xlsx"
    match_col = "email"  # Change to the column you want to match on
    
    merge_excel_sheets(input_file, sheet1, sheet2, output_file, match_col)

