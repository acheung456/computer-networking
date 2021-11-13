from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 1
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet():
    #Fill in start
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.

    # Make the header in a similar way to the ping exercise.
    # Append checksum to the header.
    checksum_val = 0
    id = os.getpid() & 0xffff  # Return the current process i
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, checksum_val, id, 1)
    #header = struct.pack("!HHHHH", ICMP_ECHO_REQUEST, 0, myChecksum, pid, 1)
    data = struct.pack("d", time.time())
    checksum_val = checksum(header + data)


    # Get the right checksum, and put in the header

    if sys.platform == 'darwin':
       checksum_val = htons(checksum_val) & 0xffff
    else:
       checksum_val = htons(checksum_val)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, checksum_val, id, 1)

    # Don’t send the packet yet , just return the final packet in this function.
    #Fill in end

    # So the function ending should look like this

    packet = header + data
    return packet

def get_route(hostname):
    timeLeft = TIMEOUT
    tracelist1 = [] #This is your list to use when iterating through each trace

    for ttl in range(1,MAX_HOPS):
        destAddr = gethostbyname(hostname)
        icmp = getprotobyname("icmp")
        mySocket = socket(AF_INET, SOCK_RAW, icmp)
        mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
        mySocket.settimeout(TIMEOUT)
        try:
            d = build_packet()
            mySocket.sendto(d, (hostname, 0))
            t= time.time()
            startedSelect = time.time()
            whatReady = select.select([mySocket], [], [], timeLeft)
            howLongInSelect = (time.time() - startedSelect)
            if whatReady[0] == []: # Timeout
                tracelist1.append([ttl, "*", "Request timed out."])
            recvPacket, addr = mySocket.recvfrom(1024)
            return tracelist1
            timeReceived = time.time()
            timeLeft = timeLeft - howLongInSelect
            if timeLeft <= 0:
                tracelist1.append([ttl, "*", "Request timed out."])
        except timeout:
            continue

        else:
            #Fill in start
            header = recvPacket[20:28]
            types, code, checksum, packetID, sequence = struct.unpack("bbHHh", header)
            #Fill in end
            try: #try to fetch the hostname
                #Fill in start
                ip_header = struct.unpack('!BBHHHBBH4s4s', recvPacket[:20])
                source_ip = inet_ntoa(ip_header[8])
                dest= gethostbyaddr(source_ip)[0]
                #Fill in end
            except herror:   #if the host does not provide a hostname
                #Fill in start
                dest = "hostname not returnable"
                #Fill in end

            if types == 11:
                bytes = struct.calcsize("d")
                timeSent = struct.unpack("d", recvPacket[28:28 +
                bytes])[0]
                #Fill in start
                tracelist1.append(
                    [
                        "{}".format(ttl),
                        "{}".format((timeReceived-t)*1000),
                        "{}".format(source_ip),
                        "{}".format(dest)
                    ]
                )
                #Fill in end
            elif types == 3:
                bytes = struct.calcsize("d")
                timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                #Fill in start
                tracelist1.append(
                    [
                        "{}".format(ttl),
                        "{}".format((timeReceived-t)*1000),
                        "{}".format(source_ip),
                        "{}".format(dest)
                    ]
                )
                #Fill in end
            elif types == 0:
                bytes = struct.calcsize("d")
                timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                #Fill in start
                #You should add your responses to your lists here and return your list if your destination IP is met
                tracelist1.append(
                    [
                        "{}".format(ttl),
                        "{}".format((timeReceived-timeSent)*1000),
                        "{}".format(source_ip),
                        "{}".format(dest)
                    ]
                )
                return tracelist1
                #Fill in end
            else:
                #Fill in start
                #If there is an exception/error to your if statements, you should append that to your list here
                tracelist1.append("error")
                #Fill in end
                break
        finally:
            mySocket.close()

def _get_route(something):
    return [["boo"]]
