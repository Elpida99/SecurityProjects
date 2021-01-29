"""
Port scanner to detect open ports
Ports checked: 20, 21, 22, 25, 80, 156, 443
Saves open ports in file "open_ports.txt"
Grabs banner of open ports--> http_grabber() for ports 80, 443 & banner_grabber() for the rest

"""
print(__doc__)

import socket


def port_scanner(host, address, port):
    """
    :param host: hostname
    :param address: address of host that gets scanned for open ports
    :param port: checks if this port is open
    :return: 0 if port is not open, the port if it is open
    prints the banner if the port is open or the exception message
    + stores it in the file "banners.txt"
    """
    check = False  # check variable -- if it is false in the end the port is not open

    # open socket and connect
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(2)
    result = s.connect_ex((address, port))

    if result == 0:  # the port is open

        check = True  # make check True so that in the end the port is returned

        print(f"Port {port} is open!")
        answer = input("Grab banner? Y/y or N/n >>> ")

        if answer == 'y' or answer == 'Y':
            f_banners = open("banners.txt", 'a+')  # open file to store the banner
            try:
                if port == 80 or port == 443:  # port 80 is HTTP and 443 is HTTPs
                    grabbed_banner = http_grabber(address, s)
                else:
                    grabbed_banner = banner_grabber(s)

                print('>>>', end=" ")  # print this so that it shows that the banner was grabbed

            except Exception as e:  # if something goes wrong
                print("---Unable to grab information: ", end=" ")  # print the exception message
                grabbed_banner = str(e)  # so that if an exception has occurred it will be printed in the file

            print(grabbed_banner)
            f_banners.write(f"############################################<<{host}>>##########################################################\n")
            f_banners.write(f"Address: {address} --- Port: {port} --- Banner:\n")
            f_banners.write(f"{grabbed_banner}\n")  # store the grabbed banner (either the banner or the exception)
            f_banners.write("---------------------------------------------------------------------------------------------------------------------\n")

            f_banners.close()

    # close the socket and the file
    s.close()

    if check:  # if check became True then the port is open
        return port
    else:
        return 0


def banner_grabber(s):
    # grabs the banner and returns it decoded so that it can be printed
    banner = s.recv(1024)

    return banner.decode("ascii")


def http_grabber(host, s):
    # grabs the banner and returns it decoded so that it can be printed
    # for port 80 and 443 (although port 443 is https)

    # sends the following message
    headers = \
        "GET / HTTP/1.1\r\n" \
        f"Host: {host}\r\n\r\n"

    s.send(headers.encode())
    response = s.recv(1024)

    return response.decode("ascii")


def check_input(user_input):
    """
    :param user_input: what the user entered
    :return: hostname and ip address
    """
    if user_input[0] == 'w':  # user input is a hostname
        host = user_input
        ip_address = socket.gethostbyname(host)

    else:  # user input is an ip address
        host = socket.gethostbyaddr(user_input)[0]  # this returns a list of which the first element is one of the hostnames
        ip_address = user_input
    return host, ip_address


def simple_port_scanning(host, ip_address):
    """
    Checks all ports [20, 21, 22, 25, 80, 156, 443] for this address
    it stores the ports it the file "open_ports.txt"
    :param host: hostname
    :param ip_address: ip address
    """

    ports = [20, 21, 22, 25, 80, 156, 443]

    print(f"\nChecking {host} for open ports....")

    open_ports = []
    try:
        for port in ports:
            print(f"Checking port {port}...")

            open_port = port_scanner(host, ip_address, port)  # port_scanner() returns 0 if the port is closed

            if open_port != 0:
                open_ports.append(open_port)  # port is open, append it to the list and check the next one

        if len(open_ports) > 0:  # if any port is open, write in the file the list open_ports
            f_ports = open("open_ports.txt", 'a+')  # open file to append the open ports for this address (if there are any)
            f_ports.write(f"hostname: {host}, address: {ip_address}, open ports: {open_ports}\n")
            f_ports.close()  # close the file

    except socket.error:
        print("--- Server not responding !!!!")


def check_nearest_addresses(ip_address):
    """
    :param user_input (hostname or ip address)
    calls simple_port_scanning() for every neighbouring ip address to the one the user gave
    """

    # split the address into the list and return the index of the last element
    ip_nums = ip_address.split('.')
    index = len(ip_nums)-1

    # strip the last element of the address (e.g 83.212.240.16 --> 83.212.240. )
    base_ip = ip_address.strip(ip_nums[index])

    print("This may take a while...")
    print(f"Checking addresses from {base_ip}0 to {base_ip}100")

    # scan for open ports all addresses beginning with base_ip (e.g 83.212.240.0 to 83.212.240.255 )
    for i in range(0, 256):
        new_address = f"{base_ip}{i}"
        print('\n' + new_address)
        try:
            # address is found--> call simple_port_scanning()
            hostname = socket.gethostbyaddr(new_address)
            simple_port_scanning(hostname, new_address)
        except:
            print("Host not found")  # address not found


def main():
    # print menu
    print("Options:\nEnter the address you want to check for open ports or -q for exit")
    user_input = input(">> ")

    # if user enters '-q' they want to exit
    if user_input == "-q":
        return
    else:
        try:
            # check if the user entered an ip address or a hostname and
            # try to return the hostname and ip address if they exist
            host, target = check_input(user_input)

            # print second menu
            user_choice = input("1. Enter '1' to simply scan this address for open ports\n2. Enter '2' to scan the address and all its neighbours\n>> ")

            if user_choice == "1":
                # simple scanning of the address
                simple_port_scanning(host, target)

            elif user_choice == "2":
                # scans all neighbouring addresses that begin with the first elements of this addresses
                # e.g 83.212.240.16 --> scans al addresses from 83.212.240.0 to 83.212.240.255
                check_nearest_addresses(target)

            else:
                print("Not valid input") # here the user must only enter either '1' or '2'

        except Exception as e:
            # user did not enter an address that is valid or exists
            print("Not valid input: " + str(e))


if __name__ == '__main__':
    main()

