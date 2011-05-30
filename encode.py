import base64

class passhash:
    password = open('password', 'r')
    passtext = password.read()
    passbin = base64.standard_b64encode(passtext)
    password.close()
    print(passbin)
    passout = open('password', 'w')
    passout.write(passbin)
    passout.close()
    