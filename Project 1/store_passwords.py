"""
Program that stores the usernames and the password hashes from the user's input
"""
print(__doc__)

import nacl.pwhash
import random
import string


def check_last_user(filename):
    """
    :param filename: name of the file ('user_passwords.txt')
    :return: number of users saved in the txt file (so that we can know who the last one was)
    """
    f = open(filename, 'r')
    users = []
    for line in f.readlines():
        tmp = line.split(": ")
        users.append(tmp[0])
    f.close()
    return len(users)

def create_user(i):  # creates usernames
    if i < 10:
        username = f"user00{i}"
    elif i < 100:
        username = f"user0{i}"
    else:
        username = f"user{i}"

    return username


def hash_password(password):
    """
    hash password and return the hash decoded (because we store it in a .txt file)
    """
    hashed_password = nacl.pwhash.str(password.encode('utf-8'))

    return hashed_password.decode('ascii')


def create_random_password():
    """
    makes a list of 14 random characters (ascii letters & digits) and joins these characters in a string named 'password'
    :return: 14 character-length password with random letters and digits
    """
    characters = string.ascii_letters + string.digits  # types of random characters
    print(characters)
    length = 14
    password_chars = []
    for x in range(length):
        password_chars.append(random.choice(characters))
    password = ""
    password = password.join(password_chars)

    return password


def main(passwords_filename):
    """
    opens text file and appends new username and password
    """
    # print little "menu"
    print("Enter your username and your password as requested")
    print("-r for randomly generated password (recommended)")
    print("-q for exit")

    # read the password file and check who the last user was
    try:
        last_user = check_last_user(passwords_filename)
    except:
        last_user = 0

    # open file or create it if it doesn't exist (mode is 'a' = append)
    f = open(passwords_filename, 'a+')

    # loop so that we can enter multiple usernames and passwords
    while True:

        user_input = input(
            f"Insert your user number - previous user was user {last_user} (e.g user001 enters: 1, etc.)\n")  # usernames must be like 'user001, user010, etc.

        # exit option
        if user_input == '-q':
            break

        # the user entered something else
        try:
            # the user must enter an integer (e.g user015 should enter: 15)
            user = int(user_input)
            username = create_user(user)  # create the username

            print(f"Hello {username}")

            # now it's time for the password
            password = input("Insert password (-r for randomly generated password)\n")

            # exit option (the user can exit here and his username will not be written in the file)
            if password == '-q':
                break

            # option for generating a random password automatically
            if password == '-r':
                new_password = create_random_password()
            else:  # the user chooses their password
                new_password = password

            print(f"Here's your password: {new_password} \n*Make sure no-one knows except for you*\n")
            hashed_password = hash_password(new_password)  # hash the password
            # store everything in the file
            f.write(f"{username}: ")
            f.write(f"{hashed_password}\n")

        # if the user does not enter a number, they get this message
        except:
            print("Not valid input")
        last_user = last_user+1
    f.close()


if __name__ == '__main__':
    main("user_passwords.txt")
