 #include <DHT.h>
#include <DHT_U.h>
#include "DHT.h"

#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321
DHT dht(DHTPIN, DHTTYPE);


#include <LiquidCrystal_I2C.h>
#include <Wire.h>


void setup() {
 
  LiquidCrystal_I2C lcd(0x3F, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);
  lcd.begin(20, 4);
  lcd.clear();
 
 
  pinMode(A0, INPUT);
  pinMode(LED_BUILTIN, OUTPUT); //to test if arduino runs without uploading code from ide
  Serial.begin(9600);
  Serial.println(F("running Arduino_code_1 (fast blinker)"));
  dht.begin();
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(2000);
  digitalWrite(LED_BUILTIN, LOW); 
  delay(2000);

  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)){ 
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  {
  int Moisture = analogRead(A0);
  
  float a;
  a = 690;
  float b;
  b = 100;
  float Moisture_Percent;
  Moisture_Percent = b-((Moisture/a)*b);
  
  Serial.print("SMOS: ");
  Serial.print(Moisture_Percent);

  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(F(", AHUM: "));
  Serial.print(h);
  
  Serial.print(F(", ATEMP: "));
  Serial.print(hic);
  Serial.print(F("C "));

  Serial.println(F(""));

  
  LiquidCrystal_I2C lcd(0x3F, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);
  lcd.begin(20, 4);
  lcd.clear();
  
  lcd.print("SMOS : ");
  lcd.print(Moisture_Percent);
  
  lcd.setCursor(0, 1);
  lcd.print("AHUM : ");
  lcd.print(h);
  lcd.print(" %");
  
  lcd.setCursor(0, 2);
  lcd.print("ATEMP: ");
  lcd.print(hic);
  lcd.print(" C");
  
  }
}
