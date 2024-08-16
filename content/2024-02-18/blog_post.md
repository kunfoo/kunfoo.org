Title: Running Linux on a HP 255 G10 Notebook
Category: Blog
Date: 2024-02-18
Tags: Komputer
Lang: en
Slug: 

My girlfriend just bought a new HP 255 G10 laptop. The specs are pretty decent:  

- AMD Ryzen 5-7530U
- 16 GB RAM
- 500 GB NVMe SSD

All this for a price of just over 400€. Best of all, I convinced my girlfriend to ditch Windows and give Linux a try. We
installed Kubuntu 23.10 because I wanted to see KDE Plasma in action and it might feel familiar to a long time Windows
user.

Once installed, everything worked as expected. Wifi and Bluetooth, even all the function keys did what they were
supposed to. Even the battery life seems decent, although I haven't tested it much yet.

However, one of my girlfriend's main use cases is listening to music via a Bluetooth speaker. It turned out that both
Wifi and Bluetooth share the same antenna, and the power saving of the Realtek rtw89 driver causes some problems. Also,
according to the [rtw89 Github repository](https://github.com/lwfinger/rtw89), HP (and Lenovo) notebooks don't handle
the PCIe interface correctly.

## Fix PCIe
So the first thing I did, was to put the following line into the file `/etc/modprobe.d/rtw89_pci.conf`:
```
options rtw89_pci disable_aspm_l1=y disable_aspm_l1ss
```
This should fix the problems with the PCIe interface.

## Fix power saving
However, we found that the wifi became extremely slow when a Bluetooth speaker was connected. The latency of a simple
ping went from ~14ms to 500-1000ms or even packet loss. There is a long [issue thread on
Github](https://github.com/lwfinger/rtw89/issues/262) about this. Basically, this is related to power saving. To
mitigate the problem for now, I created a systemd unit that is started after NetworkManager in
`/etc/systemd/system/wifi_powersave.service`:
```
[Unit]
Description=Set WiFi power save %i
After=NetworkManager.service

[Service]
Type=oneshot
ExecStart=/usr/sbin/iw wlo1 set power_save off
ExecStart=/usr/sbin/iw wlp1s0 set power_save off

[Install]
WantedBy=NetworkManager.service
```

This will disable power saving on the wifi interfaces `wlo1` and `wlp1s0`. You should check with `ip link` if your
device is called differently. I included both "real name" and "altname" to be safe. You also need to install the `iw`
package first.

## Final Words
This fixes the network latency issues when both wifi and Bluetooth are connected at the same time. I am sure this is
only temporary as the driver gets better in the future.

Finally, I would like to say that I am really surprised by the build quality of the device. For a little over 400€, it
is better than I expected. The screen is okay, it's matte and bright enough. The plastics of the case don't feel super
cheap and I even found the keyboard good enough to write this very post on it.
