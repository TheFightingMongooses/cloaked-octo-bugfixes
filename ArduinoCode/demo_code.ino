#include <Servo.h>

Servo servo1;
Servo servo2;
Servo motor;
Servo turning;

int sharp1 = 0;
int sharp2 = 1;
int red = 2;
int green = 3;
int blue = 4;

int pos = 0;
int increment = 1;
int drive = 45;

int incomingByte;

void setup(){
  servo1.attach(0);
  servo2.attach(1);
  motor.attach(2);
  turning.attach(3);
  Serial.begin(38400);
}

void setServos(int angle){
  int i;
  // angle should be an angle from 1 to 180
  servo1.write(angle);
  servo2.write(angle);
}

void loop(){
  Serial.print("S1: " + String(analogRead(sharp1), DEC) + "\t");
  Serial.print("S2: " + String(analogRead(sharp2), DEC) + "\t");
  
  Serial.print("R: " + String(analogRead(red), DEC) + "\t");
  Serial.print("G: " + String(analogRead(green), DEC) + "\t");
  Serial.println("B: " + String(analogRead(blue), DEC));
  pos += increment;
  setServos(pos);
  motor.write(40);
  turning.write(drive);
  delay(15);
  if (pos == 180){
    increment = -1;
    drive = 135;
  } else if(pos == 0){
    increment = 1;
    drive = 45;
  }
}
