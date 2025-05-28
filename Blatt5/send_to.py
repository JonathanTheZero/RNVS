from random import random
from socket import htons
import sys
from typing import Any


def send_to(bytes_data: bytes, addr_tup: tuple[str, int]) -> None:
    address, dst_port = addr_tup
    # address_bytes: int = htons(bytes(address))
    address_bytes = address.encode("UTF-8")
    destination_port: int = htons(dst_port)
    source_port: int = htons(int(random() * 65000))  # emulate or something, idk
    length: int = htons(len(bytes_data) + 8)
    checksum: int = build_checksum(length, destination_port, source_port)

    PDU: dict[str, Any] = {
        "length": length,
        "destination_port": destination_port,
        "source_port": source_port,
        "checksum": checksum,
        "bytes_data": bytes_data,
    }
    route_packet(address_bytes, PDU)


# Just as an example for show - multiply with some prime numbers or something
def build_checksum(length: int, destination_port: int, source_port: int) -> int:
    return 13 * length + 7 * destination_port + 31 * source_port


def route_packet(addr: bytes, data: Any):
    print("[ROUTING PACKAGE]")
    print("Address:", (addr).decode("UTF-8"))
    print("Raw data:", data)


if __name__ == "__main__":
    msg = bytes([0x48, 0x65, 0x6C, 0x6C, 0x6F])
    recipient = ("192.168.1.135", 6243)
    send_to(msg, recipient)
