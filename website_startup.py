import json
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64

file_name = 'user_info.json'

password = 'my_secure_password'
salt = b'my_salt'

def generate_key(password, salt):
    return PBKDF2(password, salt, dkLen=32)

key = generate_key(password, salt)

def pad(data):
    return data + (16 - len(data) % 16) * chr(16 - len(data) % 16).encode()

def unpad(data):
    return data[:-ord(data[len(data)-1:])]

def load_user_info():
    try:
        with open(file_name, 'rb') as file:
            encrypted_data = file.read()
        iv = encrypted_data[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data[16:]))
        return json.loads(decrypted_data)
    except FileNotFoundError:
        return {}
    except (json.JSONDecodeError, ValueError):
        print("Error decoding the user information file.")
        return {}

def save_user_info(user_info):
    data = json.dumps(user_info).encode()
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = iv + cipher.encrypt(pad(data))
    with open(file_name, 'wb') as file:
        file.write(encrypted_data)

user_info = load_user_info()

print("S = sign up L = log in C = change information")
su_OR_li = input("Would you like to sign up, log in, or change information?: ")

if su_OR_li == 'S':
    su_username = input("What would you like your username to be: ")
    su_password = input("What would you like your password to be: ")
    user_info[su_username] = su_password
    save_user_info(user_info)
    print("Sign-up successful. Username and password saved.")

elif su_OR_li == 'L':
    li_username = input("Enter your username: ")
    li_password = input("Enter your password: ")
    if li_username in user_info and user_info[li_username] == li_password:
        print("Account logged in.")
    else:
        print("Invalid username or password.")

elif su_OR_li == 'C':
    su_username = input("Enter your current username: ")  
    if su_username in user_info:
        print("Y = yes N = no")
        password_option = input("Would you like to change your password?: ")

        if password_option == 'Y':
            password_one = input("What would you like to change your password to?: ")
            password_two = input("Re-enter your password: ")
            if password_one == password_two:
                user_info[su_username] = password_one
                save_user_info(user_info)
                print("Password changed.")
            else:
                print("Passwords do not match.")

        print("Y = yes N = no")
        username_option = input("Would you like to change your username?: ")

        if username_option == 'Y':
            new_username = input("What would you like to change your username to?: ")
            user_info[new_username] = user_info.pop(su_username)
            save_user_info(user_info)
            print("Username has been changed.")
    else:
        print("Invalid username.")


