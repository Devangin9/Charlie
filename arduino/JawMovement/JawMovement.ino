// Sweep
// by BARRAGAN <http://barraganstudio.com> 
// This example code is in the public domain.


#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
 
int pos = 0;    // variable to store the servo position 
 
void setup() 
{ 
  myservo.attach(13);  // attaches the servo on pin 9 to the servo object 
} 
 
 
void loop() 
{ 
  int angle1 = 65;
  int angle2 = 90; //120
  int delayTime = 5;
  const int words = 5;
  int angle1Array[words] = {65, 65, 65, 70, 80};
  int angle2Array[words] = {120, 100, 90, 100, 90};
  int delayTimeArray[words] = {5, 1, 2, 3, 2};
  
  for(int i = 0 ; i <  words; i++){
  for(pos = angle1Array[i]; pos < angle2Array[i]; pos += 1)  // goes from 0 degrees to 180 degrees 
  {                                  // in steps of 1 degree 
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(delayTimeArray[i]);                       // waits 15ms for the servo to reach the position 
  } 
  for(pos = angle2Array[i]; pos>=angle1Array[i]; pos-=1)     // goes from 180 degrees to 0 degrees 
  {                                
    myservo.write(pos);              // tell servo to go to position in variable 'pos' 
    delay(delayTimeArray[i]);                       // waits 15ms for the servo to reach the position 
  } 
  }
} 
