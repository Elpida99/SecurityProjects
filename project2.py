import socket


def port_scanner(address, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(5)

    result = s.connect_ex((address, port))
    if result == 0:
        print(f"Port {port} is open!")
        try:
            if port == 80 or port == 443:
                response = http_grabber(s)
                print('[+]' + str(response))
            else:
                banner = banner_grabber(s)
                print(address + ':', end='')
                print(banner.decode('utf-8'))
        except Exception as e:
            print("Unable to grab information: "+str(e))
    s.close()


def banner_grabber(s):

    banner = s.recv(1024)

    return banner


def http_grabber(s):

    message = b'GET HTTP/1.1\r\n'
    s.send(message)
    response = s.recv(1024)

    return response


def main():
    hostnames = ["www.hua.gr", "www.skai.gr", "www.ert.gr", "www.ethnos.gr", "www.protothema.gr", "www.public.gr", "www.plaisio.gr", "www.kotsovolos.gr"]
    ports = [20, 21, 22, 23, 25, 80, 156, 443]
    for host in hostnames:
        print(f"\nChecking {host} for open ports....")
        target = socket.gethostbyname(host)
        try:
            for port in ports:
                print(f"Checking port {port}...")
                port_scanner(target, port)

        except socket.error:
            print(">>> Server not responding !!!!")


main()
