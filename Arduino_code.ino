#include <DHT.h>
#include <DHT_U.h>
#include "DHT.h"

#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  pinMode(A0, INPUT);
  pinMode(LED_BUILTIN, OUTPUT); //to test if arduino runs without uploading code from ide
  Serial.begin(9600);
  Serial.println(F("running"));
  dht.begin();
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(2000);
  digitalWrite(LED_BUILTIN, LOW); 
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)){ 
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  {
  int Moisture = analogRead(A0);
  Serial.print("SMOS: ");
  Serial.print(Moisture);

  }
  
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(F(", AHUM: "));
  Serial.print(h);
  
  Serial.print(F(", ATEMP: "));
  Serial.print(hic);
  Serial.print(F("C "));

  Serial.println(F(""));
  
}
