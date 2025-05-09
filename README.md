# TCPScan

**TCPScan** is a Python program that SYN scans a target IP address on a range of ports to identify open ports and service fingerprint each open port. For each open port, the program returns the host address and port, port service type, and response (if any). The port service type can be one of the following:

- TCP server-initiated (server banner was immediately returned over TCP)
- TLS server-initiated (server banner was immediately returned over TLS)
- HTTP server (GET request over TCP successfully elicited a response)
- HTTPS server (GET request over TLS successfully elicited a response)
- Generic TCP server (Generic lines over TCP may or may not elicit a response)
- Generic TLS server (Generic lines over TLS may or may not elicit a response)

## Implemetnation Decisions
During my program development, I chose to first check if a particular port on the target host is open, and then immediately move into service fingerprinting for the given open port before SYN scanning the next port in sequence. Personally, I felt it would save time and space by combining SYN scanning and service fingerprinting into one step for each port. From a programming perspective, this reduces memory consumed and extra for loop iterations.

## Dependencies

The only external dependency this program relies on is `scapy`, which can be installed using the following PowerShell command on Linux if not already pre-installed:

```
sudo apt install python3-scapy
```
## Commands

Here is an overview of the CLI commands.

```
sudo python [-h] [-p port_range] target
```

positional arguments:
  - target:         Specfies the target IP address for port scanning and
                 service fingerprinting.

options:
  - -h, --help:     show this help message and exit
  - -p port_range:  Specifies range of ports to scan in the format X-Y, where
                 X and Y are integers greather than or equal to 0. A single
                 port number is also accepted. If unspecified, program will
                 scan on ports 21, 22, 23, 25, 80, 110, 143, 443, 587, 853,
                 993, 3389, and 8080

  
**NOTE:** The order of CLI options are not important. The program should be run using the `sudo` command to avoid any permission errors.
  
## Example Input and Output

1. TCP server-initiated response on `ftp.dlptest.com:21`.
```
$ sudo python tcpscan.py -p 21 44.241.66.173
Host: 44.241.66.173:21
Type: (1) TCP server-initiated 
Response: 220 Welcome to the DLP Test FTP Server

```
2. Detecting an HTTPS server (GET request over TLS successfully elicited a response) on `www.cs.stonybrook.edu:443`.
```
$ sudo python tcpscan.py -p 443 23.185.0.4 
Host: 23.185.0.4:443
Type: (4) HTTPS server 
Response: HTTP/1.1 404 Unknown site
Connection: close
Content-Length: 566
Retry-After: 0
Server: Pantheon
Cache-Control: no-cache, must-revalidate
Content-Type: text/html; charset=utf-8
X-pantheon-serious-reason: The page could not be loaded properly.
Date: Sun, 30 Mar 2025 00:32:39 GMT
X-Served-By: cache-lga21949-LGA
X-Cache: MISS
X-Cache-Hits: 0
X-Timer: S1743294759.119879,VS0,VE27
Vary: Cookie
Age: 0
Accept-Ranges: bytes
Via: 1.1 varnish

```

3. Detecting a generic TLS server (generic lines cause connection termination) on `8.8.8.8:853`.
```
$ sudo python tcpscan.py -p 853 8.8.8.8
Host: 8.8.8.8:853
Type: (6) Generic TLS server 
No Response

```
4. Banner grabbing from locally created TCP server results in non-printable characters which are replaced with '.'.

```
$ sudo python tcpscan.py -p 1337 127.0.0.1
Host: 127.0.0.1:1337
Type: (1) TCP server-initiated 
Response: 2....345

```

5. Scan port range 20-25 on local host.

```
$ sudo python tcpscan.py -p 20-25 127.0.0.1
Host: 127.0.0.1:22
Type: (1) TCP server-initiated 
Response: SSH-2.0-OpenSSH_9.9p1 Debian-3

```
