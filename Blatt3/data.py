def sendto(bytes: bytes, addr_tuple: tuple[str, int]) -> None:
    msg_str: str = bytes.decode("utf-8")
    addr_str: str = f"{addr_tuple[0]}:{addr_tuple[1]}"
    # imagine the actually sending happens here...
    print(f'Successfully sent "{msg_str}" to "{addr_str}"')


if __name__ == "__main__":
    msg: bytes = bytes([0x48, 0x65, 0x6C, 0x6C, 0x6F])
    recipient: tuple[str, int] = ("192.168.1.135", 6243)
    sendto(msg, recipient)
