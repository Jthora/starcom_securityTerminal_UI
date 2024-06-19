#!/bin/bash

# Update package list and install dependencies
echo "Updating package list and installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3 python3-pip motion

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Configure Motion for each camera
echo "Configuring Motion..."
sudo cp config/motion/motion_cam1.conf /etc/motion/motion_cam1.conf
sudo cp config/motion/motion_cam2.conf /etc/motion/motion_cam2.conf
sudo cp config/motion/motion_cam3.conf /etc/motion/motion_cam3.conf
sudo cp config/motion/motion_cam4.conf /etc/motion/motion_cam4.conf

# Restart Motion service to apply new configurations
echo "Restarting Motion service..."
sudo service motion restart

# Create directories for logs if they don't exist
echo "Creating log directories..."
mkdir -p logs
touch logs/app.log logs/camera1.log logs/camera2.log logs/camera3.log logs/camera4.log

# Print completion message
echo "Setup completed successfully."