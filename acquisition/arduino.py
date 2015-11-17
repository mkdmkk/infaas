import time

__author__ = 'mkk'

import serial

"""
#include <PinChangeInt.h>
#include <eHealth.h>

int cont = 0;

// the setup routine runs once when you press reset:
void setup() {
  Serial.begin(115200);
  eHealth.initPulsioximeter();
  //Attach the inttruptions for using the pulsioximeter.
  PCintPort::attachInterrupt(6, readPulsioximeter, RISING);
}

// the loop routine runs over and over again forever:
void loop() {
  float temperature = eHealth.getTemperature();

  Serial.print("{'temperature': ");
  Serial.print(temperature, 2);
  Serial.println("}");

  delay(200);

  Serial.print("{'pulse': ");
  Serial.print(eHealth.getBPM());
  Serial.println("}");

  delay(200);

  Serial.print("{'spo2': ");
  Serial.print(eHealth.getOxygenSaturation());
  Serial.println("}");

  delay(200);

  float conductance = eHealth.getSkinConductance();
  float resistance = eHealth.getSkinResistance();
  float conductanceVol = eHealth.getSkinConductanceVoltage();
  Serial.print("{'gsr': ");
  Serial.print("{'conductance': ");
    Serial.print(conductance, 2);
  Serial.print("}, ");
    Serial.print("{'resistance': ");
  Serial.print(resistance, 2);
  Serial.print("},");
    Serial.print("{'conductanceVol': ");
  Serial.print(conductanceVol, 4);
  Serial.print("}");

    Serial.println("}");
  // wait for a second
  delay(200);
}

//Include always this code when using the pulsioximeter sensor
//=========================================================================
void readPulsioximeter(){

  cont ++;

  if (cont == 50) { //Get only of one 50 measures to reduce the latency
    eHealth.readPulsioximeter();
    cont = 0;
  }
}

"""

ser = serial.Serial('/dev/tty.usbmodem1d151', 115200)
while True:
    print(ser.readline())
    time.sleep(0.2)
