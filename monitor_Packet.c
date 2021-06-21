#include "monitor_Packet.h"

packet Encoding_Packet(uint8_t rw, uint8_t id, uint8_t data){
    packet returnPacket;
    returnPacket.R.rw = rw;
    returnPacket.R.id = id;
    returnPacket.R.data = data;
    returnPacket.R.checksum = Create_Checksum(returnPacket);

    return returnPacket;
}

packet Decoding_Packet(uint8_t *rx_buf){
    packet rx_packet;

    rx_packet.Byte[0] = rx_buf[0];
    rx_packet.Byte[1] = rx_buf[1];
    rx_packet.Byte[2] = rx_buf[2];
    rx_packet.Byte[3] = rx_buf[3];
    printf("RW: %d\n", rx_packet.R.rw);
    printf("ID: %d\n", rx_packet.R.id);
    printf("Data: %d\n", rx_packet.R.data);
    if(Check_Checksum(rx_packet) == 1){
        return rx_packet;
    }
    else{
        rx_packet.Byte[3] = 0xC5;
        rx_packet.Byte[2] = 0xC5;
        rx_packet.Byte[1] = 0xBA;
        rx_packet.Byte[0] = 0xAD;
        return rx_packet;
    }
}

uint8_t Create_Checksum(packet noChecksumPacket){
    uint8_t checksum;

    checksum = noChecksumPacket.Byte[3] + noChecksumPacket.Byte[2] + noChecksumPacket.Byte[1];
    checksum = ~(checksum) + 1;

    return checksum;
}

uint8_t Check_Checksum(packet ChecksumPacket){
    uint8_t result;

    result = ChecksumPacket.Byte[3] + ChecksumPacket.Byte[2] + ChecksumPacket.Byte[1] + ChecksumPacket.Byte[0];

    if (result == 0)
        return 1;
    else
        return 0;
}

int main(){
    int i;
    uint8_t rx_buf[4];
    packet test = Encoding_Packet(2, 3, 123);
    packet result;

    printf("RW: %d\n", test.R.rw);
    printf("ID: %d\n", test.R.id);
    printf("Data: %d\n", test.R.data);
    for(i = 0;i < 4;i++){
        printf("Buf[%d]: %x\n", i, test.Byte[i]);
    }
    rx_buf[0] = test.Byte[0];
    rx_buf[1] = test.Byte[1];
    rx_buf[2] = test.Byte[2];
    rx_buf[3] = test.Byte[3];

    for(i = 0;i < 4;i++){
        printf("Buf[%d]: %x\n", i, rx_buf[i]);
    }
    result = Decoding_Packet(rx_buf);
    printf("result: 0x%x\n", result.R);
    for(i = 0;i < 4;i++){
        printf("Buf[%d]: %x\n", i, result.Byte[i]);
    }
    return 0;
}