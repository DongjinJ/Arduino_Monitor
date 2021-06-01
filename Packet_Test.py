import Data_Packet as DP
import Arduino_Monitor as AM
import sys

app = AM.QApplication(sys.argv)
ex = AM.ArduinoApp()


rx_data = []
rx_data.append(DP.arduinoData())
rw = 3
id = 6
data = 0xAB
rx_packet = DP.encode_Data(rw, id, data)

print(rx_packet)
if DP.check_Checksum(rx_packet):
    print("Correct Checksum")
else:
    print("Checksum Error!")

DP.decode_Data(rx_data[0], rx_packet)

for i in range(len(rx_data)):
    print("[", i, "]_ID: ", rx_data[i].dataID, " / ", "[", i, "]_Data: ", rx_data[i].data)

sys.exit(app.exec_())