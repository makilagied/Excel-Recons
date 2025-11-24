# Excel Reconciliation Tool - Deployment Guide

This guide explains how to deploy the Excel Reconciliation Tool as a systemd service with a virtual environment.

## Prerequisites

- Linux system with systemd (Ubuntu, Debian, CentOS, etc.)
- Python 3.7 or higher
- Root/sudo access
- Network access (for downloading packages)

## Quick Deployment

### Option 1: Automated Deployment (Recommended)

1. **Make the deployment script executable:**
   ```bash
   chmod +x deploy.sh
   ```

2. **Run the deployment script as root:**
   ```bash
   sudo ./deploy.sh
   ```

The script will:
- Create the application directory at `/opt/excel-recons`
- Set up a virtual environment
- Install all dependencies
- Create and enable the systemd service
- Start the application

### Option 2: Manual Deployment

#### Step 1: Create Application Directory

```bash
sudo mkdir -p /opt/excel-recons
sudo chown $USER:$USER /opt/excel-recons
```

#### Step 2: Copy Application Files

```bash
cp app.py recons.py requirements.txt /opt/excel-recons/
cp setup_venv.sh run_app.sh /opt/excel-recons/
cd /opt/excel-recons
```

#### Step 3: Set Up Virtual Environment

```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Make Scripts Executable

```bash
chmod +x run_app.sh
chmod +x setup_venv.sh
```

#### Step 5: Install Systemd Service

1. **Edit the service file** to set the correct user:
   ```bash
   sudo nano excel-recons.service
   ```
   Replace `%i` with your username (or create a dedicated user)

2. **Copy service file to systemd directory:**
   ```bash
   sudo cp excel-recons.service /etc/systemd/system/
   ```

3. **Reload systemd:**
   ```bash
   sudo systemctl daemon-reload
   ```

4. **Enable and start the service:**
   ```bash
   sudo systemctl enable excel-recons.service
   sudo systemctl start excel-recons.service
   ```

## Service Management

### Start the Service
```bash
sudo systemctl start excel-recons
```

### Stop the Service
```bash
sudo systemctl stop excel-recons
```

### Restart the Service
```bash
sudo systemctl restart excel-recons
```

### Check Service Status
```bash
sudo systemctl status excel-recons
```

### View Logs
```bash
# View recent logs
sudo journalctl -u excel-recons

# Follow logs in real-time
sudo journalctl -u excel-recons -f

# View logs from last hour
sudo journalctl -u excel-recons --since "1 hour ago"
```

### Enable/Disable Auto-start on Boot
```bash
# Enable auto-start
sudo systemctl enable excel-recons

# Disable auto-start
sudo systemctl disable excel-recons
```

## Configuration

### Change Port

Edit `/opt/excel-recons/run_app.sh` and modify:
```bash
export STREAMLIT_SERVER_PORT=8501
```

Then restart the service:
```bash
sudo systemctl restart excel-recons
```

### Change Server Address

Edit `/opt/excel-recons/run_app.sh` and modify:
```bash
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

To bind to localhost only, use:
```bash
export STREAMLIT_SERVER_ADDRESS=127.0.0.1
```

### Firewall Configuration

If you need to access the application from other machines, open the port:

**UFW (Ubuntu/Debian):**
```bash
sudo ufw allow 8501/tcp
```

**firewalld (CentOS/RHEL):**
```bash
sudo firewall-cmd --permanent --add-port=8501/tcp
sudo firewall-cmd --reload
```

## Troubleshooting

### Service Won't Start

1. **Check service status:**
   ```bash
   sudo systemctl status excel-recons
   ```

2. **Check logs for errors:**
   ```bash
   sudo journalctl -u excel-recons -n 50
   ```

3. **Verify virtual environment:**
   ```bash
   ls -la /opt/excel-recons/venv
   ```

4. **Test manually:**
   ```bash
   cd /opt/excel-recons
   source venv/bin/activate
   streamlit run app.py
   ```

### Permission Issues

If you encounter permission errors:

```bash
sudo chown -R $USER:$USER /opt/excel-recons
sudo chmod +x /opt/excel-recons/run_app.sh
```

### Port Already in Use

If port 8501 is already in use:

1. Find the process using the port:
   ```bash
   sudo lsof -i :8501
   ```

2. Either stop that process or change the port in `run_app.sh`

### Virtual Environment Issues

If the virtual environment is corrupted:

```bash
cd /opt/excel-recons
rm -rf venv
./setup_venv.sh
sudo systemctl restart excel-recons
```

## Security Considerations

1. **Create a dedicated user** (recommended):
   ```bash
   sudo useradd -r -s /bin/false excel-recons
   sudo chown -R excel-recons:excel-recons /opt/excel-recons
   ```
   Then update the service file to use `excel-recons` user.

2. **Firewall rules**: Only allow access from trusted networks.

3. **Reverse proxy**: Consider using nginx as a reverse proxy with SSL/TLS.

4. **File upload limits**: Streamlit has default upload limits. Adjust if needed in the app.

## Updating the Application

1. **Stop the service:**
   ```bash
   sudo systemctl stop excel-recons
   ```

2. **Update files:**
   ```bash
   cp app.py recons.py /opt/excel-recons/
   ```

3. **Update dependencies (if needed):**
   ```bash
   cd /opt/excel-recons
   source venv/bin/activate
   pip install -r requirements.txt --upgrade
   ```

4. **Start the service:**
   ```bash
   sudo systemctl start excel-recons
   ```

## Uninstallation

1. **Stop and disable the service:**
   ```bash
   sudo systemctl stop excel-recons
   sudo systemctl disable excel-recons
   ```

2. **Remove the service file:**
   ```bash
   sudo rm /etc/systemd/system/excel-recons.service
   sudo systemctl daemon-reload
   ```

3. **Remove application directory (optional):**
   ```bash
   sudo rm -rf /opt/excel-recons
   ```

## Accessing the Application

Once deployed, access the application at:
- Local: `http://localhost:8501`
- Network: `http://<server-ip>:8501`

Replace `<server-ip>` with your server's IP address.

