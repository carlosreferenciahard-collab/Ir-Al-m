#include <DHT.h>

#define DHTPIN 15
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

const int ldrPin = 34;

void setup() {
  Serial.begin(115200);
  dht.begin();
  pinMode(ldrPin, INPUT);
}

void loop() {
  float umidade = dht.readHumidity();
  float temperatura = dht.readTemperature();
  int ldrValue = analogRead(ldrPin);
  
  int luminosidadePercent = map(ldrValue, 0, 4095, 0, 100);

  Serial.println("=========================================");
  Serial.print(" Temperatura do Ar: ");
  Serial.print(temperatura);
  Serial.println(" C");
  Serial.print(" Umidade do Ar: ");
  Serial.print(umidade);
  Serial.println(" %");
  Serial.print(" Luminosidade: ");
  Serial.print(luminosidadePercent);
  Serial.println(" %");
  Serial.println("=========================================");

  delay(2000);
}