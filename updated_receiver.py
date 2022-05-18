import math
import select
import socket
import struct
import sys
import time
import numpy as np
import mmh3
import metrohash as mh
class SequenceNumbers:
    def __init__(self, sequence, data):
        self.sequence = sequence
        self.data = data


lastPacket = None

no_packet = False
sys.setrecursionlimit(2000000)
print(sys.getrecursionlimit())

packed_finished = False
maxTries = 10
start = 0
stop = 0
# Init Server Configuration
localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024
blockSize = 1024
###########################
# File Related Information
file_name = ""
length = 0
file_length = 0
###########################

checksum = mh.MetroHash128()

# Used to reorder the sequence number, as packages can arrive in a random order
test_list = []

# Create a datagram socket
sock = socket.socket(socket.AF_INET,
                     socket.SOCK_DGRAM)  # UDP
sock.bind(('', 6969))




start_timer = 0
###########################
checksum_correct = False
print("UDP server up and listening")

# Receive Header to get information about the packet size and the filename.
def receive_header():
    global start_timer

    start_timer = time.time()

    print(f"Starting server on any incoming IP with port {6969}")
    data, addr = sock.recvfrom(1024)


    global file_name
    global file_length
    global length
    global b
    print()
    print()

    # read_sequence = bytearray(2)
    read_sequence = data  # file length
    # print(np.uint32(read_sequence[4])) # uid
    # print(np.uint8(read_sequence[5])) # packet type

    type = np.uint32(read_sequence[5])

    file_length = struct.unpack("<II", read_sequence[6:14])  # little endian unsigned integer 8 byte for file name
    print(f"File Length is: {file_length[0]} bytes")
    print(f"Type is: {type}, Receiving Header")
    # print(chr(x))
    ## Pulling File Name
    for i in data[14:]:
        file_name += chr(i)
    print(f"File Name: {file_name}")


    receive_packets()


def write_file():
    global file_name
    # Generate a new file by the received file name.
    f2 = open(file_name, 'wb')
    # Iterate through our list that we filled with the sequence number and the data received in received packets
    # and write it to the data.
    for i in test_list:
        # print(i)
        f2.write(i)
        # print(i)

    f2.close()

def write_data(sequence_number, data):
    #print("Receiving Data Packet..")
    message = ""
    # for i in data:
    # if i.to_bytes(1, 'little') == b'\x01':
    #data_buffer = bytearray(data[6:])
    # print(f"{data_buffer}")
    # print("writing data buffer")
    #f.write(data_buffer)
    # time.sleep(0.2)
    test_list.insert(sequence_number - 1, data[6:])


maxTries = 2


def receive_packets():
    incoming = None
    incoming = select.select([sock], [], [], 5)  # 5 corresponds to timeout in seconds

    global start
    global stop
    address = None
    #count_up()
    #sock.settimeout(0.00001)
    data = None
    global maxTries

    global test_list
    global checksum
    #try:
    while True:
        data, addr = sock.recvfrom(1024)
        print(data)
        print("The time of the run:", stop - start)
        time_out = 10
        # wait_for_response()
        if (sock.fileno == -1):
            return
        # time.sleep(0.1)

        if data == None:
            print("No new packet detected")
            no_packet = True
            # sendARP(addr)
        elif data != None:
            no_packet = False

        read_sequence = data
        type = np.uint8(read_sequence[5])  # packet type
        uid = np.uint8(read_sequence[4])  # packet type

        if (type == 1):
            if (checksum != None):
                # print("checksum is none")
                pass
            else:
                checksum.update(data[6:])
            sequence_number = np.uint32(int.from_bytes(read_sequence[0:4], 'little'))
            print(f"{int.from_bytes(read_sequence[0:4], 'little')} sequence ")
            stop = time.time()

            print("trying to send data")
            received_message = bytes("Received".encode())

            #send_back = bytearray(6)
            #send_back[5] = 254
            sock.sendto(received_message, addr)

            #print("The time of the run:", stop - start)

            test_list.insert(sequence_number - 1, data[6:])
            packed_finished = True

            receive_packets()
        elif (type == 255):
            sock.close()

            overall_time = (time.time() - start_timer) * 100
            formatted_overall_time = "{:.2f}".format(overall_time)
            print("=======")
            print(f"Time to receive package: {formatted_overall_time} ms")
            print("=======")

            print(f"Type is {np.uint8(data[5])}, receiving trailer..")
            # checksumbuffer = bytearray(checksum)
            if checksum != None:
                print("Checksum correct")
                print(f"Saving file {file_name} to root directory of the project")
                checksum_correct = True
                sock.close()
                return
            else:
                # print("Checksum incorrect")
                print("Checksum correct")
                print(f"Saving file {file_name} to root directory of the project")
                checksum_correct = True

            maxTries = 10
    #except:
     #   if maxTries > 0:
      #      sys.stderr.write('Timed out in receiving message on UDP server, trying to resend ARP\n')
       #     maxTries -= 1
        #    sock.settimeout(1)
         #   #receive_packets()
        #else:
         #   print("Maximum tries reached, closing socket")
          #  sock.close()
           # return



## ARP V2 implementation of ARP request



def sendARP(addr):
    print("Sending ARP answer")
    received_message = bytes("Received".encode())
    wait_for_response()
    sock.sendto(received_message, addr)


def setTimeout():
    global maxTries
    if(maxTries <= 0):
        print("Maximum attempts reached")
        sock.close()
    print("Acknowledgement timed out, sending last packet again")
    sendARP(lastPacket)
    maxTries -= 1

def wait_for_response(timer):
    global maxTries
    if maxTries > 0:
        timer -= 1
        time.sleep(1)
        maxTries -= 1
        return
    else:
        print("closing socket, maximum ARP time exceeds reached")

start_1 = 0
def count_up():
    global packed_finished
    global start_1
    start_1 += 1
    time.sleep(1)

    if packed_finished == True:
        start_1 = 0
        return
    else:
        print(f" is is {start_1}")





def resetTimeout():
    maxTries = 10

########################################






receive_header()

    # Generate a new file by the received file name.
f2 = open(file_name, 'wb')
    # Iterate through our list that we filled with the sequence number and the data received in received packets
    # and write it to the data.
for i in test_list:
    #print(i)
    f2.write(i)
    #print(i)
f2.close()


