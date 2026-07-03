#include <ESP32Servo.h>

// ========== MOTOR PINS ==========
int m1 = 26;
int m2 = 27;
int power = 25;

// ========== SERVO ==========
Servo myservo;
int servoPin = 16;


void setup() {
  Serial.begin(115200);

  pinMode(m1, OUTPUT);
  pinMode(m2, OUTPUT);
  pinMode(power, OUTPUT);

  myservo.attach(servoPin);


  Serial.println("ESP32 ready");
}

void loop() {

  if (Serial.available()>0) {

    int angle = Serial.parseInt();

    angle = constrain(angle, 0, 180);
    myservo.write(angle);
      // Serial.println(angle);
    // if (angle == 48) {
    //   myservo.write(angle);
    //   delay(650);
    // }
    move_motor(255, 1);
  }
}

void move_motor(int speed, int direction) {
  analogWrite(power, speed);

  if (direction == 0) {
    digitalWrite(m1,LOW);
    digitalWrite(m2,LOW);
  }
  else if (direction == 1) { // counter clockwise
    digitalWrite(m1,HIGH);
    digitalWrite(m2,LOW);
  }
  else if (direction == 2) { // clockwise
    digitalWrite(m1,LOW);
    digitalWrite(m2,HIGH);
  }
}