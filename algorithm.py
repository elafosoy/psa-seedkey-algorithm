import math

def transform(data, sec):
    """
    Transforma un valor de datos utilizando un conjunto de secretos. 
    """ 
    if data > 32767: 
        data = data - 65536   
     
    quotient = int(data / sec[0]) 
    remainder = int(math.fmod(data, sec[0]))
    
    term1 = remainder * sec[2]
    term2 = quotient * sec[1]
    
    result = term1 - term2 
    modulus = (sec[0] * sec[2]) + sec[1]
    if result < 0:
        result += modulus
        
    return result & 0xFFFF

def get_key(seed_txt, app_key_txt="0000"):
    """
    Genera una clave a partir de un texto semilla y una clave de aplicación.
    """
    seed = [seed_txt[i:i+2] for i in range(0, len(seed_txt), 2)]
    app_key = [app_key_txt[i:i+2] for i in range(0, len(app_key_txt), 2)]
 
    sec_1 = [0xB2, 0x3F, 0xAA]   
    sec_2 = [0xB1, 0x02, 0xAB]  
 
    val1 = transform(int(app_key[0] + app_key[1], 16), sec_1)
    val2 = transform(int(seed[0] + seed[3], 16), sec_2)
    res_msb = val1 | val2
    
    val3 = transform(int(seed[1] + seed[2], 16), sec_1)
    val4 = transform(res_msb, sec_2)
    res_lsb = val3 | val4
     
    res = (res_msb << 16) | res_lsb
    return f'{res:08X}'

# --- Ejemplo de uso --- 
print(get_key("00000001", "ADDA"))
