import RPi.GPIO as GPIO
import time
import datetime
import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image, ImageDraw, ImageFont

# Initialize GPIO and SPI
def init_gpio_spi():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # SPI for LCD
    spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
    return spi

# Initialize buttons and outputs
def setup_buttons_outputs():
    # Buttons
    GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Example Button
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Lamp Button

    # Outputs
    GPIO.setup(18, GPIO.OUT)  # Sensor Trigger
    GPIO.setup(21, GPIO.OUT)  # Pump
    GPIO.setup(20, GPIO.OUT)  # Lamp

# Initialize LCD display
def init_lcd(spi):
    dc = digitalio.DigitalInOut(board.D23)
    cs1 = digitalio.DigitalInOut(board.CE1)
    reset = digitalio.DigitalInOut(board.D24)
    display = adafruit_pcd8544.PCD8544(spi, dc, cs1, reset, baudrate=1000000)
    display.bias = 4
    display.contrast = 60
    display.invert = True
    display.fill(0)
    display.show()
    return display

# Draw on display
def draw_on_display(display, text, line_height=10):
    image = Image.new('1', (display.width, display.height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSansBold.ttf", 10)
    draw.rectangle((0, 0, display.width, display.height), outline=255, fill=255)
    
    for i, line in enumerate(text.split('\n')):
        draw.text((1, i * line_height), line, font=font)
    
    display.image(image)
    display.show()

# Measure water depth
def measure_water_depth():
    GPIO.output(18, True)
    time.sleep(0.01)
    GPIO.output(18, False)
    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(17) == 0:
        start_time = time.time()

    while GPIO.input(17) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 17000)
    return distance

# Stepper motor initialization
def setup_stepper_pins():
    control_pins = [26, 19, 13, 6]
    for pin in control_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
    return control_pins

# Stepper motor control
def step_motor(control_pins, steps, direction=1):
    sequence = [
        [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]
    ]
    for _ in range(steps):
        for half_step in range(8):
            for pin in range(4):
                GPIO.output(control_pins[pin], sequence[half_step][pin] if direction == 1 else sequence[7 - half_step][pin])
            time.sleep(0.001)

# Placeholder for pump control logic
def control_pump(active):
    GPIO.output(21, GPIO.HIGH if active else GPIO.LOW)

# Main loop update
def main_loop(display, control_pins):
    lamp_status = False
    # Additional variables for button debouncing
    last_button_press_time = 0

    while True:
        current_time = time.time()
        
        # Lamp control with basic debouncing
        if GPIO.input(4) == GPIO.HIGH and current_time - last_button_press_time > 0.5:
            lamp_status = not lamp_status
            GPIO.output(20, GPIO.HIGH if lamp_status else GPIO.LOW)
            last_button_press_time = current_time

        # Stepper motor control example (adjust based on your application's requirements)
        if GPIO.input(2) == GPIO.HIGH:  # Assuming GPIO 2 is a stepper control button
            step_motor(control_pins, 512, direction=1)  # Example: 512 steps in one direction
            last_button_press_time = current_time
        
        # Example placeholder for pump control based on water depth
        water_depth = measure_water_depth()
        if water_depth > 10:  # Example threshold
            control_pump(True)
        else:
            control_pump(False)

        # Display updates
        display_text = f"Time: {datetime.now().strftime('%H:%M:%S')}\nDepth: {water_depth:.1f} cm\nLamp: {'On' if lamp_status else 'Off'}"
        draw_on_display(display, display_text)
        
        time.sleep(1)  # Main loop delay

if __name__ == "__main__":
    spi = init_gpio_spi()
    setup_buttons_outputs()
    control_pins = setup_stepper_pins()  # Setup stepper motor pins
    display = init_lcd(spi)
    main_loop(display, control_pins)