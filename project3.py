import socket
import ssl
from datetime import datetime


hostname = 'www.hua.gr'
port = 443


def connect(hostname, port):

    ctx = ssl.create_default_context()

    with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
        s.connect((hostname, port))
        cert = s.getpeercert()
        test = s.cipher()

    s.close()
    return cert, test


x = datetime.now()
date = x.strftime("%b %d %H:%M:%S %Y")
print(f"current date: {date}")


def get_cert_info(cert):
    version = cert['version']
    issuer = cert['issuer']
    issuer_common_name = issuer[4][0][1]
    subject = cert['subject']
    subject_common_name = subject[5][0][1]
    not_after = cert['notAfter']
    not_before = cert['notBefore']

    return version, issuer_common_name, subject_common_name, not_after, not_before


cert, test = connect(hostname, port)
print()
version, issuer_common_name, subject_common_name, not_after, not_before = get_cert_info(cert)

if (hostname.split('www')[1]) == (subject_common_name.split('*')[1]):
    print("Certificate is issued to the right host")



