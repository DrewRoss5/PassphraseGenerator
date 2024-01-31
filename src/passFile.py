import os
import json
import secrets
from Crypto.Cipher import AES 
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

class PassFile:
    # these define postions for data in the file header
    KEY_SALT_END = 16
    CHECK_SALT_END = 32
    IV_END = 48
    KEY_END = 80 
    def __init__(self, password: str, file_path: str) -> None:
        self.file_path = file_path
        self.key = b''
        self.master_password = password
        self.passwords = {}

    # reads and decrypts the file
    def read(self):
        # ensure the file exists
        if not os.path.exists(self.file_path):
            raise ValueError('Password file does not exist')
        # read the file's content
        with open(self.file_path, 'rb') as f:
            ciphertext = f.read()
            key_salt = ciphertext[:self.KEY_SALT_END]
            check_salt = ciphertext[self.KEY_SALT_END:self.CHECK_SALT_END]
            iv = ciphertext[self.CHECK_SALT_END:self.IV_END]
            key_hash = ciphertext[self.IV_END:self.KEY_END]
            ciphertext = ciphertext[self.KEY_END:]
        # generate the key and validate it 
        self.key = SHA256.new(key_salt + self.master_password.encode()).digest()
        checksum = SHA256.new(self.key + check_salt).digest()
        if checksum != key_hash:
            raise ValueError('Invalid Password')
        # decrypt the ciphertext
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        # parse the user passwords from the plaintext
        try:
            self.passwords = json.loads(plaintext.decode())
        except json.JSONDecodeError:
            raise ValueError('Passwords could not be decrypted')

    # encrypts the dictionary as a json string and saves the file
    def write(self):
        # generate requisite salts and iv from system entropy
        key_salt = os.urandom(16)
        check_salt = os.urandom(16)
        iv = os.urandom(16)
        # create and hash the key
        self.key = SHA256.new(key_salt + self.master_password.encode()).digest()
        checksum = SHA256.new(self.key + check_salt).digest()
        # create and encrypt the password's json string
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(json.dumps(self.passwords).encode(), AES.block_size))
        # create the file header and save the newly created file
        header = key_salt + check_salt + iv +  checksum
        with open(self.file_path, 'wb') as f:
            f.write(header+ciphertext) 

    # adds a key to the password dictionary if not already present
    def add_key(self, username: str):
        if username in self.passwords:
            raise ValueError('Username is already in the password database')
        # create a new password
        with open('words.txt') as f:
            words = f.read().split('\n')
        password = ''
        for i in range(3):
            password += secrets.choice(words).capitalize()
            password += secrets.choice('!?%&')
        password += str(secrets.randbelow(100))
        self.passwords[username] = password
        
    # reads a key from the dictionary
    def read_key(self, username: str):
        try:
            return self.passwords[username]
        except KeyError as e:
            return None
