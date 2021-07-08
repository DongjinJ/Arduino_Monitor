class arduinoData:
    def __init__(self):
        self.dataID = 0xFF
        self.data = 0xFF

    def update_ID(self, ID):
        self.dataID = ID
    def update_Data(self, data):
        self.data = data

    def get_ID(self):
        return self.dataID
    def get_Data(self):
        return self.data

def check_Checksum(packet):
    checksum = int.from_bytes(packet[0],"big",signed=False) + int.from_bytes(packet[1],"big",signed=False) + int.from_bytes(packet[2],"big",signed=False) + int.from_bytes(packet[3],"big",signed=False)
    checksum = checksum & 0xFF

    if checksum == 0:
        return True
    else:
        return False

def decode_Data(packet):
    for i in range(4):
        print("[", i, "]", int.from_bytes(packet[i],"big",signed=False))
    if check_Checksum(packet):
        id = int.from_bytes(packet[3],"big",signed=False) & 0x3F
        data = ((int.from_bytes(packet[2],"big",signed=False) << 8) & 0xFF00) | (int.from_bytes(packet[1],"big",signed=False) & 0x00FF)
        return id, data
    else:
        return None, None
    
def create_Checksum(rw, id, data):
    buf = [0, 0, 0, 0]
    buf[0] = ((rw << 6) & 0xC0) | (id & 0x3F)
    buf[1] = (data >> 8) & 0xFF
    buf[2] = (data & 0xFF)
    checksum = buf[0] + buf[1] + buf[2]
    checksum = ~(checksum) + 1

    return checksum

def encode_Data(rw, id, data):
    packet = 0x00000000

    packet |= (rw << 30) & 0xC0000000
    # print("rw: ", hex(packet))
    packet |= (id << 24) & 0x3F000000
    # print("id: ", hex(packet))
    packet |= (data << 8) & 0x00FFFF00
    # print("data: ", hex(packet))
    packet |= (create_Checksum(rw, id, data) & 0xFF)
    # print("Checksum: ", hex(packet))

    return packet