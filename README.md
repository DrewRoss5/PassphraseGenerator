# PassphraseGenerator
CLI Utility for generating and storing passphrases
## ⚠Warning⚠
While this program uses AES-256-CBC encryption, it was made as a hobby project and hasn't been professionally audieted for security.<br>**Use with Caution.**
## PassPhrase Generation: 
Passphrase are generated with three randomly selected words from the words.txt file. The words are seperated with randomly selected characters and followed by a randomly genereated number between 0-100 (exclusive.) Currently there are 10000 possible words.<br>
### Example:
Establishing%Mercy!Passport!60
## Encryption:
Passwords encrypted with AES-256 operating in CBC mode. The key is a SHA-256 of the provided master password with a cryptographically secure random salt. 
## Usage:
Run the main.py file.There are three operations this program can perform.<br>
### Creating a file:
To create a password file, run: `main.py create <filename>` where <filename> is, of course, the name of the password file to be created.
### Adding a password to a file:
To create a new ranomly generated password and add it to an existing password file, run: `main.py add <filename> <site>` where site is the username or website the password will be for.
### Accessing a password from a file:
To access a password from an existing password file, run: `main.py get <filename> <site>` The password will be automatically copied to your clipboard to avoid shoulder surfing. 
