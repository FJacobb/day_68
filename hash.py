import os, binascii
from backports.pbkdf2 import pbkdf2_hmac
class Pwd_hash():
    def __init__(self):
        self.salt = binascii.unhexlify('74784e323068766a4e4e424f5965333239445850724d4759677a4f68666a4c6f74623636584a4162414f6d435962595667316c55506c6a4d53614f3674595561')

    def hash(self):

        self.key = pbkdf2_hmac("sha256", self.passwd, self.salt, 100000, 85)
        return binascii.hexlify(self.key)
    def passindata(self, password):
        self.passwd = password.encode("utf8")
        return self.hash().decode('utf-8')