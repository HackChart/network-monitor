import subprocess

results = subprocess.run('./speedtest', capture_output=True)
print(results)
print(results.stdout)
decoded_results = results.stdout.decode('UTF-8')
print(decoded_results)

# grab variables for upload/download
# TODO: move all captured results into class for easy use
for line in decoded_results.split('\n'):
    print(line)
    if 'Download' in line:
        download = line.strip()
    elif 'Upload' in line:
        upload = line.strip()
try:
    print(f'{upload}\n{download}')
except NameError:
    print('Capture Failed')


