#include "monitor_Packet.h"

packet tx_data;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  uint16_t data = analogRead(A0);
  tx_data = Encoding_Packet(3, 0, data);

  uint8_t errCode = false;
  if(tx_data.Byte[0] == 0xAD){
    if(tx_data.Byte[1] == 0xBA){
      if(tx_data.Byte[2] == 0xC5){
        if(tx_data.Byte[3] == 0xC5){
          errCode = true;
        }
      }
    }
  }

  if (errCode == true){
    
  }
  else {
    for (int i = 0; i < 4; i++) {
      Serial.write(tx_data.Byte[i]);
    }
  }

}
