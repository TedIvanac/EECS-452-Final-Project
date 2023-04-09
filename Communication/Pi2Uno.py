import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1.0)

try:
    while True:
        # Send a message to Arduino
        message = "0,50.1" # string message
        # message = str(message)
        ser.write(message.encode('utf-8', errors='ignore')) # convert string to bytes and send over serial communication
        time.sleep(1)
       
        # Read and print what's in the Arduino serial monitor
        if ser.in_waiting > 0: # Check if there's any data available in the serial buffer
            arduino_data = ser.readline().decode('utf-8', errors='ignore').rstrip() # Read the data from the serial buffer and decode it
            
            #print(arduino_data)
            direction, distance = map(float, arduino_data.split(','))
            print("Direction: ", direction) # Print the data received from Arduino
            print("Distance: ", distance)
       
        #time.sleep(1) # wait for 1 second before sending next message

except KeyboardInterrupt:
    print("Keyboard Interrupt Detected. Closing serial port...")
    ser.close()