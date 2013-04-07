#include <Servo.h> 

// Pin 13 has an LED connected on most Arduino boards.
// give it a name:
int led = 13;

Servo myServo1;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
Servo myServo2;  

boolean clockwise1 = true;
boolean clockwise2 = true;

boolean moveServoNextPosition(Servo servo, boolean clockwise){
  int pos = servo.read();
  if(clockwise){
     pos = pos + 1; // goes from 0 degrees to 180 degrees 
                                      // in steps of 1 degre
     servo.write(pos);              // tell servo to go to position in variable 'pos' 
     delay(5);                       // waits 15ms for the servo to reach the position 
     if(pos == 180)
        clockwise = false;
  }else{
    pos = pos - 1;     // goes from 180 degrees to 0 degrees 
    servo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(5);                       // waits 15ms for the servo to reach the position 
    if(pos == 0)
      clockwise = true;
  }    
  return clockwise;
}


//............................................................................
void BSP_ledOff(void) {
    digitalWrite(led, LOW);    // turn the LED off by making the voltage LOW
    clockwise1 = moveServoNextPosition(myServo1, clockwise1);
}


//............................................................................
void BSP_ledOn(void) {
   digitalWrite(led, HIGH);   // turn the LED on (HIGH is the voltage level)
    clockwise2 = moveServoNextPosition(myServo2, clockwise2);
}


//............................................................................
void setup() {
   pinMode(led, OUTPUT); 
    myServo1.attach(9);  // attaches the servo on pin 9 to the servo object 
    myServo2.attach(10); 
    // Serial.begin(9600);     // opens serial port, sets data rate to 9600 bps
}

void loop(){
  BSP_ledOn();
  BSP_ledOff();
}
