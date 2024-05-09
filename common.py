import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from datetime import *






# TODO : in the future - make this close to be Singleton
class Encryption:


    def __init__(self):
        self.pub_key_path = 'C:\\Users\\ניר\\cyberproject24\\pub_key'    
        self.priv_key_path = 'C:\\Users\\ניר\\cyberproject24\\priv_key'


    # run this once(!)  to create keys, not in ctor!
    def init_once(self):    
        key = RSA.generate(2048)
        private_key = key.export_key('PEM')
        f = open (self.pub_key_path,"wb")
        public_key = f.write(private_key)
        f.close()
        f = open (self.priv_key_path,"wb")
        public_key = f.write(private_key)
        f.close()
        public_key = key.publickey().exportKey('PEM')
   
    def rsa_encrypt_msg(self, message):
        message = str.encode(message)
        f = open (self.pub_key_path,"rb")
        public_key = f.read()
        f.close()
        rsa_public_key = RSA.importKey(public_key)
        rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
        encrypted_text = rsa_public_key.encrypt(message)
        return encrypted_text


    def rsa_decrypt_msg(self, encrypted_text):
        f = open (self.priv_key_path,"rb")
        private_key = f.read()
        f.close()
        rsa_private_key = RSA.importKey(private_key)
        rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
        decrypted_text = rsa_private_key.decrypt(encrypted_text)
        return decrypted_text


class Time:
    def __init__(self):
        self.timenow = datetime.now()
   
    def time(self):
        timestamp = int(self.timenow.timestamp())
        return timestamp


shared_vars = {
    "connection_status": False
}


get_client_id_msg = "Please enter client ID:"
server_ip = "127.0.0.1"
server_port = 7999
successful_connection = "connection_established"
