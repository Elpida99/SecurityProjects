"""
Program that searches for matching passwords between the stolen hashes and the common passwords file
It stores any match found in a file called 'found_pwds.txt'
"""
print(__doc__)

from methods import read_common_pwds
import nacl.pwhash


def main(common_passwords_filename, stolen_passwords_filename):
    common_passwords = read_common_pwds(filename=common_passwords_filename)

    with open(stolen_passwords_filename, 'r') as f:
        users = []
        hashes = []
        for line in f:
            user = line.strip().split(": ")[0]
            hash = line.strip().split(": ")[1]

            users.append(user)
            hashes.append(''.join(hash).encode('utf-8'))

    found_users = []
    found_pwrds = []

    for i in range(1, len(hashes) + 1):
        for p in common_passwords:
            try:
                res = nacl.pwhash.verify(hashes[i - 1], p)
                print(res)
                found_pwrds.append(p)
                found_users.append(users[i - 1])
            except:
                f = False

    with open('found_pwds.txt', 'w') as f:
        for i in range(0, len(found_users)):
            f.write(found_users[i] + ": " + found_pwrds[i].decode('utf-8') + "\n")


common_passwords_file = "common_passwords.txt"
stolen_passwords_file = "user_passwords"

main(common_passwords_file, stolen_passwords_file)