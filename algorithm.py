def transform(data_msb: int, data_lsb: int, sec: list[int]) -> int:
    data = (data_msb << 8) | data_lsb
    result = ((data % sec[0]) * sec[2]) - ((data // sec[0]) * sec[1])
    if result < 0:
        result += (sec[0] * sec[2]) + sec[1]
    return result & 0xFFFF  # asegurar que queda en 16 bits


def compute_response(pin: list[int], chg: list[int]) -> int:
    sec_1 = [0xB2, 0x3F, 0xAA]
    sec_2 = [0xB1, 0x02, 0xAB]

    res_msb = transform(pin[0], pin[1], sec_1) | transform(chg[0], chg[3], sec_2)
    res_lsb = transform(chg[1], chg[2], sec_1) | transform((res_msb >> 8) & 0xFF, res_msb & 0xFF, sec_2)
    return ((res_msb << 16) | res_lsb) & 0xFFFFFFFF  # asegurar que queda en 32 bits


# Ejemplo de uso:
# pin = [0x12, 0x34]
# chg = [0x01, 0x02, 0x03, 0x04]
# respuesta = compute_response(pin, chg)
# print(f"Respuesta: {respuesta:08X}")
