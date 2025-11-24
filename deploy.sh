#!/bin/bash

# Deployment script for Excel Reconciliation Tool
# This script sets up the application and systemd service

set -e

# Configuration
APP_DIR="/opt/excel-recons"
SERVICE_FILE="excel-recons.service"
CURRENT_USER=$(whoami)

echo "=========================================="
echo "Excel Reconciliation Tool - Deployment"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ This script must be run as root (use sudo)"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "Step 1: Creating application directory..."
mkdir -p "$APP_DIR"

echo "Step 2: Copying application files..."
# Get the directory where deploy.sh is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cp "$SCRIPT_DIR/app.py" "$SCRIPT_DIR/recons.py" "$SCRIPT_DIR/requirements.txt" "$APP_DIR/"
cp "$SCRIPT_DIR/run_app.sh" "$SCRIPT_DIR/setup_venv.sh" "$APP_DIR/"
chown -R $CURRENT_USER:$CURRENT_USER "$APP_DIR"

echo "Step 3: Making scripts executable..."
chmod +x "$APP_DIR/run_app.sh"
chmod +x "$APP_DIR/setup_venv.sh"

echo "Step 4: Setting up virtual environment..."
cd "$APP_DIR"
sudo -u $CURRENT_USER bash "$APP_DIR/setup_venv.sh" || {
    # If setup_venv.sh doesn't work, do it manually
    echo "Setting up venv manually..."
    sudo -u $CURRENT_USER python3 -m venv "$APP_DIR/venv"
    sudo -u $CURRENT_USER "$APP_DIR/venv/bin/pip" install --upgrade pip
    sudo -u $CURRENT_USER "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"
}

echo "Step 5: Installing systemd service..."
# Update service file with correct user
sed "s/%i/$CURRENT_USER/g" "$SCRIPT_DIR/$SERVICE_FILE" > "/tmp/${SERVICE_FILE}"
cp "/tmp/${SERVICE_FILE}" "/etc/systemd/system/${SERVICE_FILE}"
rm "/tmp/${SERVICE_FILE}"

# Reload systemd
systemctl daemon-reload

echo "Step 6: Enabling service..."
systemctl enable excel-recons.service

echo ""
echo "=========================================="
echo "✅ Deployment complete!"
echo "=========================================="
echo ""
echo "Service installed as: excel-recons.service"
echo "Application directory: $APP_DIR"
echo ""
echo "To start the service:"
echo "  sudo systemctl start excel-recons"
echo ""
echo "To stop the service:"
echo "  sudo systemctl stop excel-recons"
echo ""
echo "To check service status:"
echo "  sudo systemctl status excel-recons"
echo ""
echo "To view logs:"
echo "  sudo journalctl -u excel-recons -f"
echo ""
echo "The application will be available at:"
echo "  http://localhost:8501"
echo "  http://<server-ip>:8501"
echo ""

