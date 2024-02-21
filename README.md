
---

# Fish Tank Feeder Project

This project is an automated fish tank feeder system that utilizes a Raspberry Pi. It features a stepper motor for dispensing fish food, an ultrasonic sensor for measuring the food's depth in the dispenser, a pump for water circulation or filtration, controllable lighting (lamp) for the fish tank, buttons for manual control, and an LCD screen for displaying system status.

## Features

- **Food Dispensing**: Uses a stepper motor to drop food into the fish tank.
- **Food Level Monitoring**: An ultrasonic sensor measures the depth of the food within the dispenser to monitor remaining food levels.
- **Light Control**: Manages a lamp for the fish tank, allowing for a light cycle that simulates day and night.
- **Manual Control**: Buttons are provided for manual override of automatic functions.
- **Status Display**: An LCD screen displays the current status, including the food level and lamp status.

## Hardware Requirements

- Raspberry Pi (any model that supports GPIO pins)
- Stepper motor for dispensing food
- Ultrasonic sensor (e.g., HC-SR04) for measuring food level
- Relay module for lamp control
- Buttons for manual input
- LCD screen (e.g., Adafruit PCD8544) for status display
- Resistors, capacitors, and wiring for connections

## Software Requirements

- Raspbian OS or any compatible Raspberry Pi OS
- Python 3.x
- Required Python libraries:
  - RPi.GPIO
  - adafruit-circuitpython-pcd8544
  - PIL (Python Imaging Library)

## Setup and Installation

### Setup

![Setup](./Setup.png)


1. **Hardware Setup**:
   - Connect the stepper motor, ultrasonic sensor, relay module, buttons, and LCD screen to the Raspberry Pi according to the GPIO pin configuration specified in the script.
   - Ensure proper power supply to the components, especially the stepper motor and lamp.

2. **Software Setup**:
   - Install the latest version of Raspbian OS on your Raspberry Pi.
   - Clone this repository to your Raspberry Pi.
   - Install the required Python libraries by running `pip install -r requirements.txt` in the project directory.

## Usage

To run the fish tank feeder system, navigate to the project directory and execute:

```bash
python fish_tank_feeder.py
```

- Use the buttons to manually toggle the lamp and dispense food if needed.
- The LCD screen will display the current food level and lamp status.
- The system automatically dispenses food at scheduled intervals and monitors the food level.

## Configuration

- Edit the `fish_tank_feeder.py` script to adjust GPIO pin assignments, feeding schedule, and other parameters.



