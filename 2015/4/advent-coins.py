import hashlib

done = False;

key_string = "bgvyzdsv"
key_number = 0

while(done == False):
    
    key = key_string + str(key_number)
    MD5_hash = hashlib.md5(key.encode('utf-8')).hexdigest()
    if(MD5_hash[:6] == "000000"):
        done = True;
    else:
        key_number += 1

print(key_string + " : " + str(key_number) + " -> " + MD5_hash)
