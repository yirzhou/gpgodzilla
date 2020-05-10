# gpgodzilla - Large File Encryption with Line Modification

**gpgodzilla** enables developers and data scientists to encrypt and decrypt large and structured files while modifying them using whatever custom functions/methods they want, in memory. It is specifically designed for de-tokenization + encryption of sensitive data such as account numbers and social insurance numbers, where raw data is not allowed to live on the local storage of the system. 

## Use Case
The files that can be worked with should be structured on a line-by-line basis. For example, each line has some portions that need to be modified in the same way before encryption or after decryption. 

One primary example is for transferring and processing PANs. Provided is a file of customers' PANs that are tokenized. The requirement is to send the encrypted and de-tokenized PANs to the receiver. 

However, because PANs are highly sensitive, the de-tokenized/raw PANs cannot touch the local storage of the system. Hence, de-tokenization and encryption need to happen in system memory.

## Requirements
It is essential to have *GnuPG 2* installed on the system.

## Quick Start
Install via pip:

```pip install gpgodzilla```

## Basic Example
With the file to manipulate on the local storage, define the path to the file and the path to the processed/manipulated file. *The file to process must exist*. 

Define the recipient of the encrypted file and the manipulation method for each line (ex. de-tokenization method that returns the de-tokenized line).

```python
from gpgodzilla import encrypt_large_file, decrypt_large_file

def tokenize_foo(line):
    # The example tokenization
    # replacing each "foo" with "bar" before encryption
    line = line.replace('foo', 'bar')
    return line

def detokenize_bar(line):
    # The example detokenization method
    # replacing each "some_token" with "cipher" before encryption
    line = line.replace('bar', 'foo')
    return line

# The following code demonstrates a simple use case

file_to_encrypt = 'test.txt'  # File to manipulate and encrypt
recipient = 'john.doe@test.com'  # Email of the recipient (GnuPG), which must exist on the system on which the code is running
output_file_encrypt = 'test.pgp'   # path of the encrypted & manipulated file
output_file_decrypt = 'original_test.txt' # path of the decrypted file
encrypt_large_file(recipient, file_to_encrypt, output_file_encrypt, tokenize_foo)

# then, to decrypt the file and detokenize each 'bar' back to 'foo':
decrypt_large_file(output_file_encrypt, output_file_decrypt, detokenize_bar, PASSPHRASE)
```
