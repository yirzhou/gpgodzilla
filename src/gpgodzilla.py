import logging
import subprocess
from multiprocessing import Process

logging.basicConfig(format='gpgeternal: %(asctime)s - %(message)s', level=logging.DEBUG)

def load_public_key(key_path):
    try:
        output = subprocess.check_output(['gpg2', '--import', key_path])
        (output)
    except Exception as e:
        logging.error('GPG Error: importing public key at %s.' % key_path)
        raise ValueError(str(e))

def load_private_key(key_path):
    try:
        subprocess.check_output(['gpg2', '--allow-secret-key-import', '--import', key_path])
    except Exception as e:
        logging.error('GPG Error: importing private key at %s.' % key_path)
        raise ValueError(str(e))

def __encrypt_with_subprocess(encryptProcess, line):
    try:
        encryptProcess.stdin.write(line)
        encryptProcess.stdin.flush()
    except Exception as e:
        logging.error(str(e))
        raise ValueError(str(e))
    
def __get_subprocess_for_encrypt(recipient, output_file):
    try:
        output_stream = open(output_file, 'ab+')
        encryptProcess = subprocess.Popen(['gpg2', '--allow-multiple-messages', f'--recipient={recipient}', '--always-trust', '--encrypt'], stdin=subprocess.PIPE, stdout=output_stream)
        return encryptProcess, output_stream
    except Exception as e:
        logging.error(str(e))
        raise ValueError(str(e))

def __get_subprocess_for_decrypt(incoming_file, passphrase=None):
    try:
        input_file = open(incoming_file, 'r')
        decryptProcess = None
        if not passphrase:
            decryptProcess = subprocess.Popen(['gpg2', '--allow-multiple-messages', '--always-trust', '--decrypt'], stdin=input_file, stdout=subprocess.PIPE)
        else: 
            decryptProcess = subprocess.Popen(['gpg2', f'--passphrase={passphrase}', '--pinentry-mode=loopback', '--allow-multiple-messages', '--always-trust', '--decrypt'], \
                                            stdin=input_file, stdout=subprocess.PIPE)
        return decryptProcess
    except Exception as e:
        logging.error(str(e))
        raise ValueError(str(e))

def __decrypt_and_manipulate_line(file_to_decrypt, output_file, manipulation_function, passphrase=None):
    """
    The flow is as follows:
    Create one subprocess for decryption.
    Open the large file for decryption, decrypt it line by line in bytes,
    manipulate each line and write it to the output file stream.

    - recipient: the recipient of the encrypted message.
    - file_to_encrypt: file path of the file to manipulate and encrypt.
    - output_file: file path of the file to output.
    - manipulation_function: custom function to manipulate each line before encryption. 
    - passphrase: passphrase of secret key if any.
    """
    decryptProcess = __get_subprocess_for_decrypt(file_to_decrypt, passphrase)
    with open(output_file, 'a+') as output_stream:
        for line in iter(decryptProcess.stdout.readline, b''):
            line = manipulation_function(line.decode("utf-8"))
            output_stream.write(line)

def __encrypt_and_manipulate_line(recipient, file_to_encrypt, output_file, manipulation_function):
    """
    The flow is as follows:
    Create one subprocess for encryption.
    Open the large file for encryption, read it line by line in bytes,
    manipulate each line, encrypt each manipulated line and write it to 
    the output file stream.

    - recipient: the recipient of the encrypted message.
    - file_to_encrypt: file path of the file to manipulate and encrypt.
    - output_file: file path of the file to output.
    - manipulation_function: custom function to manipulate each line before encryption. 
    """
    encryptProcess, output_stream = __get_subprocess_for_encrypt(recipient, output_file)
    with open(file_to_encrypt, 'r') as input_file:
        for line in input_file:
            manipulated_line = manipulation_function(line)
            manipulated_line = bytes(manipulated_line, 'utf-8')
            __encrypt_with_subprocess(encryptProcess, manipulated_line)
    output_stream.close()

def encrypt_large_file(recipient, file_to_encrypt, output_file, manipulation_function):
    """Encrypts large file after manipulating each line with custom function.

    - recipient: the recipient of the encrypted message.
    - file_to_encrypt: file path of the file to manipulate and encrypt.
    - output_file: file path of the file to output.
    - manipulation_function: custom function to manipulate each line before encryption. 
    """
    logging.info('Start encrypting large file: %s', str(file_to_encrypt))
    encryption_task = None
    try:
        encryption_task = Process(target=__encrypt_and_manipulate_line, args=(recipient, file_to_encrypt, output_file, manipulation_function,))
        encryption_task.start()
        encryption_task.join()
    except Exception as e:
        logging.fatal(str(e))
        raise ValueError(str(e))
    if encryption_task.exitcode != 0:
        logging.error('Encryption of large file failed: %s', 'exitcode!=0')
        raise ValueError('Encryption of large file failed.')
    logging.info('Encryption status: %s' , 'Success')

def decrypt_large_file(file_to_decrypt, output_file, manipulation_function, passphrase=None):
    """Manipulates each line with custom function after decryption of each line.

    - file_to_decrypt: file path of the file to manipulate and decrypt.
    - output_file: file path of the file to output.
    - manipulation_function: custom function to manipulate each line before encryption. 
    """
    logging.info('Start decrypting large file: %s', str(file_to_decrypt))
    decryption_task = None
    try:
        decryption_task = Process(target=__decrypt_and_manipulate_line, args=(file_to_decrypt, output_file, manipulation_function, passphrase,))
        decryption_task.start()
        decryption_task.join()
    except Exception as e:
        logging.fatal(str(e))
        raise ValueError(str(e))
    if decryption_task.exitcode != 0:
        logging.error('Decryption of large file failed.')
        raise ValueError('Decryption of large file failed.')
    logging.info('Decryption status: %s' , 'Success')
