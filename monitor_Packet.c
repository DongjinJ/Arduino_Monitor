#include "monitor_Packet.h"

packet Encoding_Packet(uint8_t rw, uint8_t id, uint8_t data){
    packet returnPacket;
    returnPacket.R.rw = rw;
    returnPacket.R.id = id;
    returnPacket.R.data = data;
    returnPacket.R.checksum = Create_Checksum(returnPacket);

    return returnPacket;
}

uint8_t Decoding_Packet(packet rx_packet){

}

uint8_t Create_Checksum(packet noChecksumPacket){
    uint8_t checksum;

    checksum = noChecksumPacket.Byte[0] + noChecksumPacket.Byte[1] + noChecksumPacket.Byte[2];
    checksum = ~(checksum) + 1;

    return checksum;
}

uint8_t Check_Checksum(packet ChecksumPacket){

}

int main(){
    int i;
    packet test = Encoding_Packet(2, 3, 123);
    printf("RW: %d\n", test.R.rw);
    printf("ID: %d\n", test.R.id);
    printf("Data: %d\n", test.R.data);
    for(i = 0;i < 4;i++){
        printf("Buf[%d]: %d\n", i, test.Byte[i]);
    }

    return 0;
}