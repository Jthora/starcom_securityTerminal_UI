#!/bin/bash

echo "Updating package list and installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip motion python3-venv

echo "Creating Python virtual environment..."
python3 -m venv venv

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Configuring Motion..."
sudo cp config/motion/motion_cam1.conf /etc/motion/motion_cam1.conf
sudo cp config/motion/motion_cam2.conf /etc/motion/motion_cam2.conf
sudo cp config/motion/motion_cam3.conf /etc/motion/motion_cam3.conf
sudo cp config/motion/motion_cam4.conf /etc/motion/motion_cam4.conf

echo "Restarting Motion service..."
sudo service motion restart

echo "Creating log directories..."
mkdir -p logs

echo "Setup completed successfully."

echo "To activate the virtual environment, run:"
echo "source venv/bin/activate"