void setup() { 
 //Initialize serial and wait for port to open:
  Serial.begin(9600); 
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }
  
  // prints title with ending line break 
  Serial.print("AT");
  delay(1000);
  Serial.print("AT");
  delay(1000);
  Serial.print("AT");
  delay(1000);
  Serial.print("AT+BAUD8"); 
} 

void loop()
{
}
