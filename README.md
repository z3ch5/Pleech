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
``` shell
pleech.py [-h] (-u URL | -U FILE | -p IP:PORT | -P FILE) (-f | -t {http,socks4,socks5}) [-c] [-d SEC] [-T THREAD][-i SERVER:PORT] -s FILE [-v] [--version]
```
  `-h, --help`<br />show this help message and exit<br />
  `-u URL, --url URL`<br />URL to get proxies from<br />
  `-U FILE, --urls-list FILE`<br />URLs list file to get proxies from<br />
  `-p IP:PORT, --proxy IP:PORT`<br />proxy to check, must be as form {ip:port}<br />
  `-P FILE, --proxies-list FILE`<br />proxies list file to check line by line[first line ip:proxy,2nd line ip2:port2...etc]<br />
  `-f, --force`<br />Try to bruteforce proxy type and check which one the proxy is<br />
  `-t {http,socks4,socks5}, --type {http,socks4,socks5}`<br />Set the proxy type<br />
  `-c, --check-listed`<br />check the proxy if listed in opened proxies (abusing list)<br />
  `-d SEC, --delay SEC`<br />The timeout while checking proxy and stop the process to the next one {min.sec}, (default is 5.0)<br />
  `-T THREAD, --thread THREAD`<br />multithreading for faster process<br />
  `-i SERVER:PORT, --irc-test SERVER:PORT`<br />check the proxy if works as an irc proxy<br />
  `-s FILE, --save-list FILE`<br />save the working proxies to specific file<br />
  `-v, --verbose`<br />show some details (-vv for more)<br />
  `--version`<br />show program's version number and exit<br />
  
  # Example of saved file:
  (proxy):(port):(type):(listed or not):(dely):(url where the proxy took from)<br />
  188.166.110.212:8080:socks5:False:5.0:http://www.proxyurl.net/
  
  # TO-DO
  - Leeching proxies from websites based on image processing.
  - Changeable User-Agent.
  - Changeable accuracy.
