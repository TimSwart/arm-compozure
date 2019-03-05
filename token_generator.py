import getpass
import base64

username = input('Username:')
password = getpass.getpass('Password/Token:')
userpass = str.encode("{}:{}".format(username, password))
authorization = base64.b64encode(userpass).decode()
print("Authorization token: {}".format(authorization))