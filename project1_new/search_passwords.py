import nacl.pwhash

def read_common_pwds(filename):
    """
    reads the .txt file with 200 common passwords divided by ', '
    :param filename: name of the file
    :return: returns a list of the common passwords
    """
    common_passwords = []
    # read the file and store the passwords in a list
    f = open(filename,'r')
    for line in f.readlines():
        tmp = line.split(", ")
        for p in tmp:
            common_passwords.append(p)

    f.close()

    return common_passwords


def read_stolen_passwords(filename):
    usernames = []
    passwords = []

    f = open(filename, 'r')
    for line in f.readlines():
        tmp = line.split(": ")
        usernames.append(tmp[0])
        passwords.append(tmp[1].strip())

    f.close()

    return usernames, passwords


def verify_password(password, common_password):
    try:
        res = nacl.pwhash.verify(password.encode('utf-8'), common_password.encode('utf-8'))
    except:
        res = False
    return res


def search_for_passwords(stolen_file, common_passwords_file):

    popular_passwords = read_common_pwds(common_passwords_file)
    usernames, passwords = read_stolen_passwords(stolen_file)

    f = open("found_passwords.txt",'w')
    for user, password in zip(usernames, passwords):
        print(f"trying passwords for username: {user} ...")
        for popular_p in popular_passwords:
            result = verify_password(password, popular_p)
            if result:
                f.write(f"{user}: {popular_p}\n")
                print(f"[+] found password: {popular_p}")

    f.close()


search_for_passwords("user_passwords.txt", "common_passwords.txt")

