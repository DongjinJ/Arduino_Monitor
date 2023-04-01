#include <monitor_Packet.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  packet tx_data;
  uint16_t data_0 = analogRead(A0);
  tx_data = Encoding_Packet(3, 0, data_0);
  for (int i = 0; i < 4; i++) {
    Serial.write(tx_data.Byte[i]);
    delay(1);
  }

  uint16_t data_1 = analogRead(A1);
  tx_data = Encoding_Packet(3, 1, data_1);
  for (int i = 0; i < 4; i++) {
    Serial.write(tx_data.Byte[i]);
    delay(1);
  }
  
  uint16_t data_2 = analogRead(A2);
  tx_data = Encoding_Packet(3, 2, data_2);
  for (int i = 0; i < 4; i++) {
    Serial.write(tx_data.Byte[i]);
    delay(1);
  }

  delay(100);
}
