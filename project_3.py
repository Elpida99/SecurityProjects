"""
User input: url or hostname, date or option for the current date
The program verifies the ssl certificate by:
    * checking if the hostname and the common name match
    * checking if the CA is one of the trusted ones
    * checking that the version is 3
    * checking if the date given or the current date is within the valid range of the certificate[not_before, not_after]
"""
print(__doc__)

import socket
import ssl
from datetime import datetime
import time
import urllib.parse


def connect(hostname):
    """
    connects with the host and returns the ssl certificate
    """
    ctx = ssl.create_default_context()

    with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
        s.connect((hostname, 443))
        cert = s.getpeercert()

    s.close()
    return cert


def get_cert_info(cert):
    """
    returns the info needed from the ssl certificate
    """
    
    # version
    version = cert['version']

    #issuer
    issuer = cert['issuer']
    issuer_dic = make_dictionary(issuer) # make it a dictionary to return
    issuer_common_name = issuer_dictionary['commonName']

    subject = cert['subject']
    subject_dic = make_dictionary(subject)
    subject_common_name = subject_dictionary['commonName']

    not_after = convert_date(cert['notAfter'].split(" GMT")[0])
    not_before = convert_date(cert['notBefore'].split(" GMT")[0])

    all_data = {'version': version, 'issuer_common_name': issuer_common_name, 'subject_common_name': subject_common_name, 'not_after': not_after, 'not_before': not_before}

    return all_data


def make_dic(target):

    target_dic = {}
    for i in range(0, len(target)):
        temp = dict(target[i])
        target_dic.update(temp)
    return target_dic


def convert_date(date, user_input=False):
    if user_input:
        new_date = time.strptime(date, "%d/%m/%Y")
    else:
        new_date = time.strptime(date, "%b %d %H:%M:%S %Y")

    return new_date


def get_current_date():
    x = datetime.now()
    date = x.strftime("%b %d %H:%M:%S %Y")
    return convert_date(date)


def compare_dates(current_date, not_before, not_after):
    if not_before < current_date < not_after:
        return True

    return False


def check_certificate(hostname, all_data, current_date, trusted_CAs):

    if (compare_dates(current_date, all_data['not_before'], all_data['not_after'])) and (all_data['version'] == 3):
        print("The date is in the valid range and is version 3!")

    temp = all_data['subject_common_name'].split('.')
    print(temp)
    cn = f".{temp[len(temp)-2].strip('*')}.{temp[len(temp)-1].strip('*')}"

    if cn == hostname.strip("www"):
        print("Hostname matches the subject common name")
    else:
        print("Hostname doesn't match the subject common name")

    print(all_data['issuer_common_name'])
    if all_data['issuer_common_name'] in trusted_CAs:
        print("Issuer is OK!")


def check_hostname(hostname):
    try:
        socket.gethostbyname(hostname)
        return 0
    except Exception as e:
        exc = e
        return 1


def parse_url(url):
    parsed_url = urllib.parse.urlparse(url)
    return parsed_url


def main():
    print("Hello, here you can check an ssl certificate")
    input_url: str = input("Enter the url of the page you want to check:\n>>> ")

    parsed_url = parse_url(input_url)

    if parsed_url.netloc == '':
        hostname = input_url.strip('*')
    else:
        hostname = parsed_url.netloc.strip('*')
    print(hostname)
    if check_hostname(hostname):
        print("hostname not found")
        return

    date_option = input("Enter the date as d/m/Y, or enter -c for the current date\n>>> ")
    if date_option == '-c':
        date = get_current_date()
    else:
        try:
            date = convert_date(date_option, user_input=True)
        except Exception as e:
            print("Not valid format or date "+str(e))
            return
    try:
        trusted_CAs = ["TERENA SSL CA 3", "DigiCert SHA2 Secure Server CA", "DigiCert ECC Extended Validation Server CA",
                       "GeoTrust RSA CA 2018","Sectigo RSA Domain Validation Secure Server CA", "Cloudflare Inc ECC CA-3", "DigiCert Secure Site ECC CA-1"]
        cert = connect(hostname)
        all_data = get_cert_info(cert)
        check_certificate(hostname, all_data, date, trusted_CAs)
    except Exception as e:
        print(str(e))


if __name__ == '__main__':
    main()
