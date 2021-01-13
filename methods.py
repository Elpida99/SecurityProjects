"""
Methods used by both programs store_hashes.py and search_pwds.py
"""
print(__doc__)

import nacl.pwhash
import random, string

# https://nordpass.com/most-common-passwords-list/
# Generate users as userXXX


def generate_users():
    users = []
    for i in range(1, 101):
        username = create_user(i)
        users.append(username)
    return users


def create_user(i):
    if i < 10:
        username = f"user00{i}"
    elif i < 100:
        username = f"user0{i}"
    else:
        username = f"user{i}"

    return username


def create_passwords(users, common_filename):
    passwords = []
    characters = string.ascii_letters + string.digits + string.punctuation
    length = 8
    for i in range(1, len(users) - 40):
        password = []
        for x in range(length):
            password.append(random.choice(characters))
        # Converting String to byte array
        bpassword = ''.join(password).encode('utf-8')
        passwords.append(bpassword)

    common_passwords = read_common_pwds(common_filename)
    random.shuffle(common_passwords)

    for j in range(0, len(users) - i):
        # fill with popular passwords
        passwords.append(common_passwords[j])

    random.shuffle(passwords)

    return passwords


# def read_common_pwds(filename):
#     pwds = []
#     with open(filename) as f:
#         for line in f:
#             # for i in line:
#             pwds.append(line.strip().split(", "))
#     common_passwords = pwds[0]
#     for i in range(1, len(common_passwords)):
#         common_passwords[i] = ''.join(common_passwords[i]).encode('utf-8')
#
#     return common_passwords

def read_common_pwds(filename):
    common_passwords = []
    bc_passwords = []
    f = open(filename)
    for line in f.readlines():
        tmp = line.split(", ")
        for p in tmp:
            common_passwords.append(p)
    for i in range(1, len(common_passwords)):
        temp = ''.join(common_passwords[i]).encode('utf-8')
        bc_passwords.append(temp)
    return bc_passwords


# def hash_passwords(pwds):
#     hashed = []
#     for pwd in pwds:
#         hashed_pwd = nacl.pwhash.str(pwd)
#         hashed.append(hashed_pwd)
#     return hashed

def hash_passwords(pwds):
    hashed = []
    for i in range(0, len(pwds)):#pwd in pwds:
        hashed_pwd = nacl.pwhash.str(pwds[i])
        hashed.append(hashed_pwd)
    return hashed
