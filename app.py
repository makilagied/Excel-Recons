import streamlit as st
import pandas as pd
import io
from recons import merge_excel_sheets
import tempfile
import os

st.set_page_config(
    page_title="Excel Reconciliation Tool",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Excel Reconciliation Tool")
st.markdown("Upload an Excel file, select sheets and columns to reconcile your data.")

# File upload
uploaded_file = st.file_uploader(
    "Upload Excel File",
    type=['xlsx', 'xls'],
    help="Upload an Excel file containing the sheets you want to reconcile"
)

if uploaded_file is not None:
    try:
        # Read Excel file to get sheet names
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names
        
        if len(sheet_names) < 2:
            st.error("⚠️ The Excel file must contain at least 2 sheets for reconciliation.")
        else:
            # Create two columns for sheet selection
            col1, col2 = st.columns(2)
            
            with col1:
                sheet1_name = st.selectbox(
                    "Select First Sheet",
                    sheet_names,
                    key="sheet1",
                    help="Select the first sheet to reconcile"
                )
            
            with col2:
                # Filter out the first selected sheet from second dropdown
                remaining_sheets = [s for s in sheet_names if s != sheet1_name]
                sheet2_name = st.selectbox(
                    "Select Second Sheet",
                    remaining_sheets if remaining_sheets else sheet_names,
                    key="sheet2",
                    help="Select the second sheet to reconcile"
                )
            
            # Read both sheets to get column names
            try:
                df1 = pd.read_excel(uploaded_file, sheet_name=sheet1_name)
                df2 = pd.read_excel(uploaded_file, sheet_name=sheet2_name)
                
                # Find common columns
                common_columns = list(set(df1.columns) & set(df2.columns))
                
                if not common_columns:
                    st.error("⚠️ No common columns found between the two sheets. Cannot perform reconciliation.")
                else:
                    # Column selection
                    match_column = st.selectbox(
                        "Select Column to Match On",
                        common_columns,
                        help="Select the column that exists in both sheets to use for matching"
                    )
                    
                    # Show preview of data
                    st.subheader("📋 Data Preview")
                    preview_col1, preview_col2 = st.columns(2)
                    
                    with preview_col1:
                        st.write(f"**{sheet1_name}** ({len(df1)} rows)")
                        st.dataframe(df1.head(10), use_container_width=True)
                    
                    with preview_col2:
                        st.write(f"**{sheet2_name}** ({len(df2)} rows)")
                        st.dataframe(df2.head(10), use_container_width=True)
                    
                    # Process button
                    if st.button("🔄 Process Reconciliation", type="primary", use_container_width=True):
                        with st.spinner("Processing reconciliation..."):
                            try:
                                # Create temporary file for output
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_file:
                                    output_path = tmp_file.name
                                
                                # Save uploaded file temporarily to read it
                                with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp_input:
                                    tmp_input.write(uploaded_file.getvalue())
                                    tmp_input_path = tmp_input.name
                                
                                # Perform reconciliation
                                merge_excel_sheets(
                                    tmp_input_path,
                                    sheet1_name,
                                    sheet2_name,
                                    output_path,
                                    match_column
                                )
                                
                                # Read the output file
                                with open(output_path, 'rb') as f:
                                    output_data = f.read()
                                
                                # Clean up temporary files
                                os.unlink(tmp_input_path)
                                os.unlink(output_path)
                                
                                # Store in session state
                                st.session_state['output_file'] = output_data
                                st.session_state['output_filename'] = f"reconciliation_output.xlsx"
                                
                                st.success("✅ Reconciliation completed successfully!")
                                
                                # Read output to show statistics
                                output_excel = pd.ExcelFile(io.BytesIO(output_data))
                                matched_df = pd.read_excel(io.BytesIO(output_data), sheet_name='Matched')
                                left_only_df = pd.read_excel(io.BytesIO(output_data), sheet_name='Left Only')
                                right_only_df = pd.read_excel(io.BytesIO(output_data), sheet_name='Right Only')
                                
                                # Display statistics
                                st.subheader("📈 Reconciliation Results")
                                stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
                                
                                with stats_col1:
                                    st.metric("Total Records", len(matched_df) + len(left_only_df) + len(right_only_df))
                                
                                with stats_col2:
                                    st.metric("Matched", len(matched_df), delta=None)
                                
                                with stats_col3:
                                    st.metric("Left Only", len(left_only_df), delta=None)
                                
                                with stats_col4:
                                    st.metric("Right Only", len(right_only_df), delta=None)
                                
                                # Show preview of results
                                st.subheader("📄 Output Preview")
                                result_tabs = st.tabs(["Matched", "Left Only", "Right Only"])
                                
                                with result_tabs[0]:
                                    st.write(f"**Matched Records ({len(matched_df)})**")
                                    st.dataframe(matched_df, use_container_width=True)
                                
                                with result_tabs[1]:
                                    st.write(f"**Left Only Records ({len(left_only_df)})**")
                                    st.dataframe(left_only_df, use_container_width=True)
                                
                                with result_tabs[2]:
                                    st.write(f"**Right Only Records ({len(right_only_df)})**")
                                    st.dataframe(right_only_df, use_container_width=True)
                                
                            except Exception as e:
                                st.error(f"❌ Error during reconciliation: {str(e)}")
                    
                    # Download button (shown after processing)
                    if 'output_file' in st.session_state:
                        st.download_button(
                            label="📥 Download Reconciliation Results",
                            data=st.session_state['output_file'],
                            file_name=st.session_state['output_filename'],
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            use_container_width=True,
                            type="primary"
                        )
                        
            except Exception as e:
                st.error(f"❌ Error reading sheets: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ Error reading Excel file: {str(e)}")
        st.info("Please make sure the file is a valid Excel file (.xlsx or .xls)")

else:
    st.info("👆 Please upload an Excel file to get started.")
    st.markdown("""
    ### How to use:
    1. **Upload** your Excel file containing at least 2 sheets
    2. **Select** the two sheets you want to reconcile
    3. **Choose** the column to match on (must exist in both sheets)
    4. **Click** "Process Reconciliation" to generate results
    5. **Download** the output file with three sheets: Matched, Left Only, and Right Only
    """)

