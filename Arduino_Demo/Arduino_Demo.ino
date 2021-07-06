#include <monitor_Packet.h>

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  packet tx_data;
  uint16_t data = analogRead(A0);
  tx_data = Encoding_Packet(3, 0, data);

  for (int i = 0; i < 4; i++) {
    Serial.write(tx_data.Byte[i]);
    delay(1);
  }
  delay(100);
}
