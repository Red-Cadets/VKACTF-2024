import click
import os
import cli.utils as utils
from cli.options import *
from Crypto.Cipher import AES
from datetime import datetime
from cli.constants import *
import random

def gen_key(length):
    return os.urandom(length)

def gen_iv(length):
    return os.urandom(length)

def make_shared_secret(IV, share, encrypted):

    part = IV
    part += int.to_bytes(share[0], 3, byteorder='big')
    part += int.to_bytes(share[1], 66, byteorder='big')
    return part + encrypted


@click.command(help='Split file into shared secrets') 
@with_number_option
@with_minimum_option
@with_file_option
@with_dir_option
@with_params_option
@with_key_option
@with_iv_option
def split(minimum, number, file, dir, params, key, iv):

    if not os.path.exists(file):
        return f'{file} does not exist'

    if not os.path.exists(dir):
        return f'{dir} does not exist'

    if minimum > number:
        return f'{minimum} > {number}'
    

    with open(file, 'rb') as f:
        plain = f.read()

    if key != None:
        key = int.to_bytes(int(open(key, 'r').read()), 32, byteorder='big')
    else:
        key = gen_key(32)
        f_name = f'key_{random.randint(0, 10000)}.txt'
        with open(os.path.join(KEYS_DIR, f_name), 'w') as f:
            f.write(str(int.from_bytes(key, byteorder='big')))
        print("Your key saved in: " + os.path.join(KEYS_DIR, f_name))

    if iv != None:
        iv = int.to_bytes(int(open(iv, 'r').read()), 16, byteorder='big')
    else:
        iv = gen_iv(16)
        f_name = f'iv_{random.randint(0, 10000)}.txt'
        with open(os.path.join(IVS_DIR, f_name), 'w') as f:
            f.write(str(int.from_bytes(iv, byteorder='big')))
        print("Your IV saved in: " + os.path.join(KEYS_DIR, f_name))

    cipher = AES.new(key, AES.MODE_OFB, iv)
    ciphertext = cipher.encrypt(plain)

    if params == None:
        poly = None
    else:
        with open(os.path.join(params), 'r') as f:
            params_list = f.read()
        poly = [int(param) for param in params_list[1:-1].split(',')]
    
    FSS = utils.FSS(minimum, number)
    shares, poly = FSS.split(int.from_bytes(key, byteorder='big'), poly)
    
    f_name = f'poly_{random.randint(0, 10000)}.txt'
    with open(os.path.join(PARAMS_DIR, f_name), 'wb') as f:
        f.write(str(poly).encode('utf-8'))
    print("Your polynomial saved in: " + os.path.join(PARAMS_DIR, f_name))
    
    current_datetime = datetime.now()
    folder_name = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(os.path.join(dir, folder_name), exist_ok=True)

    for i in range(len(shares)):

        share = shares[i]
        s = make_shared_secret(iv, share, ciphertext)
        with open(os.path.join(dir, folder_name, f'Part_{i+1}_of_{number}.txt'), 'wb') as f:
            f.write(s)

    print('Done! You can find your files in ' + os.path.join(dir, folder_name))