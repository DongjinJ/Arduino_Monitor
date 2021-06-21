/*  Generate Arduino Monitor Packet */

#include <stdint.h>
#include <stdio.h>

typedef union packet_tag{
    uint8_t Byte[4];
    struct{
        uint32_t checksum:8;
        uint32_t data:16;
        uint32_t id:6;
        uint32_t rw:2;
    }R;
}packet;

extern packet Encoding_Packet(uint8_t rw, uint8_t id, uint8_t data);
extern packet Decoding_Packet(uint8_t *rx_packet);
extern uint8_t Create_Checksum(packet noChecksumPacket);
extern uint8_t Check_Checksum(packet ChecksumPacket);