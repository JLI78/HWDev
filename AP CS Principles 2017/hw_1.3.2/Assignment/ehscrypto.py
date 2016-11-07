# https://pycryptodome.readthedocs.io/en/latest/src/examples.html#encrypt-data-with-aes

import sys
import binascii
import os
import struct
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP



class EHSCrypto:
    """ EHS Crypto class. Latest release rev-alpha-1.0.0, 2016_10_18."""

    def __init__(self):
        pass

    def add_elements_to_array(self, target_arr, arr_to_add):
        """ Add the bytes from the arr_to_add to the target array"""

        no_of_elements = len(arr_to_add)
        for k in range(no_of_elements):
            target_arr.append(arr_to_add[k])

        return  target_arr

    def number_to_int16(self, thenumber):
        """ Converting a number to a defined set of bytes"""

        # TODO: complete this method with proper functionality, for now use only 2 bytes.

        # if thenumber > 2**(noofbytes*8):
        #     print "Can't convert, too big of a number..."
        #     return

        res = [thenumber >> i & 0xff for i in ( 8, 0)]

        # res = [hex(thenumber >> i & 0xff) for i in (8, 0)]
        # res = thenumber & 0xffff
        return res

    def generate_rsa_key_pair(self,filename):
        """ Generate the keys for RSA"""

        # Start RSA crypto system
        key = RSA.generate(2048)

        # Private key generation
        private_key = key.exportKey(pkcs=8)
        private_filename = filename + '_rsa_key_private.bin'
        file_out_private = open(private_filename, "wb")
        file_out_private.write(private_key)
        print('private key size: ', sys.getsizeof(private_key))

        # Public key generation
        public_key = key.publickey().exportKey()
        public_filename = filename + '_rsa_key_public.bin'
        file_out_public = open(public_filename, "wb")
        file_out_public.write(public_key)
        print('public key size: ', sys.getsizeof(public_key))

        print 'key pairs generated... put them in a secure location...'

    def generate_aes_session_key(self):
        """ Generate a session key for the symmetric crypto system. 16 bytes by default"""
        return get_random_bytes(16)

    def rsa_encrypt_data(self,public_key_filename, data_to_encrypt):
        """ Encrypt the data with the public key specified in the path"""

        # import rsa public key from file.
        public_key = RSA.importKey(open(public_key_filename).read())
        # start RSA cipher engine, with the selected public key.
        rsa_cipher = PKCS1_OAEP.new(public_key)
        # encrypt the data
        cipher_data = rsa_cipher.encrypt(data_to_encrypt)
        # print 'rsa data size : ' + str(len(cipher_data))
        # print 'rsa encrypted data : ' + cipher_data.encode('hex')
        return cipher_data

    def rsa_decrypt_data(self,private_key_filename, data_to_dencrypt):
        """ Decrypt the data using the private key specified in the path. """

        # import rsa private key from file.
        private_key = RSA.importKey(open(private_key_filename).read())
        # start RSA cipher engine, with the selected private key.
        rsa_cipher = PKCS1_OAEP.new(private_key)
        # decrypt the data
        plaintext_data = rsa_cipher.decrypt(data_to_dencrypt)
        # print 'rsa decrypt data size : ' + str(len(plaintext_data))
        # print 'rsa decrypt plaintext data : ' + plaintext_data.encode('hex')
        # print 'rsa decrypt plaintext data : ' + plaintext_data
        return plaintext_data

    def aes_encrypt_data(self,session_key,data_to_encrypt):
        """ encrypt using Advanced Encryption Standard (AES) block cipher"""

        #  data must have be a multiple of 16 in length, adding a special character
        #  to pad. the char will be removed when decrypting.

        # print data_to_encrypt
        length = 16 - (len(data_to_encrypt) % 16)
        data_to_encrypt += '|' * length
        aes_cipher = AES.new(session_key)
        cipher_data = aes_cipher.encrypt(data_to_encrypt)
        # print 'aes data size : ' + str(len(cipher_data))
        # print 'aes encrypted data : ' + cipher_data.encode('hex')
        return cipher_data

    def aes_decrypt_data(self, session_key, data_to_decrypt):
        """ decrypt using Advanced Encryption Standard (AES) block cipher"""

        aes_cipher = AES.new(session_key)
        padded_text = aes_cipher.decrypt(data_to_decrypt)

        # removing the padding from the end. We are using '.' for padding here.
        plaintext = padded_text.replace('|','')

        # print 'decrypted data size : ' + str(sys.getsizeof(plaintext))
        # print 'decrypted data : ' + plaintext.encode('hex')
        # print 'decrypted data : ' + plaintext
        return plaintext

    def get_file_data(self, filename):
        """ Open a file and get the data."""

        fid = open(filename,'r')
        filedata = fid.read()
        # print  filedata
        return filedata

    def encrypt_homework_file(self, plain_homework_file):
        """ Perform the whole encryption schema, but not saving to file just yet"""

        print '... Implementing homework encryption workflow...'

        # load the content of the file
        msg = self.get_file_data(plain_homework_file)
        # get the user name. User validation can be added later
        user_name = raw_input(' Enter user name : ')    #'peter pan'

        aes_key = self.generate_aes_session_key()
        ciphered_uname = self.aes_encrypt_data(aes_key, user_name)
        ciphered_msg = self.aes_encrypt_data(aes_key, msg)
        ciphered_aes_key = self.rsa_encrypt_data('ehs_20161010_rsa_key_public.bin', aes_key)
        uname_length = self.number_to_int16(len(ciphered_uname))
        aes_key_length = self.number_to_int16(len(ciphered_aes_key))

        data_to_file = bytearray([])
        self.add_elements_to_array(data_to_file, uname_length)
        self.add_elements_to_array(data_to_file, aes_key_length)
        self.add_elements_to_array(data_to_file, ciphered_uname)
        self.add_elements_to_array(data_to_file, ciphered_aes_key)
        self.add_elements_to_array(data_to_file, ciphered_msg)
        # print ' --> encrypted msg: ' + binascii.hexlify(data_to_file)

        # writing to file. alternative we can use the user name in the file name
        output_filename = user_name + '_' + plain_homework_file + '.eee'
        file_out = open(output_filename, "wb")
        file_out.write(data_to_file)
        print '... Homework encryption completed.'

    def decrypt_homework_file(self,cipher_homework_file):
        """ Perform the whole decryption scheme. """

        print '... Implementing homework decryption workflow...'

        # reading the encrypted data file
        file_in = open(cipher_homework_file, "rb")
        encrypted_data = file_in.read()

        uname_length = struct.unpack('>h', encrypted_data[0:2])[0]
        # print uname_length

        aes_key_length = struct.unpack('>h', encrypted_data[2:4])[0]
        # print aes_key_length

        unamestart = 4
        unameend = 4 + uname_length
        keystart = 4 + uname_length
        keyend = 4 + uname_length + aes_key_length
        msgstart = 4 + uname_length + aes_key_length
        msgend = len(encrypted_data)

        # Recovering the data from the file
        ciphered_uname = encrypted_data[unamestart:unameend]
        # print binascii.hexlify(ciphered_uname)

        ciphered_aes_key = encrypted_data[keystart:keyend]
        # print binascii.hexlify(ciphered_aes_key)

        ciphered_msg = encrypted_data[msgstart:msgend]
        # print binascii.hexlify(ciphered_aes_key)

        # Starting decrypting process
        aes_key = self.rsa_decrypt_data("ehs_20161010_rsa_key_private.bin", ciphered_aes_key)
        # print aes_key

        plain_uname = self.aes_decrypt_data(aes_key, ciphered_uname)
        # print plain_uname

        # getting the original message and saving it to file
        plain_msg = self.aes_decrypt_data(aes_key, ciphered_msg)
        print ' --> Recovered message : ' + plain_msg

        # saving to a file now
        student_filename = os.path.splitext(os.path.basename(cipher_homework_file))[0]
        file_out = open(student_filename, "wb")
        file_out.write(plain_msg)

        print '... Homework decryption completed.'

    def test_01(self):
        """ Test 01 - generating key pairs."""

        self.generate_rsa_key_pair('sg')

    def test_02(self):
        """ Test 02 - enc/dec with RSA"""

        # encrypting the data
        sampledata = b'mydata'
        ciphertext = self.rsa_encrypt_data('ehs_20161010_rsa_key_public.bin', sampledata)
        # decrypting the data
        plaintext = self.rsa_decrypt_data('ehs_20161010_rsa_key_private.bin', ciphertext)
        assert sampledata == plaintext

    def test_03(self):
        """ Test 03 - encrypting data from a file using RSA."""

        python_data = self.get_file_data('hw_1.4.1.py')
        cipher_text = self.rsa_encrypt_data('ehs_20161010_rsa_key_public.bin', python_data)
        plain_text = self.rsa_decrypt_data('ehs_20161010_rsa_key_private.bin', cipher_text)
        assert python_data == plain_text

    def test_04(self):
        """ Testing AES encryption schema"""

        print '... testing AES encryption'
        session_key = self.generate_aes_session_key()

        # encrypting the data
        sample_data = b'0123456789abcdef'
        cipher_text = self.aes_encrypt_data(session_key,sample_data)
        # decrypting the data
        plain_text = self.aes_decrypt_data(session_key,cipher_text)
        assert sample_data == plain_text

    def test_05(self, content_to_encrypt):
        """ Perform the whole encryption schema, but not saving to file just yet"""

        print '... Test_05 starting...'
        user_name = 'petery'

        # msg = 'This is the message. Encrypt and send to Bob.'
        msg = content_to_encrypt
        print ' --> Original message : ' + msg

        aes_key = self.generate_aes_session_key()
        ciphered_uname = self.aes_encrypt_data(aes_key, user_name)
        ciphered_msg = self.aes_encrypt_data( aes_key, msg)
        ciphered_aes_key = self.rsa_encrypt_data('ehs_20161010_rsa_key_public.bin',aes_key)
        uname_length = self.number_to_int16(len(ciphered_uname))
        aes_key_length = self.number_to_int16(len(ciphered_aes_key))
        # result = (aes_key_length,uname_length, ciphered_aes_key,ciphered_uname,ciphered_msg)
        # print result

        data_to_file = bytearray([])
        self.add_elements_to_array(data_to_file, uname_length)
        self.add_elements_to_array(data_to_file, aes_key_length)
        self.add_elements_to_array(data_to_file, ciphered_uname)
        self.add_elements_to_array(data_to_file, ciphered_aes_key)
        self.add_elements_to_array(data_to_file, ciphered_msg)
        print ' --> encrypted msg: ' +  binascii.hexlify(data_to_file)

        # writing to file
        file_out = open("encrypted_message.eee", "wb")
        file_out.write(data_to_file)
        print '... Test_05 completed...'

    def test_06(self):
        """ Perform the whole decryption scheme. """

        print '... Test_06 starting...'

        # reading the encrypted data file
        file_in = open("encrypted_message.eee", "rb")
        encrypted_data = file_in.read()

        uname_length = struct.unpack('>h', encrypted_data[0:2])[0]
        # print uname_length

        aes_key_length = struct.unpack('>h', encrypted_data[2:4])[0]
        # print aes_key_length

        unamestart = 4
        unameend = 4 + uname_length
        keystart = 4 + uname_length
        keyend = 4 + uname_length + aes_key_length
        msgstart = 4 + uname_length + aes_key_length
        msgend = len(encrypted_data)

        # Recovering the data from the file
        ciphered_uname = encrypted_data[unamestart:unameend]
        # print binascii.hexlify(ciphered_uname)

        ciphered_aes_key = encrypted_data[keystart:keyend]
        # print binascii.hexlify(ciphered_aes_key)

        ciphered_msg = encrypted_data[msgstart:msgend]
        # print binascii.hexlify(ciphered_aes_key)

        # Starting decrypting process
        aes_key = self.rsa_decrypt_data("ehs_20161010_rsa_key_private.bin", ciphered_aes_key)
        # print aes_key

        plain_uname = self.aes_decrypt_data( aes_key,ciphered_uname)
        # print plain_uname

        # plain_msg = self.aes_decrypt_data(aes_key,ciphered_msg)
        plain_msg = self.aes_decrypt_data(aes_key,ciphered_msg)
        print ' --> Recovered message : ' + plain_msg

        print '... Test_06 completed...'

    def test_07(self, file_to_encrypt):
        """ Encrypt and decrypt the content of a file """

        content = crypto.get_file_data(file_to_encrypt)
        print content
        self.test_05(content)

        self.test_06()

    def run_test_battery(self):
        """Add the actions you want to happen when the script is run from the console."""

        print ' ... starting testing.'
        # self.test_01()
        # self.test_02()
        # self.test_03()
        # self.test_04()
        # self.test_05('This is the message.')
        # self.test_06()
        # self.test_07_encrypt_file_content('hw_1.4.1.py')
        # self.encrypt_homework_file('hw_1.4.1.py')
        # self.decrypt_homework_file('Glover Ruiz_testy.py.eee')


if __name__ == "__main__":
    """ this code will run when launch from the environment."""
    crypto = EHSCrypto()
    crypto.run_test_battery()





