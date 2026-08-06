POLY = 0xD5


def crc8_byte(value):
    crc = value

    for _ in range(8):
        if crc & 0x80:
            crc = ((crc << 1) & 0xFF) ^ POLY
        else:
            crc = (crc << 1) & 0xFF

    return crc


table = [crc8_byte(i) for i in range(256)]

print("static const uint8_t crc8_table[256] = {")
for row in range(0, 256, 16):
    values = ", ".join(f"0x{v:02X}" for v in table[row:row + 16])
    ending = "," if row < 240 else ""
    print(f"    {values}{ending}")
print("};")