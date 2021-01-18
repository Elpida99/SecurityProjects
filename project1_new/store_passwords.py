"""
Program that stores usernames and hashed passwords from user input
"""

import nacl.pwhash
import random
import string


# https://nordpass.com/most-common-passwords-list/ --> source of common passwords
# Generate users as userXXX


def get_user_input():
    print("Enter your username and your password as requested")
    print("-r for randomly generated password (recommended)")
    print("-q for exit")
    f = open("user_passwords.txt", 'a')
    while True:
        user_input = input("Insert your user number (e.g 1 or 10, etc.)\n")

        if user_input == '-q':
            break

        try:
            user = int(user_input)
            username = create_user(user)

            print(f"Hello {username}")

            password = input("Insert password (-r for randomly generated password)\n")

            if password == '-q':
                break
            if password == '-r':
                new_password = create_random_password()
            else:
                new_password = password

            print(f"Here's your password: {new_password} \n*Make sure no-one knows except for you*\n")
            hashed_password = hash_password(new_password)
            f.write(f"{username}: ")
            f.write(f"{hashed_password}\n")

        except:
            print("Not valid input")
    f.close()


def create_user(i):  # creates usernames
    if i < 10:
        username = f"user00{i}"
    elif i < 100:
        username = f"user0{i}"
    else:
        username = f"user{i}"

    return username


def hash_password(password):
    hashed_password = nacl.pwhash.str(password.encode('utf-8'))
    return hashed_password.decode('ascii')


def create_random_password():
    characters = string.ascii_letters + string.digits # types of random characters
    length = 14  # length of randomly generated passwords
    password_chars = []  # single password is a list of characters
    for x in range(length):
        password_chars.append(random.choice(characters))  # 14 random characters (letters & digits)
    password = ""
    password = password.join(password_chars)

    return password


get_user_input()

