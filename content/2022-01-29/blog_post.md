Title: Goodbye NetworkManager. Hello decent network configuration
Category: Blog
Date: 2022-01-29
Tags: Komputer
Lang: en
Slug: goodbye-networkmanager

I was recently experiencing problems with the wireless interface on my Debian 11 home server. The connection was very
instable and I could observe `rtlwifi: AP off, try to reconnect now` entries in the kernel log. My first thought was a
power management issue with my wireless adapter, so I put
```
options rtl8188ee swenc=1 ips=0 swlps=0 fwlps=0 aspm=0
```

into `/etc/modprobe.d/rtl8188ee.conf`. However, this did not solve the problem.

## iwd
Somewhere I read that it might be NetworkManager's fault, so I decided to give [iwd](https://iwd.wiki.kernel.org/) (iNet
Wireless Daemon) a try. The setup couldn't be easier, and as always, [the Arch Wiki has a very good
documentation](https://wiki.archlinux.org/title/Iwd). First disable NetworkManager and enable iwd:
```
# systemctl disable --now NetworkManager.service
# systemctl enable --now iwd.service
```

Then, just connect to your wireless network using `iwctl station $IWDEV connect $YOURSSID`. The credentials are stored
in `/var/lib/iwd/$SSID.psk` and the connection will be established automatically the next time you boot. That's it for
the wireless connection. However iwd is not particulary good at configuring your network interfaces with irrelevant
details like an IP address. For example, IPv6 is disabled by default (wtf, it's 2022 guys). Even after I manually
enabled IPv6, I couldn't really get it to work as expected. So I decided to use systemd-networkd for this.

## systemd-networkd
As I already disabled NetworkManager, it couldn't interfere with systemd-networkd. However, your mileage may vary. Make
sure there is no `/etc/network/interfaces*`, netplan or anything else also trying to configure your network interface.
The configuration goes to `/etc/systemd/network/wireless.network` in my case, and is quite straight forward:
```
[Match]
# Name=wlan0
Type=wlan

[Network]
DHCP=ipv4
IgnoreCarrierLoss=true
IPv6AcceptRA=true

[IPv6AcceptRA]
UseDNS=false

[DHCPv4]
UseDNS=false
```

As I only have one wireless interface, I decided to use `Type=wlan`, but it's also perfectly fine to specify the
wireless interface. Again have a look at the great [Arch Wiki documentation on
systemd-networkd](https://wiki.archlinux.org/title/Systemd-networkd) or `man systemd.network` for details.
Then enable systemd-networkd by `systemctl enable --now systemd-networkd.service`. As I wanted to play with DNS over
TLS, I decided to put `UseDNS=false` in there and use systemd-resolved for DNS.

## systemd-resolved
I just found out that the VPN provider [Mullvad offers free ad-blocking DoT-ready DNS
servers](https://mullvad.net/en/help/dns-over-https-and-dns-over-tls/). [The german Wikipedia also has a list of
DoT-ready DNS servers for you.](https://de.wikipedia.org/wiki/DNS_over_TLS#%C3%96ffentliche_DNS-Server) The DNS
configuration goes to `/etc/systemd/resolved.conf` and effectively just looks like this in my case:
```
[Resolve]
DNS=2a07:e340::3#adblock.doh.mullvad.net 194.242.2.3#adblock.doh.mullvad.net 193.19.108.3#adblock.doh.mullvad.net
DNSOverTLS=yes
FallbackDNS=2a00:f826:8:1::254 2a01:4f8:1c0c:82c0::1 94.247.43.254 88.198.92.222 
```

If DoT on the Mullvad servers does not work for whatever reason, I fallback to using DNS servers of the [OpenNIC
project](https://servers.opennic.org/). systemd-resolved has some fallback servers from Cloudflare, Google and Quad9
builtin, but I don't want to use them, even in case.

After enabling systemd-resolved (run `systemctl enable --now systemd-resolved.service`) you can already resolve your
first domain names securely and ad-free. For example try `resolvectl query analytics.google.com`. Oh no, Google
Analytics resolves to 0.0.0.0, that's sad, isn't it? However, you will notice that other DNS resolvers on your system
don't respect your wishes for an ad-free world and happily resolve domain names using whatever nameserver is configured
in your legacy `/etc/resolv.conf`. systemd-resolved provides a stub dns resolver listening on localhost:53 for this and
you can configure it system-wide by symlinking to a pseudo resolv.conf like this:
```
# rm /etc/resolv.conf
# ln -s /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf
```

## Conclusion
I am happy to say, that I finally have a stable wireless connection on my home server, thanks to iwd and
systemd-networkd. As a plus, I am now enjoying an ad-free and privacy-friendly DNS experience. Nice :)
