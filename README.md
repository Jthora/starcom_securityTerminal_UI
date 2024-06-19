
# Starcom Security System

## Description
This project is designed to create a security system for the Starcom facility using Raspberry Pi devices and USB cameras. The system aggregates camera feeds from multiple Raspberry Pis and displays them on a central touch screen.

## Setup Instructions

### Clone the Repository
Navigate to your home directory or your preferred directory and clone the repository:
```sh
cd ~
git clone <repository-url> starcom_security
cd starcom_security
```

### Run the Setup Script
Make sure the setup script is executable and then run it:
```sh
chmod +x setup.sh
./setup.sh
```

### Activate the Virtual Environment
Each time you want to run your application, activate the virtual environment:
```sh
source venv/bin/activate
```

### Run the Application
After activating the virtual environment, run your application:
```sh
python src/main.py
```

## Folder Structure

- **assets/**: Contains static files like images.
  - **images/**: Stores image assets like the background image for the UI.
- **config/**: Contains configuration files for Motion.
  - **motion/**: Stores individual configuration files for each camera connected to the Raspberry Pis.
- **src/**: Contains source code for the application.
  - **main.py**: The main entry point for the Kivy application.
  - **camera_feed.py**: Contains code related to fetching and processing camera feeds.
  - **utils.py**: Contains utility functions that can be reused across the application.
- **logs/**: Stores log files for the application and individual cameras.
- **README.md**: Project documentation.
- **requirements.txt**: Lists the Python dependencies required for the project.
- **setup.sh**: A shell script to set up the environment, install dependencies, and configure the system.

## Motion Configuration

Make sure each Raspberry Pi with a camera is configured properly with Motion. Example configuration files are provided in the `config/motion` directory. Copy them to `/etc/motion/` on each respective Raspberry Pi and adjust the settings if needed.

## Notes

- Ensure all Raspberry Pi computers are on the same local network and can communicate with each other.
- Assign static IP addresses to each Raspberry Pi for consistent access.
- Test each camera feed individually by accessing the stream URL in a web browser (`http://<IP>:<Port>`).
- This setup ensures that all necessary software is pre-installed and configured to work offline, creating a robust and functional security interface for Starcom.
