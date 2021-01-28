import socket
import time
import errno
import sys
import fcntl, os
import signal
import sys

# def signal_handler(signal, frame):
#     print("aaaa")
#   #sys.exit(0)
#
# signal.signal(signal.SIGINT, signal_handler)


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 1234        # The port used by the server

GET_PUBLISHERS_LIST_CMD = '4'
SUBSCRIBE_TO_PUBLISHER_CMD = '5'
START_RECEPTION_CMD = '6'
i=0
NAME = ''
frame = '\0' * 64
#list_of_publishers = ['czujnik1', 'czujnik2', 'czujnik3']
list_of_publishers = []


def read_message():
    while True:
        try:
            msg = s.recv(64)
        except socket.error as e:
            err = e.args[0]

            if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                time.sleep(1)
                #print('No data available')
                continue
            else:
                # a "real" error occurred
                print(e)
                sys.exit(1)
        else:
            return msg

# def parse_data(msg, command):
#     if command == GET_PUBLISHERS_LIST_CMD:


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    fcntl.fcntl(s, fcntl.F_SETFL, os.O_NONBLOCK)


    while True:

        #try:
        # Choose command to execute
        command = input("What do you want to do?\n"
                        " 4 - get all publishers\n"
                        " 5 - subscribe to publisher\n"
                        " 6 - start reception\n")

        if command == SUBSCRIBE_TO_PUBLISHER_CMD:
            publisher = input("Provide name of publisher\n")
            if publisher not in list_of_publishers:
                print("Invalid publisher. Try again.")
                continue
            #data = command + publisher + frame[len(publisher)+len(command):]
            data = str(len(publisher) + len(command)) + '\n\n' + command + publisher

        else:
            data = '1' + '\n\n' + command



        #command = "4"

        s.send(str.encode(data))
        if command == SUBSCRIBE_TO_PUBLISHER_CMD:
            continue
        #time.sleep(10)

        while True:
            try:
                size_chars = []
                frame_size = 0
                final_msg = b""
                size = 0
                no_of_new_line = 0
                while(True):
                    if size == 0:
                        msg = s.recv(1)
                    else:
                        msg = s.recv(size)
                    frame_size += len(msg)
                    final_msg += msg
                    print("Received packet of %d length" % len(msg))
                    if len(msg) == 0:
                        print("closing socket")
                        s.close()
                        exit(0)


                    if size == 0:

                        size_chars.append(msg)

                        if msg[0] == 10:
                            no_of_new_line += 1
                            if no_of_new_line == 2:
                                size = int("".join([chr(char_size[0]) for char_size in size_chars]))
                                header_length = no_of_new_line + len(size_chars) - 2 # /n/n + 5

                        continue

                    #else:



                        #
                        # try:
                        #
                        #     for i, msg_byte in enumerate(msg):
                        #
                        #
                        #         print(msg[i], msg[i + 1])
                        #         if msg[i] == 10 and msg[i + 1] == 10:
                        #             print("end")
                        #             header_length = i + 2  # +2 for \n\n
                        #             break
                        #         size_chars.append(msg_byte)
                        #
                        #     size = int("".join([chr(char_size) for char_size in size_chars]))
                        # except IndexError:
                        #     continue


                    #get size of data



                    if frame_size == size + header_length:
                        print("All data received.")
                        break
                msg = final_msg[header_length:]

            except socket.error as e:
                err = e.args[0]

                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    time.sleep(1)
                    #print('No data available')
                    continue
                else:
                    # a "real" error occurred
                    print(e)
                    sys.exit(1)
            else:

                if command == GET_PUBLISHERS_LIST_CMD:

                    list_of_publishers = [name.decode("utf-8") for name in msg.split(b'\n')[:-1]]
                    print(list_of_publishers)
                    break

                if command == SUBSCRIBE_TO_PUBLISHER_CMD:
                    break

                if command == START_RECEPTION_CMD:

                    print("Message no.%d received from publisher: %s" % (i, msg))
                    i+=1
                    time.sleep(0.3)

            # got a message, do something :)


        # except KeyboardInterrupt:
        #     print("ctrl+c")
        #     continue
        # s.send(bytes.fromhex('02' + format(12344, 'x')))

        # Get list of publishers
        #s.send(str.encode("%s%s" % (GET_PUBLISHERS_LIST_CMD, frame[1:])))
        #frame = "{}{}".format(GET_PUBLISHERS_LIST_CMD, NAME)



        #numStr = "".ljust(5, '0')

        # name_length = s.recv(8)[0]
        #
        # name = s.recv(name_length)
        #
        # a=1
        #name = s.recv(64)
        #time.sleep(10)

    #print('Received', repr(name))
