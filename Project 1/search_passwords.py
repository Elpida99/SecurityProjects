"""
Program that stores the usernames and the password hashes from the user's input
https://nordpass.com/most-common-passwords-list/ --> source of common passwords
"""
print(__doc__)
import nacl.pwhash


def read_common_passwords(filename):
    """
    reads the .txt file with 200 common passwords divided by ', '
    :param filename: name of the file ('common_passwords.txt')
    :return: returns a list of all these common passwords
    """
    common_passwords = []
    # read the file and store the passwords in a list
    f = open(filename, 'r')
    for line in f.readlines():
        tmp = line.split(", ")
        for p in tmp:
            common_passwords.append(p)

    f.close()

    return common_passwords


def read_stolen_passwords(filename):
    """
    reads the stolen file with the stored usernames and password hashes
    username and hash are separated by ': '
    :param filename: name of the file ('user_passwords.txt')
    :return: a list of all the usernames & a list of all the password hashes
    """
    usernames = []
    passwords = []

    f = open(filename, 'r')
    for line in f.readlines():
        tmp = line.split(": ")
        usernames.append(tmp[0])
        passwords.append(tmp[1].strip())  # every line ends with '\n', strip() removes it

    f.close()

    return usernames, passwords


def verify_password(user_hash, common_password):
    """
    verifies if the hash matches the common password
    :param user_hash: password hash extracted from the stolen file
    :param common_password: password extracted from the file with the popular passwords
    :return: True if they match, False if they don't
    """
    try:
        res = nacl.pwhash.verify(user_hash.encode('utf-8'), common_password.encode('utf-8'))  # both encoded into byte arrays
    except:
        res = False
    return res


def main(stolen_file, common_passwords_file):
    """
    main function, reads both files, verifies the passwords and
    stores in a file the found matching passwords alongside the usernames
    :param stolen_file: 'user_passwords.txt'
    :param common_passwords_file: 'common_passwords.txt'
    """

    common_passwords = read_common_passwords(common_passwords_file)
    usernames, passwords = read_stolen_passwords(stolen_file)
    print("This may take a while...")
    f = open("found_passwords.txt",'w+')
    for user, user_hash in zip(usernames, passwords):
        print(f"trying passwords for username: {user}...")
        for common_p in common_passwords:
            result = verify_password(user_hash, common_p)
            if result:
                f.write(f"{user}: {common_p}\n")
                print(f"[+] found password: {common_p}")
                break
    f.close()


if __name__ == '__main__':
    main("user_passwords.txt", "common_passwords.txt")

