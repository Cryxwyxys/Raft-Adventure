#include <Wire.h>
#include <Joystick.h>

const uint8_t MPU_ADDR = 0x68;

Joystick_ Joystick(JOYSTICK_DEFAULT_REPORT_ID, JOYSTICK_TYPE_JOYSTICK,
                   1, 0,                       // 1 button, 0 hat switches
                   true, true, false, false, false, false,
                   false, false, false, false, false);

bool writeReg(uint8_t reg, uint8_t val) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  Wire.write(val);
  return Wire.endTransmission() == 0;
}

// Wake up and configure the sensor, returns true on success
bool initMPU() {
  if (!writeReg(0x6B, 0x00)) return false;     // PWR_MGMT_1: wake up
  delay(100);
  return writeReg(0x1C, 0x10)                  // accelerometer range +-8 g
      && writeReg(0x1A, 0x04);                 // low-pass filter 21 Hz
}

// Read one 16-bit value (high byte first)
int16_t read16() {
  int16_t hi = Wire.read();
  int16_t lo = Wire.read();
  return (int16_t)((hi << 8) | lo);
}

// Read X and Y acceleration in m/s^2
bool readAccel(float &ax, float &ay) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);                            // ACCEL_XOUT_H
  if (Wire.endTransmission(false) != 0) return false;
  if (Wire.requestFrom(MPU_ADDR, (uint8_t)4, (uint8_t)true) != 4) return false;

  int16_t rawX = read16();
  int16_t rawY = read16();

  ax = rawX / 4096.0 * 9.80665;                // +-8 g = 4096 LSB per g
  ay = rawY / 4096.0 * 9.80665;
  return true;
}

void setup() {
  // Start the joystick first so the PC detects the device immediately
  Joystick.setXAxisRange(-127, 127);
  Joystick.setYAxisRange(-127, 127);
  Joystick.begin();

  Wire.begin();
  delay(500);                                  // give the sensor time to power up

  // Retry until the sensor responds
  while (!initMPU()) {
    delay(200);
  }
}

void loop() {
  float ax, ay;

  // If the sensor stops responding, configure it again
  if (!readAccel(ax, ay)) {
    initMPU();
    return;
  }

  Joystick.setXAxis(constrain((int)( ay * 20.0), -127, 127));
  Joystick.setYAxis(constrain((int)( ax * 20.0), -127, 127));

  delay(20);
}