#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include <Mouse.h>

Adafruit_MPU6050 mpu;

void setup(void) {
  Serial.begin(115200);
  while (!Serial) {
    yield(); // Required for Leonardo to wait for Serial Monitor
  }

  // Give the sensor time to power up and stabilize
  delay(500); 

  Serial.println("Initializing MPU6050...");

  // Try to initialize the sensor with explicit I2C address 0x68
  if (!mpu.begin(0x68)) {
    Serial.println("Failed to find MPU6050 chip, check wiring!");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // Initialize the USB Mouse control
  Mouse.begin();
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Map acceleration values to mouse movement 
  // (Multiplying or dividing adjusts the sensitivity/speed)
  int moveX = (int)(-a.acceleration.y * 1.2); // Tilt left/right moves mouse horizontally
  int moveY = (int)(a.acceleration.x * 0.0);  // Tilt forward/backward moves mouse vertically

  // Move the mouse if there is a change
  if (moveX != 0 || moveY != 0) {
    Mouse.move(moveX, moveY, 0);
  }

  // Short delay to keep the movement smooth and controllable
  delay(20);
}