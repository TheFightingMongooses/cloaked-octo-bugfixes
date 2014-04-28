#include <Servo.h>

Servo armServo;
Servo motor;
Servo turning;

int sharpRight = 0;
int sharpLeft = 1;
int sharpTop = 2;
int red = 3;
int green = 4;
int blue = 5;

int drive = 45;

void setup(){
  armServo.attach(0);
  motor.attach(12);
  turning.attach(13);
  Serial.begin(38400);
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
  if ((int)analogRead(sharpRight) > 500 || (int)analogRead(sharpLeft) > 500){
    setVelocity(40);
    if ((int) analogRead(sharpLeft) < 500){
      setDirection(35);
    } else if ((int) analogRead(sharpRight) < 500) {
      setDirection(55);
    } else{
      setDirection(45);
    // This will TOTALLY need to change when we actually get experimental stuff
    }
  } else {
    setDirection(45);
  }
}

void foreMidBrain(){
  // Basically, this just tells the robit how to respond to whatever the python code
  // is saying. The way it's set up, it should just keep on trucking unless it's
  // told otherwise.
  armServo.write(45);
  setVelocity(40);
  setDirection(135);
}

void loop(){
  Serial.println(
    String(analogRead(sharpLeft), DEC) + "\t" + 
    String(analogRead(sharpRight), DEC) + "\t" +
    String(analogRead(sharpTop), DEC) + "\t"+
    String(analogRead(red), DEC) + "\t" +
    String(analogRead(green), DEC) + "\t" +
    String(analogRead(blue), DEC)
  );
  armServo.write(95);
  motor.write(1500);
  turning.write(1000);
  delay(15);
  //hindBrain();
}
