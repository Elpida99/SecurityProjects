"""
Methods used by both programs store_hashes.py and search_pwds.py
"""

import nacl.pwhash
import random
import string
import numbers
import os


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
            f.write(f"{username}: ")
            print(f"Hello {username}")

            password = input("Insert password (-r for randomly generated)\n")
            if password == '-r':
                new_password = create_random_password()
                print(f"Here's your password: {new_password}")
                hashed_password = hash_password(new_password)
                f.write(f"{hashed_password}\n")
            else:
                print(f"Here's your password: {password}")
                hashed_password = hash_password(password)
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
    characters = string.ascii_letters + string.digits + string.punctuation  # types of random characters
    length = 10  # length of randomly generated passwords
    password_chars = []  # single password is a list of characters
    for x in range(length):
        password_chars.append(random.choice(characters))  # 8 random characters (letters, digits & punctuation)
    password = ""
    password = password.join(password_chars)

    return password


def random_ints():
    indexes = []
    common_passwords = ["123456789", "picture1", "password", "asdfghjkl", "love123"]
    for i in range(0, len(common_passwords)):
        r = random.randint(1, 101)
        indexes.append(r)
    return indexes, common_passwords


def test():
    common_passwords = ["123456789", "picture1", "password", "asdfghjkl", "love123"]
    indexes = random.sample(range(1, 100), len(common_passwords))
    return indexes, common_passwords


def store_usernames_and_hashed_passwords():
    f = open("user_passwords.txt", 'w')
    indexes, common_passwords = test()  # random_ints()
    print(common_passwords)
    print(indexes)
    j = 0
    for i in range(1, 101):
        username = create_user(i)
        f.write(f"{username}: ")
        password = ""
        for index in indexes:
            if i == index:
                print(i, j)
                password = common_passwords[j]
                j = j + 1
                continue
            else:
                password = create_random_password()
                continue
        print(username, password)
        hashed_password = hash_password(password)
        f.write(f"{hashed_password}\n")

    f.close()

# store_usernames_and_hashed_passwords()
get_user_input()
