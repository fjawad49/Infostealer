# Infostealer Implant

**Infostealer Implant** is a Python malware program that iterates through all files and subdirectories in a user's home directory and retrieves the following types of files/folders:
- All SSH-related files/dirs under ~/.ssh/
- All Configuration-related files/dirs under ~/.config/
- All Cloud provider files/dirs under ~/.aws/ or ~/.gcloud/ or ~/.azure/
- All shell history files matching the pattern ~/.*_history

These files are then placed into a ZIP and sent to an always-on server, which extracts the contents of the ZIP within the same directory containing the server. The files are extracted into a new folder with the following name: **"Current_DateTime:Victim_IP"**.

## Dependencies

The only external dependency this program relies on is `cryptography`, which can be installed using the following PowerShell command on Linux if not already pre-installed:

```
sudo apt install python3-cryptography
```

## Implemetnation Decisions
### Retrieving Files
To iterate through the user's home files and subdirectories, I decided the use the `os.walk()` function as this provided the easy functionality of iterating through all subdirectories without needing messy recursion. To write the files into a ZIP file, I decided to simply record the paths of all desired files into an array. For any desired subdirectory, I would simply record all the files paths in the directory into an array as well. 

### Zipping Files
To ZIP the files I utilized Python's `zipfile` library that provided helpful functionality of maintaing relative file paths by automatically creating a directory in a given ZIP file if it does not already exist. This module also allowed the create of in memory ZIP files using buffers.

### Encryption
For encrypting the ZIP file content, I utilized symmetric encryption with the help of the `cryptography` library. I utilized a hardcoded key in both the server and victim malware implant for the symmetric encryption/decryption. The encrypted content was sent to the server over a regular TCP socket connection. 

## Server Setup

Here is an overview of the CLI commands for the server.

```
sudo python server363.py [-h] ip port
```

positional arguments:
  - ip:          Specifies server IP address
  - port:        Specfies server port

options:
  - -h, --help:  show this help message and exit
  
## Malware Implant Setup

Here is an overview of the CLI commands for the malware implant.

```
sudo python tmp363.py [-h] ip port
```

positional arguments:
  - ip:          Specifies server IP address
  - port:        Specfies server port

options:
  - -h, --help:  show this help message and exit


  
