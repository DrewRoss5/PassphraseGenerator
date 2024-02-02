import passFile as pf
import sys
import getpass
import pyperclip

if len(sys.argv) not in (3, 4):
    print('Error - This program accepts between two and three arguments.')
    sys.exit(1)

# determine the action the user would like to perform and the file on which they'd like to perform it.
action = sys.argv[1]
file_name = sys.argv[2]

# get the user's password and create a password file object with
password = getpass.getpass()
pass_file = pf.PassFile(password, file_name)

# run the appropriate functions for the user's selected action
match action:
    case 'create':
        pf.write()
        print('Password file was created succesfully')
    
    case 'get':
        # decrypt the password file
        try:
            pass_file.read()
        except ValueError as e:
            print(f'Error - {e}')
            sys.exit(1)
        # validate length of arguments
        if len(sys.argv) != 4:
            print('Error - Please provide the name of the password to be read')
            sys.exit(1)
        # attempt to get the password from the dictionary
        username = sys.argv[3]
        password = pass_file.read_key(username)
        if not password:
            print(f'Error - A password for the username "{username}" could not be found')
            sys.exit(1)
        # copy the password to user's clipboard
        pyperclip.copy(password)
        print('Password has been copied to clipboard')

    case 'add':
        # decrypt the password file
        try:
            pass_file.read()
        except ValueError as e:
            print(f'Error - {e}')
            sys.exit(1)
        # validate length of arguments
        if len(sys.argv) != 4:
            print('Error - Please provide the name of the password to be created')
            sys.exit(1)
        # attempt to generate a new password for the given username
        username = sys.argv[3]
        try:
            pass_file.add_key(username)
            pass_file.write()
            print(f'A new password for the username "{username}" was created successfully')
        except ValueError:
            print(f'A password cannot be created for the username "{username}"\nPerhaps it already exists?')
