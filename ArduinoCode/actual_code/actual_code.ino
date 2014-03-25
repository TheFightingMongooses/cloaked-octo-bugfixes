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

int drive = 45;

String inputString = "";
boolean stringComplete = false;

void setup(){
  servo1.attach(0);
  servo2.attach(1);
  motor.attach(2);
  turning.attach(3);
  Serial.begin(38400);
  inputString.reserve(100);
}

void serialEvent(){
  while (Serial.available()){
    char inChar = (char)Serial.read();
    inputString += inChar;
    if (inChar == '\n'){
      stringComplete = true;
    }
  }
}

void setVelocity(int velocity){
  motor.write(velocity);
}

void setDirection(int angle){
  turning.write(angle);
  drive = angle;
}

void hindBrain(){
  // Right now this should basically be, if the sharp sensors say you're too close
  // then stop and pivot a little bit. This will change depending on how fast our
  // robit is, and which side the IR sensors are on and how we mount the motors.
  if (analogRead(sharp1) > 400 || analogRead(sharp2) > 400){
    setVelocity(0);
    if (analogRead(sharp1) > analogRead(sharp2)){
      setDirection(drive + 5);
    } else {
      setDirection(drive - 5);
    }
    // This will TOTALLY need to change when we actually get experimental stuff
    setVelocity(-1);
    delay(150);
    setVelocity(0);
  }
}

int getNextValue(char delimiter){
  int nextIndex = inputString.indexOf(delimiter);
  int nextValue = inputString.substring(0, nextIndex).toInt();
  inputString = inputString.substring(nextIndex);
  return nextValue;
}

void foreMidBrain(){
  // Basically, this just tells the robit how to respond to whatever the python code
  // is saying. The way it's set up, it should just keep on trucking unless it's
  // told otherwise.
  servo1.write(getNextValue('`'));
  servo2.write(getNextValue('`'));
  setVelocity(getNextValue('`'));
  setDirection(getNextValue('`'));
}

void loop(){
  Serial.println(
    String(analogRead(sharp1), DEC) + "`" + 
    String(analogRead(sharp2), DEC) + "`" +
    String(analogRead(red), DEC) + "`" +
    String(analogRead(green), DEC) + "`" +
    String(analogRead(blue), DEC)
    );
  
  if (stringComplete){
    foreMidBrain();
    inputString = "";
    stringComplete = false;
  }
  
  hindBrain();
}
