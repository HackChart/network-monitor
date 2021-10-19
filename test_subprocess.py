import subprocess

# run command, capture result
x = subprocess.run(['ls'], capture_output=True)
# grab stdout as bytestring, decode to utf-8
print(x.stdout.decode('UTF-8'))