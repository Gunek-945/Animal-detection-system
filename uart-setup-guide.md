# UART Communication Setup Guide for Orin Nano

This guide provides detailed instructions for setting up UART communication between an NVIDIA Orin Nano and an ESP32 module for wild boar detection. The system uses YOLOv8 for detection and communicates with the ESP32 to control various deterrent devices through UART.

## System Overview

When the system detects a wild boar using the YOLOv8 model running on the Orin Nano, it sends JSON messages via UART to an ESP32 module. The ESP32 then controls three deterrent mechanisms:
- LED warning lights
- Ultrasonic speakers
- Spraying system

## Prerequisites

Before beginning the setup, ensure you have:
- NVIDIA Orin Nano (fully assembled)
- ESP32 development board
- USB-C power supply for Orin Nano
- Jumper wires for connections
- VSCode installed on your computer
- Internet connection for downloading required packages

## Initial Setup

### Setting Up the Orin Nano

First, update your system and install necessary packages:

```bash
# Update system packages
sudo apt update && sudo apt upgrade

# Install required development tools
sudo apt install python3-pip python3-venv
```

### Creating a Python Environment

Create and configure a dedicated Python virtual environment:

```bash
# Create new virtual environment
python3 -m venv ~/wildboar_env

# Activate the environment
source ~/wildboar_env/bin/activate

# Clone the project repository
git clone https://github.com/Gunek-945/Animal-detection-system.git
cd Animal-detection-system

# Install project dependencies
pip install -r requirements.txt
```

## UART Configuration

### Configuring UART on Orin Nano

Set up the UART port permissions and install necessary tools:

```bash
# Add user to dialout group for serial port access
sudo usermod -a -G dialout $USER

# Set UART port permissions
sudo chmod 666 /dev/ttyTHS0

# Install serial communication tools
sudo apt install minicom tio
```

### ESP32 Setup in VSCode

1. Install Arduino extension in VSCode
2. Configure ESP32 board support:
   - Open Command Palette (Ctrl+Shift+P)
   - Select "Arduino: Board Manager"
   - Add URL: `https://dl.espressif.com/dl/package_esp32_index.json`
   - Install ESP32 board package

3. Configure board settings:
   - Board: "ESP32 Dev Module"
   - Upload Speed: 115200
   - CPU Frequency: 240MHz
   - Flash Frequency: 80MHz
   - Flash Mode: QIO
   - Flash Size: 4MB
   - Partition Scheme: Default

## Physical Connections

Connect the Orin Nano and ESP32 using the following pin configuration:

```
Orin Nano          ESP32
UART_1_TX (Pin 8) → RX (Pin 17)
UART_1_RX (Pin 10) → TX (Pin 16)
GND              → GND
```

## Testing UART Communication

Create a test script (`test_uart.py`) to verify the UART connection:

```python
import serial
import json
import time

def test_uart_connection():
    # Configure serial port for Orin Nano
    uart = serial.Serial(
        port='/dev/ttyTHS0',  # Orin Nano's UART port
        baudrate=115200,
        timeout=1
    )
    
    # Create test message following project JSON format
    test_message = {
        "Alarm Message": {
            "Detection Zone ID": "A",
            "Status": {
                "LED": True,
                "ULT": True,
                "BDS": True
            }
        }
    }
    
    try:
        # Send JSON message
        uart.write(json.dumps(test_message).encode())
        print("Test message sent")
        
        # Wait for and read response
        time.sleep(1)
        if uart.in_waiting:
            response = uart.readline().decode().strip()
            print(f"Received response: {response}")
        
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        uart.close()

if __name__ == "__main__":
    test_uart_connection()
```

## ESP32 LED Indicators

When properly connected, the ESP32 will display the following LED states:

- Red LED: Power indicator (constant when powered)
- Blue LED: Deterrent LED (automatically turns off after 10 seconds)
- White LED: Ultrasound speaker indicator (automatically turns off after 20 seconds)
- Yellow LED: Spraying system indicator (turns off when commanded)

## Running the Detection System

To run the complete wild boar detection system:

```bash
# Switch to JSON branch
git checkout JSON

# Navigate to inferencing directory
cd Inferencing

# Run the detection script
python inferencing.py
```

## Monitoring and Troubleshooting

### Monitoring UART Communication

Use minicom to monitor UART traffic:

```bash
minicom -D /dev/ttyTHS0 -b 115200
```

Or use tio for a simpler interface:

```bash
tio /dev/ttyTHS0 -b 115200
```

### Common Issues and Solutions

1. UART Port Not Responding
   ```bash
   # Check port detection
   ls -l /dev/ttyTHS*
   
   # Check kernel messages
   dmesg | grep tty
   ```

2. JSON Message Issues
   - Verify message format matches exactly:
   ```json
   {"Alarm Message":{"Detection Zone ID":"A","Status":{"LED":true,"ULT":true,"BDS":true}}}
   ```
   - Ensure message is sent as a single line
   - Check for proper UTF-8 encoding

3. Connection Problems
   - Verify physical connections are secure
   - Confirm ground connection is properly established
   - Check baudrate matches on both devices (115200)

## Additional Resources

- [Orin Nano Developer Guide](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit)
- [ESP32 Documentation](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/)
- Project Repository: https://github.com/Gunek-945/Animal-detection-system

For additional help or to report issues, please refer to the project's GitHub repository.