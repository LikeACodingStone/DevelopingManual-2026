"""Build a BACnet/IP Who-Is packet. Sends only with explicit --target."""
import argparse
import ipaddress
import socket
import struct


def who_is():
    # Version 1 NPDU, global broadcast destination, hop count 255;
    # unconfirmed-request APDU, Who-Is service 8, no instance limits.
    npdu_apdu = bytes.fromhex('01 20 ff ff 00 ff 10 08')
    return struct.pack('!BBH', 0x81, 0x0b, 4 + len(npdu_apdu)) + npdu_apdu


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', type=ipaddress.IPv4Address)
    args = parser.parse_args()
    packet = who_is()
    print('Who-Is:', packet.hex(' '))
    if args.target:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.bind(('', 0))
            sock.settimeout(2)
            sock.sendto(packet, (str(args.target), 47808))
            try:
                while True:
                    reply, peer = sock.recvfrom(65535)
                    print(peer, reply.hex(' '))
            except socket.timeout:
                pass

if __name__ == '__main__':
    main()
