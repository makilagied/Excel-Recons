# 📊 Excel Reconciliation Tool

A modern web-based application for reconciling data between two Excel sheets. This tool helps you identify matched records, records unique to each sheet, and provides detailed reconciliation reports.

## 🌟 Features

- **Web-based UI**: User-friendly Streamlit interface for easy data reconciliation
- **Interactive Sheet Selection**: Choose any two sheets from your Excel file
- **Smart Column Matching**: Automatically detects common columns between sheets
- **Data Preview**: Preview your data before processing
- **Comprehensive Results**: 
  - **Matched**: Records found in both sheets
  - **Left Only**: Records found only in the first sheet
  - **Right Only**: Records found only in the second sheet
- **Real-time Statistics**: View reconciliation metrics at a glance
- **Download Results**: Export reconciled data as Excel file
- **Production Ready**: Can be deployed as a systemd service

## 📋 Requirements

- Python 3.7 or higher
- pip (Python package manager)
- Linux system (for systemd deployment)

## 🚀 Quick Start

### Local Development Setup

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

5. **Access the application**:
   Open your browser and navigate to `http://localhost:8501`

## 📖 Usage Guide

### Step-by-Step Instructions

1. **Upload Excel File**
   - Click "Upload Excel File" button
   - Select an Excel file (`.xlsx` or `.xls`) containing at least 2 sheets
   - The file must have at least two sheets to perform reconciliation

2. **Select Sheets**
   - Choose the first sheet from the dropdown
   - Choose the second sheet from the dropdown
   - The second dropdown automatically excludes the first selected sheet

3. **Select Matching Column**
   - Choose a column that exists in both sheets
   - This column will be used to match records between sheets
   - Only common columns are shown in the dropdown

4. **Preview Data**
   - Review the first 10 rows of each sheet
   - Verify that your selections are correct

5. **Process Reconciliation**
   - Click "🔄 Process Reconciliation" button
   - Wait for processing to complete

6. **Review Results**
   - View statistics: Total Records, Matched, Left Only, Right Only
   - Browse results in three tabs: Matched, Left Only, Right Only

7. **Download Results**
   - Click "📥 Download Reconciliation Results" button
   - The downloaded file contains three sheets:
     - **Matched**: Records found in both sheets (with all columns from both)
     - **Left Only**: Records only in the first sheet
     - **Right Only**: Records only in the second sheet

### Example Use Cases

- **Data Migration Verification**: Compare data before and after migration
- **Database Reconciliation**: Match records between two data sources
- **Audit Trail**: Identify discrepancies between systems
- **Customer Data Matching**: Find common and unique customer records
- **Financial Reconciliation**: Compare transaction records

## 🏗️ Project Structure

```
Excel Recons/
├── app.py                 # Streamlit web application
├── recons.py              # Core reconciliation logic
├── requirements.txt       # Python dependencies
├── setup_venv.sh          # Virtual environment setup script
├── run_app.sh             # Application startup script
├── deploy.sh              # Automated deployment script
├── excel-recons.service   # Systemd service file
├── DEPLOYMENT.md          # Detailed deployment guide
└── README.md              # This file
```

## 🔧 How It Works

### Reconciliation Logic

The tool uses pandas' merge functionality with an outer join to combine data from two sheets:

1. **Read Sheets**: Loads both selected sheets into pandas DataFrames
2. **Merge Data**: Performs an outer join on the selected matching column
3. **Categorize Records**:
   - **Matched**: Records where the match column value exists in both sheets
   - **Left Only**: Records where the match column value exists only in the first sheet
   - **Right Only**: Records where the match column value exists only in the second sheet
4. **Generate Output**: Creates an Excel file with three separate sheets

### Column Naming

When records are matched, columns from both sheets are included:
- Columns from the first sheet have `_left` suffix
- Columns from the second sheet have `_right` suffix
- The matching column appears only once (without suffix)

## 🚀 Production Deployment

### Automated Deployment

For quick deployment as a systemd service:

```bash
# Make scripts executable
chmod +x deploy.sh setup_venv.sh run_app.sh

# Run deployment (requires sudo)
sudo ./deploy.sh
```

This will:
- Install the application to `/opt/excel-recons`
- Set up a virtual environment
- Install dependencies
- Configure and start the systemd service

### Manual Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed manual deployment instructions.

### Service Management

```bash
# Start service
sudo systemctl start excel-recons

# Stop service
sudo systemctl stop excel-recons

# Restart service
sudo systemctl restart excel-recons

# Check status
sudo systemctl status excel-recons

# View logs
sudo journalctl -u excel-recons -f
```

## 📦 Dependencies

- **streamlit** (>=1.28.0): Web framework for the UI
- **pandas** (>=2.0.0): Data manipulation and Excel operations
- **openpyxl** (>=3.1.0): Excel file reading/writing
- **xlrd** (>=2.0.1): Legacy Excel file support

## 🐛 Troubleshooting

### Common Issues

**Issue: "No common columns found"**
- **Solution**: Ensure both sheets have at least one column with the same name

**Issue: "Column not found in one of the sheets"**
- **Solution**: Verify the selected column exists in both sheets (case-sensitive)

**Issue: Service won't start**
- **Solution**: Check logs with `sudo journalctl -u excel-recons -n 50`
- Verify virtual environment exists: `ls -la /opt/excel-recons/venv`

**Issue: Port 8501 already in use**
- **Solution**: Change the port in `run_app.sh` or stop the conflicting service

**Issue: Permission denied errors**
- **Solution**: Ensure proper file permissions:
  ```bash
  sudo chown -R $USER:$USER /opt/excel-recons
  chmod +x /opt/excel-recons/run_app.sh
  ```

### Getting Help

1. Check the logs: `sudo journalctl -u excel-recons -f`
2. Test manually: Run `streamlit run app.py` directly
3. Verify dependencies: `pip list` in the virtual environment

## 🔒 Security Considerations

- The application runs with the permissions of the configured user
- File uploads are processed in memory and temporary files are cleaned up
- Consider using a reverse proxy (nginx) with SSL/TLS for production
- Restrict network access via firewall rules if needed
- For sensitive data, consider running on localhost only

## 📝 Command Line Usage

The core reconciliation function can also be used programmatically:

```python
from recons import merge_excel_sheets

merge_excel_sheets(
    file_path="data.xlsx",
    sheet1_name="Sheet1",
    sheet2_name="Sheet2",
    output_path="output.xlsx",
    match_column="email"
)
```

## 🎯 Best Practices

1. **Data Preparation**:
   - Ensure the matching column has consistent formatting
   - Remove leading/trailing whitespace if needed
   - Handle null/empty values appropriately

2. **Performance**:
   - For large files (>100MB), processing may take time
   - Consider splitting very large datasets

3. **Data Quality**:
   - Verify the matching column contains unique identifiers when possible
   - Review preview data before processing

## 📄 License

This project is provided as-is for use and modification.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📞 Support

For issues, questions, or feature requests, please open an issue in the repository.

---

**Made with ❤️ for data reconciliation needs**

