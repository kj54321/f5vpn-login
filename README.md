# F5 VPN Command-line client

This software allows you to connect to an [F5 Networks](https://f5.com/) VPN server (BIG-IP APM) without using their
proprietary VPN client.

**It is not supported or affiliated with F5 in any way.** I actually find it rather
sad the client they provide is so terribly poor that I had to write this in
order to get reliable access to my company's VPN.

This software does not require any software from F5 to be installed on the
client. The only requirement is Python 3. It works on at least Linux and MacOS
systems, but porting to any similar OS should be trivial. Porting to Windows, on
the other hand, is probably not reasonably possible.

## Setup

The script requires [`ppp`](https://www.samba.org/ppp/). If you are on Linux, install it using your package manager. If you are on MacOS, you already have it.

The script also requires [`netstat`](http://man7.org/linux/man-pages/man8/netstat.8.html), which is generally packaged as ```net-tools```.

## Basic Usage (supports two-factor authentication):

```bash
sudo ./f5vpn-login.py --sessionid=0123456789abcdef0123456789abcdef your.fully.qualified.hostname
```

You can find the session ID by going to the VPN host in a web browser, logging in, and running this JavaScript in Developer Tools:

```javascript
document.cookie.match(/MRHSession=(.*?); /)[1]
```

If your organization does not use 2FA and you are able to log in with just your username and password:

```bash
sudo ./f5vpn-login.py user@host
```

## Auto acquire MRHSession by f5-utls.py

By using chrome webdriver and selenium, you can automate above steps to acuqire MRHSession.
Required packages:
splinter, selenium, stoken

Some parameters in script that need to modify as your wish:
- url, f5 login address 
- username, f5 login username
- pin, 2FA pin if applicable
- chrome_options, your personal chrome profile(optional)

Usage:
```
python3 f5-utils.py
```


## DNS and Routing

- By default, the script will change your DNS servers to the ones provided by the VPN server. Skip this step by by passing the `--skip-dns` option.

- By default, once connected, the script will route all traffic through the newly-created VPN network interface. Skip this step by passing the `--skip-routes` option (your VPN connection will be useless if this option is used, so only use it if you plan to set up the routing table yourself).

- Add --custom-routes (Deprecated)
On Linux System, [VPN routing is recommended under /etc/ppp/ip-up.d](https://tldp.org/HOWTO/PPP-HOWTO/x1455.html), you can write customized script when ppp tunnel established.

Example: 
```
sudo LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libsqlite3.so.0 python3 f5vpn-login.py --sessionid 54fd617b35d8396a8eab2351857de7dc --skip-routes --custom-routes yourcompany.com:8443
```

## Other Info

*user@host is saved for future invocations, so doesn't need to be
specified on future invocations.*

Use **CTRL-C** to exit.

The application will save "user@host" and last session ID in ``~/.f5vpn-login.conf``. In case of problems or for reset the session data simply remove that file.
