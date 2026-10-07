#include <Wire.h>
#include <Joystick.h>

const uint8_t MPU_ADDR = 0x68;

Joystick_ Joystick(JOYSTICK_DEFAULT_REPORT_ID, JOYSTICK_TYPE_JOYSTICK,
                   1, 0,                       // 1 Button, 0 Hat-Switches
                   true, true, false, false, false, false,
                   false, false, false, false, false);

void writeReg(uint8_t reg, uint8_t val) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  Wire.write(val);
  Wire.endTransmission();
}

// Liest Beschleunigung in m/s^2
bool readAccel(float &ax, float &ay) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);                            // ACCEL_XOUT_H
  if (Wire.endTransmission(false) != 0) return false;
  if (Wire.requestFrom(MPU_ADDR, (uint8_t)4, (uint8_t)true) != 4) return false;

  int16_t rawX = Wire.read() << 8 | Wire.read();
  int16_t rawY = Wire.read() << 8 | Wire.read();

  // ±8 g -> 4096 LSB pro g
  ax = rawX / 4096.0 * 9.80665;
  ay = rawY / 4096.0 * 9.80665;
  return true;
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);

  Wire.begin();

  // Sensor aufwecken
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);                            // PWR_MGMT_1
  Wire.write(0);

  writeReg(0x1C, 0x10);                        // Beschleunigung ±8 g
  writeReg(0x1A, 0x04);                        // Filter 21 Hz

  Joystick.setXAxisRange(-127, 127);
  Joystick.setYAxisRange(-127, 127);
  Joystick.begin();
}

void loop() {
  float ax, ay;
  if (!readAccel(ax, ay)) return;

  int joystickX = constrain((int)(-ay * 20.0), -127, 127);
  int joystickY = constrain((int)( ax * 20.0), -127, 127);

  Joystick.setXAxis(joystickX);
  Joystick.setYAxis(joystickY);

  delay(20);
}