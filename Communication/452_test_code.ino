void setup() {
  Serial.begin(115200); // Start serial communication at 115200 baud rate
}

void loop() {
  if (Serial.available() > 0) { // Check if there's any data available in the serial buffer
    String message = Serial.readString(); // Read the message from the serial buffer
    //Serial.println(message);
    int directions;
    float distance;
    char separator = ',';

    directions = message.substring(0, message.indexOf(separator)).toInt();
    //Serial.print(directions);
    distance = message.substring(message.indexOf(separator) + 1).toFloat();
    //Serial.println(distance);
    
    Serial.print(directions); // Print the received message on the serial monitor
    Serial.write(',');

    Serial.println(distance);
    //Serial.write('\n');
  }
}
