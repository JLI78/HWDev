import ehscrypto

print  '... Starting homework encrypting.'

file_to_encrypt = 'hw_1.4.1.py'

hw_encrypter = ehscrypto.EHSCrypto()

hw_encrypter.encrypt_homework_file(file_to_encrypt)

print  '... Homework encrypting completed. Send the resulting *.eee file for review.'

