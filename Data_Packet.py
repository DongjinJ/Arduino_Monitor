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
    buf = [0, 0, 0, 0]
    buf[0] = (packet >> 24) & 0xFF
    buf[1] = (packet >> 16) & 0xFF
    buf[2] = (packet >> 8) & 0xFF
    buf[3] = packet & 0xFF

    checksum = buf[0] + buf[1] + buf[2] + buf[3]
    checksum = checksum & 0xFF

    if checksum == 0:
        return True
    else:
        return False

def decode_Data(arduinoData, packet):
    if check_Checksum(packet):
        id = (packet >> 24) & 0x3F
        data = (packet >> 8) & 0x00FFFF
        arduinoData.update_ID(id)
        arduinoData.update_Data(data)
    else:
        pass
    
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