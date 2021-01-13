"""
Program that stores the employees' usernames and hashes in a file called 'user_passwords'
"""
print(__doc__)

from methods import generate_users, create_passwords, hash_passwords


def main(filename):

    users = generate_users()
    passwords = create_passwords(users, filename)
    hashed = hash_passwords(passwords)

    with open('user_passwords', 'wb') as f:
        for i in range(0, len(users)):
            f.write(''.join(users[i]).encode('utf-8'))
            f.write(''.join(": ").encode('utf-8'))
            f.write(hashed[i])
            f.write(''.join("\n").encode('utf-8'))


common_passwords_file = "common_passwords.txt"

main(common_passwords_file)