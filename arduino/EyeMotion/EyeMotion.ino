// Sweep
// by BARRAGAN <http://barraganstudio.com> 
// This example code is in the public domain.


#include <Servo.h> 
#include <math.h>


boolean isConsiderTopDown = true;
boolean isConsiderLeftRight = true;

void moveEyeBalls2Ways(int startAngleLeftRight,int endAngleLeftRight,int middleAngleLeftRight,int startAngleTopDown,int endAngleTopDown );
void moveEyeBalls(int angleLeftRight, int angleTopDown);
void moveEyeBallsCircle(int radiusLeftRight,int radiusTopDown, int angleStep);



 
Servo eyeServoLeftRight;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
Servo eyeServoTopDown;                
 
int pos = 0;    // variable to store the servo position 


int startAngleTopDown = 0; //down
int angleRangeTopDown = 85;
int endAngleTopDown = startAngleTopDown + angleRangeTopDown; //up
int startAngleLeftRight = 70;
int angleRangeLeftRight = 150;
int endAngleLeftRight = startAngleLeftRight + angleRangeLeftRight;
 
void setup() 
{   
  // attaches the servo on pins to the servo object 
  eyeServoLeftRight.attach(12);  
  eyeServoTopDown.attach(13);
    Serial.begin(9600);
} 
 
 
void loop() 
{ 
   Serial.print(startAngleLeftRight);
   
   //put the eyes in the middle
   int middleAngleLeftRight = (startAngleLeftRight + endAngleLeftRight)/2;
   
  // eyeServoTopDown.write(100);
   moveEyeBalls2Ways( startAngleLeftRight, endAngleLeftRight, middleAngleLeftRight, startAngleTopDown, endAngleTopDown );
   //moveEyeBallsCircle(angleRangeLeftRight/2, 10);
} 


void moveEyeBalls2Ways(int startAngleLeftRight,int endAngleLeftRight,int middleAngleLeftRight,int startAngleTopDown,int endAngleTopDown ){
   int delayTime = 5;  
  if(isConsiderLeftRight){
     //left write motion
    for(pos = startAngleLeftRight; pos < endAngleLeftRight; pos += 1)  // goes from 0 degrees to 180 degrees 
    {                                  // in steps of 1 degree 
      eyeServoLeftRight.write(pos);              // tell servo to go to position in variable 'pos' 
      Serial.write(pos);
      delay(delayTime);                       // waits 15ms for the servo to reach the position 
    } 
    for(pos = endAngleLeftRight; pos>=startAngleLeftRight; pos-=1)     // goes from 180 degrees to 0 degrees 
    {                                
      eyeServoLeftRight.write(pos);              // tell servo to go to position in variable 'pos' 
      delay(delayTime);                       // waits 15ms for the servo to reach the position 
    } 
    eyeServoTopDown.write(middleAngleLeftRight);
  }
 
  if(isConsiderTopDown) {
      //top down motion
     for(pos = startAngleTopDown; pos < endAngleTopDown; pos += 1)  // goes from 0 degrees to 180 degrees 
    {                                  // in steps of 1 degree 
      eyeServoTopDown.write(pos);              // tell servo to go to position in variable 'pos' 
      delay(delayTime);                       // waits 15ms for the servo to reach the position 
    } 
    for(pos = endAngleTopDown; pos>=startAngleTopDown; pos-=1)     // goes from 180 degrees to 0 degrees 
    {                                
      eyeServoTopDown.write(pos);              // tell servo to go to position in variable 'pos' 
      delay(delayTime);                       // waits 15ms for the servo to reach the position 
    } 
  }
  
}

 
 
  void moveEyeBalls(int angleLeftRight, int angleTopDown){
   
    int currentLeftRightAngle = eyeServoLeftRight.read();
    int delayTime = 5;
    //move left or right
    if(angleLeftRight > currentLeftRightAngle){
       for(pos = currentLeftRightAngle; pos < angleLeftRight; pos += 1)  // goes from 0 degrees to 180 degrees 
      {                                  // in steps of 1 degree 
        eyeServoLeftRight.write(pos);              // tell servo to go to position in variable 'pos' 
        delay(delayTime);                       // waits 15ms for the servo to reach the position 
      } 
    }else{
      for(pos = currentLeftRightAngle; pos >= angleLeftRight; pos -= 1)  // goes from 0 degrees to 180 degrees 
      {                                  // in steps of 1 degree 
        eyeServoLeftRight.write(pos);              // tell servo to go to position in variable 'pos' 
        delay(delayTime);                       // waits 15ms for the servo to reach the position 
      } 
    }
  
  
  int currentTopDown = eyeServoTopDown.read();
  
  //move top or down
  if(angleTopDown > currentTopDown){
     for(pos = currentTopDown; pos < angleTopDown; pos += 1)  // goes from 0 degrees to 180 degrees 
    {                                  // in steps of 1 degree 
      eyeServoTopDown.write(pos);              // tell servo to go to position in variable 'pos' 
      delay(delayTime);                       // waits 15ms for the servo to reach the position 
    }
  }
  else{
     for(pos = currentTopDown; pos>=angleTopDown; pos-=1)     // goes from 180 degrees to 0 degrees 
    {                                
      eyeServoTopDown.write(pos);              // tell servo to go to position in variable 'pos' 
      delay(delayTime);                       // waits 15ms for the servo to reach the position 
    } 
  }
  }
  
  
  void moveEyeBallsCircle(int radiusLeftRight,int radiusTopDown, int angleStep){
    
    //calculate centers
    int centerLeftRight = startAngleLeftRight + angleRangeLeftRight/2;
    int centerTopDown = startAngleTopDown + angleRangeTopDown/2;
   
    
    for(int i = 0 ; i < 360; i += angleStep){
      int angleLeftRight = centerLeftRight + radiusLeftRight * cos(i);
      int angleTopDown = centerTopDown + radiusTopDown * sin(i);
    }
    
  }


