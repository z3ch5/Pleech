# Pleech
Pleech is yet another proxy leecher, simple yet full featured and powefull.

# Main features
- Taking proxies from url(s) using regex (regular expression)
- Testing proxies and export them to a file
- Testing working proxies if listed as spammed proxies
- HTTP, SOCKS5, and SOCKS4 types are supported
- Multi-Threading
- Can test the proxies if they work with ircs too
- Timeout option is giving, so that you can take only fast proxies

# Usage
pleech.py [-h] (-u URL | -U FILE | -p IP:PORT | -P FILE) (-f | -t {http,socks4,socks5}) [-c] [-d SEC] [-T THREAD][-i SERVER:PORT] -s FILE [-v] [--version]

  -h, --help            show this help message and exit
  -u URL, --url URL     URL to get proxies from
  -U FILE, --urls-list FILE
                        URLs list file to get proxies from
  -p IP:PORT, --proxy IP:PORT
                        proxy to check, must be as form {ip:port}
  -P FILE, --proxies-list FILE
                        proxies list file to check line by line[first line
                        ip:proxy,2nd line ip2:port2...etc]
  -f, --force           Try to bruteforce proxy type and check which one the
                        proxy is
  -t {http,socks4,socks5}, --type {http,socks4,socks5}
                        Set the proxy type
  -c, --check-listed    check the proxy if listed in opened proxies (abusing
                        list)
  -d SEC, --delay SEC   The timeout while checking proxy and stop the process
                        to the next one {min.sec}, (default is 5.0)
  -T THREAD, --thread THREAD
                        multithreading for faster process
  -i SERVER:PORT, --irc-test SERVER:PORT
                        check the proxy if works as an irc proxy
  -s FILE, --save-list FILE
                        save the working proxies to specific file
  -v, --verbose         show some details (-vv for more)
  --version             show program's version number and exit
  # Example of saved file:
  (proxy):(port):(type):(listed or not):(dely):(url where the proxy took from)
  188.166.110.237:8080:socks5:False(didn't apply -c):5.0:http://www.socks-proxy.net/
  
  # TO-DO
  - Leeching proxies from websites based on image processing.
  - changeable User-Agent.
  - changeable accuracy.
