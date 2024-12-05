def getSize(file) -> int:
    Bytes = 0
    with open(file, "rb") as f:
        for byte in f.read():
            Bytes += 1
    return Bytes