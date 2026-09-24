#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <Joystick.h>

Adafruit_MPU6050 mpu;

Joystick_ Joystick(
  JOYSTICK_DEFAULT_REPORT_ID,
  JOYSTICK_TYPE_JOYSTICK,

  1,      // 1 tlačítko
  0,      // 0 hat switchů

  true,   // X
  true,   // Y
  false,  // Z
  false,  // Rx
  false,  // Ry
  false,  // Rz
  false,  // Rudder
  false,  // Throttle
  false,  // Accelerator
  false,  // Brake
  false   // Steering
);

void setup() {

  Serial.begin(115200);

  delay(500);

  // MPU6050
  if (!mpu.begin(0x68)) {
    while (1) {
      delay(10);
    }
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // Joystick
  Joystick.setXAxisRange(-127, 127);
  Joystick.setYAxisRange(-127, 127);

  Joystick.begin();
}

void loop() {

  sensors_event_t a, g, temp;

  mpu.getEvent(&a, &g, &temp);

  // MPU6050 → joystick
  int joystickX = (int)(-a.acceleration.y * 20.0);
  int joystickY = (int)(a.acceleration.x * 20.0);

  // Omezit rozsah
  joystickX = constrain(joystickX, -127, 127);
  joystickY = constrain(joystickY, -127, 127);

  Joystick.setXAxis(joystickX);
  Joystick.setYAxis(joystickY);

  delay(20);
}