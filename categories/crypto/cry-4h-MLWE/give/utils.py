def bytes_to_bits(input_bytes):

    bit_list = []
    for byte in input_bytes:
        bits = format(byte, '08b')[::-1]  
        bit_list.extend(map(int, bits))  
    return bit_list
    
def bitstring_to_bytes(s):

    return bytes([int(s[i:i+8][::-1], 2) for i in range(0, len(s), 8)])
    
def round_up(x):

    return round(x + 0.000001)
    
def xor_bytes(a, b):

    return bytes(a^b for a,b in zip(a,b))