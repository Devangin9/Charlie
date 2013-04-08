
#include <CapacitiveSensor.h>



/*
 * CapitiveSense Library Demo Sketch
 * Paul Badger 2008
 * Uses a high value resistor e.g. 10 megohm between send pin and receive pin
 * Resistor effects sensitivity, experiment with values, 50 kilohm - 50 megohm. Larger resistor values yield larger sensor values.
 * Receive pin is the sensor pin - try different amounts of foil/metal on this pin
 * Best results are obtained if sensor foil and wire is covered with an insulator such as paper or plastic sheet
 */

/*
int commonPort = 34;
int capacitorChin = 44;
int capacitorForehead = 46;
int capacitorRightCheek = 48;
int capacitorLeftCheek = 50;
int capacitorNose = 52;
int eyes1 = 42;
int eyes2 = 40;
int lips = 38;
*/

int commonPort = 19;
int capacitorChin = 15;
int capacitorForehead = 16;
int capacitorRightCheek = 17;
int capacitorLeftCheek = 18;
int capacitorNose = 4;
int eyes = 3;
int lips = 2;


const int capacitorCount =7;
const int capacitorSize = 6;
CapacitiveSensor capacitors[capacitorCount] =      // 10 megohm resistor between pins 4 & 2, pin 2 is sensor pin, add wire, foil
//CapacitiveSensor   cs_4_5 = CapacitiveSensor(24,22);        // 10 megohm resistor between pins 4 & 6, pin 6 is sensor pin, add wire

//CapacitiveSensor   cs_4_8 = CapacitiveSensor(4,8);        // 10 megohm resistor between pins 4 & 8, pin 8 is sensor pin, add wire, 
{ 
  CapacitiveSensor(commonPort, capacitorChin),
  CapacitiveSensor(commonPort, capacitorForehead),
  CapacitiveSensor(commonPort, capacitorRightCheek),
  CapacitiveSensor(commonPort, capacitorLeftCheek),
  CapacitiveSensor(commonPort, capacitorNose),
  CapacitiveSensor(commonPort, lips),
  CapacitiveSensor(commonPort, eyes)
  
  };


int sensorChin = A8;    // select the input pin for the potentiometer
int sensorForeheadRight = A7; 
int sensorForeheadLeft = A15; 
int sensorRightCheek1 = A3; 
int sensorRightCheek2 = A4; 
int sensorLeftCheek1 = A5; 
int sensorLeftCheek2 = A6; 
int sensorNose = A7; 


const int quantumSensorsSize = 3;
int quantumSensors[quantumSensorsSize] = {
  sensorChin,
  sensorForeheadRight/* ,
  sensorForeheadLeft, 
  sensorRightCheek1,
  sensorRightCheek2,
  sensorLeftCheek1,
  sensorLeftCheek2, 
  sensorNose = A7*/
};

//int ledPin = 13;      // select the pin for the LED
//int sensorValue = 0;  // variable to store the value coming from the sensor





void setup()                    
{

  for(int i = 0 ; i < capacitorSize; i ++ ){
    capacitors[i].set_CS_AutocaL_Millis(0xFFFFFFFF);     // turn off autocalibrate on channel 1 - just as an example
  }
  Serial.begin(9600);

  // declare the ledPin as an OUTPUT:
  // pinMode(ledPin, OUTPUT);  

}

void loop()                    
{
  long start = millis();
  long totalCounts[capacitorSize];
  for(int i = 0 ; i < capacitorSize; i++){
    totalCounts[i] =  capacitors[i].capacitiveSensor(30);
  }

  //long total2 =  cs_4_5.capacitiveSensor(30);
  //long total3 =  cs_4_8.capacitiveSensor(30);

  //Serial.print(millis() - start);        // check on performance in milliseconds
  //Serial.print("\t");                    // tab character for debug windown spacing

  for(int i = 0 ; i < capacitorSize; i++){
    Serial.print( i);
    Serial.print( " :: ");
    Serial.print(totalCounts[i]);
    Serial.print( "\t" );                  // print sensor output 1
  }
  // Serial.print("\n");
  /// Serial.print(total2);                  // print sensor output 2
  // Serial.print("\t");
  //Serial.println(total3);                // print sensor output 3

  //delay(10);                             // arbitrary delay to limit data to serial port 


    int quantumSensorValue[quantumSensorsSize];
  // read the value from the sensor
  for(int i = 0 ; i < quantumSensorsSize; i++){
    quantumSensorValue[i] = analogRead(quantumSensors[i]);
  }
  //sensorValue = analogRead(sensorPin);   

  for(int i = 0 ; i < quantumSensorsSize; i++){
    Serial.print( i);
    Serial.print( " --- ");
    Serial.print(quantumSensorValue[i]);
    Serial.print( "\t" );                  // print sensor output 1
  }

  //Serial.print(sensorValue);
  Serial.print("\n");

  // turn the ledPin on
  //digitalWrite(ledPin, HIGH);  
  // stop the program for <sensorValue> milliseconds:
  //delay(sensorValue);          
  // turn the ledPin off:        
  //digitalWrite(ledPin, LOW);   
  // stop the program for for <sensorValue> milliseconds:
  //delay(sensorValue); 
}


