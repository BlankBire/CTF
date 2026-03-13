import hashlib
target = "3a52fc83037bd2cb81c5a04e49c048a2"
with open("rockyou.txt", 'r', encoding='latin-1') as f:
    for line in f:
        password = line.strip()
        for i in range(100):
            flag = password + str(i).zfill(2)
            hash = hashlib.md5(flag.encode()).hexdigest()
            if hash == target:
                print(f"Flag: pctf{{{flag}}}")
                exit()