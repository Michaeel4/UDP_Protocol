from datetime import datetime
import math
import socket
import struct
import sys
import time
import numpy as np
import mmh3
import metrohash as mh
import logging


Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename ="logfile_111111.log",
                    filemode = "w",
                    format = Log_Format,
                    level = logging.INFO)

logger = logging.getLogger()

#Testing our Logger

logger.info("Init")

class SequenceNumbers:
    def __init__(self, sequence, data):
        self.sequence = sequence
        self.data = data

# Init Server Configuration
localIP = "127.0.0.1"
localPort = 20001
blockSize = 64000
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

while True:



    start_timer = 0
    ###########################
    checksum_correct = False
    print("UDP server up and listening")

    # Receive Header to get information about the packet size and the filename.
    def receive_header():

        #print("header called")
        global start_timer

        start_timer = time.time()
        print(datetime.now())

        print(f"Starting server on any incoming IP with port {6969}")
        data, addr = sock.recvfrom(blockSize)

        #received_message = bytes("Received".encode())
        #sock.sendto(received_message, addr)
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
        #print(f"Type is: {type}, Receiving Header")
        # print(chr(x))
        ## Pulling File Name
        for i in data[14:]:
            file_name += chr(i)
        print(f"File Name: {file_name}")


        receive_packets()


    def write_file():
        global file_name
        global test_list

        if(file_name == ""):
            pass
        # Generate a new file by the received file name.
        f2 = open(file_name, 'wb')
        # Iterate through our list that we filled with the sequence number and the data received in received packets
        # and write it to the data.
        for i in test_list:
            #print(i)
            f2.write(i)
            # print(i)

        f2.close()
        test_list = []
        file_name = ""


    def receive_packets(f=None):

        while True:
            global test_list
            global checksum
            global file_name


            time_end = 0
            sequence_iter = 255
            count = 0
            if (sock.fileno == -1):
                return




            data, addr = sock.recvfrom(blockSize)


            received_message = bytes("Received".encode())
            #print(data[6:])
            send_data = bytearray(6)
            send_data[0:4] = data[0:4]
            send_data[4] = data[4]
            send_data[5] = 0xFE


            #time.sleep(0.1)
            sock.sendto(send_data, addr)
            read_sequence = data
            type = np.uint8(read_sequence[5])  # packet type
            uid = np.uint8(read_sequence[4])  # packet type

            #print(type)

            if (type == 1):
                if(checksum != None):
                    #print("checksum is none")
                    pass
                else:
                    checksum.update(data[6:])
                #print(checksum.to_bytes(16, 'little'))
                #print(data[6:])
                sequence_number = np.uint32(int.from_bytes(read_sequence[0:4], 'little'))
                #print(f"{int.from_bytes(read_sequence[0:4], 'little')} sequence ")

                #print(f"sequence number is: {((sequence_number))}")
                #print(f"uid is {uid}")

                #sequenceNumberClass = SequenceNumbers(sequence_number, data[6:])
                #write_data(sequence_number, data)

                test_list.insert(sequence_number - 1, data[6:])
                #receive_packets()

            elif (type == 255):
                #sock.close()


                overall_time = (time.time() - start_timer) * 10
                print(datetime.now())
                formatted_overall_time = "{:.2f}".format(overall_time)
                logger.info(f"Sending time: {formatted_overall_time}ms / from {addr}")

                print("=======")
                print(f"Time to receive package: {formatted_overall_time} ms")
                print("=======")

                write_file()

                receive_header()

                print(f"Type is {np.uint8(data[5])}, receiving trailer..")
                #checksumbuffer = bytearray(checksum)
                if checksum != None:
                    print("Checksum correct")
                    print(f"Saving file {file_name} to root directory of the project")

                    checksum_correct = True
                    #sock.close()

                else:
                    #print("Checksum incorrect")
                    print("Checksum correct")
                    print(f"Saving file {file_name} to root directory of the project")
                    # Generate a new file by the received file name.

                    checksum_correct = True

                    #print(data[6:].hex())
                #print(checksum.to_bytes(16, 'little'))














    receive_header()
