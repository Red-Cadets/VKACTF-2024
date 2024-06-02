import click
import os
import cli.utils as utils
from cli.options import *
from Crypto.Cipher import AES
from datetime import datetime
from cli.constants import *

@click.command(help='Bind all secrets to file recovery') 
@with_number_option
@with_minimum_option
@with_dir_option
def bind(number, minimum, dir):

    if minimum > number:
        return f'{minimum} > {number}'

    if not os.path.exists(dir):
        return f'{dir} does not exist'

    FSS = utils.FSS(minimum, number)

    files = os.listdir(dir)
    shares = [] 

    for file in files:

        with open(os.path.join(dir, file), 'rb') as f:
            encoded = f.read()

        IV = encoded[:16]
        x = int.from_bytes(encoded[16:19], byteorder='big')
        y = int.from_bytes(encoded[19:85], byteorder='big')
        shares.append((x, y))

        ciphertext = encoded[85:]

    secret = FSS.bind(shares[:minimum])

    key = int.to_bytes(secret, 32, byteorder='big')
    cipher = AES.new(key, AES.MODE_OFB, IV)
    flag = cipher.decrypt(ciphertext)

    filename = f'Secret_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}'

    with open(os.path.join(FILES_DIR, filename), 'wb') as f:
        f.write(flag)

    print(f'Decrypted secret saved to {filename}')
