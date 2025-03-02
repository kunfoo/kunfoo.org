Title: Soyo M4Pro Mini PC
Category: Blog
Date: 2025-03-02
Tags: Komputer
Slug: 
Lang: en

Since I was only able to find very little information about the Soyo M4 Pro on the internet, here is a brief
review. The mini PC has the following specifications:

- Intel N150 CPU
- 16 GiB RAM  (SODIMM DDR4 3200Mhz von Mougul)
- 512 GiB m.2 SATA SSD (Aosenke AS500 m.2-2280)
- RealTek RTL-8169 Gigabit Ethernet
- RealTek RTL8852BE 802.11ax Wifi6/Bluetooth
- 4 USB-A
- 2x USB-C
- 2x HDMI
- 1x 3,5mm Klinke (vorn)

It is important to know that m.2 SATA SSDs are not supported, but I will come back to that later.

Here is the complete output of `lspci`:
```
00:00.0 Host bridge: Intel Corporation Device 461c
00:02.0 VGA compatible controller: Intel Corporation Alder Lake-N [Intel Graphics]
00:04.0 Signal processing controller: Intel Corporation Alder Lake Innovation Platform Framework Processor Participant
00:08.0 System peripheral: Intel Corporation Device 467e
00:0a.0 Signal processing controller: Intel Corporation Platform Monitoring Technology (rev 01)
00:0d.0 USB controller: Intel Corporation Alder Lake-N Thunderbolt 4 USB Controller
00:14.0 USB controller: Intel Corporation Alder Lake-N PCH USB 3.2 xHCI Host Controller
00:14.2 RAM memory: Intel Corporation Alder Lake-N PCH Shared SRAM
00:15.0 Serial bus controller: Intel Corporation Device 54e8
00:15.1 Serial bus controller: Intel Corporation Device 54e9
00:15.2 Serial bus controller: Intel Corporation Device 54ea
00:15.3 Serial bus controller: Intel Corporation Device 54eb
00:16.0 Communication controller: Intel Corporation Alder Lake-N PCH HECI Controller
00:19.0 Serial bus controller: Intel Corporation Device 54c5
00:19.1 Serial bus controller: Intel Corporation Device 54c6
00:1a.0 SD Host controller: Intel Corporation Device 54c4
00:1c.0 PCI bridge: Intel Corporation Device 54bb
00:1c.6 PCI bridge: Intel Corporation Alder Lake-N PCI Express Root Port
00:1d.0 PCI bridge: Intel Corporation Alder Lake-N PCI Express Root Port
00:1e.0 Communication controller: Intel Corporation Alder Lake-N Serial IO UART Host Controller
00:1e.2 Serial bus controller: Intel Corporation Device 54aa
00:1e.3 Serial bus controller: Intel Corporation Device 54ab
00:1f.0 ISA bridge: Intel Corporation Alder Lake-N PCH eSPI Controller
00:1f.3 Multimedia audio controller: Intel Corporation Alder Lake-N PCH High Definition Audio Controller
00:1f.4 SMBus: Intel Corporation Alder Lake-N SMBus
00:1f.5 Serial bus controller: Intel Corporation Alder Lake-N SPI (flash) Controller
01:00.0 Ethernet controller: Realtek Semiconductor Co., Ltd. RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller (rev 15)
02:00.0 Network controller: Realtek Semiconductor Co., Ltd. RTL8852BE PCIe 802.11ax Wireless Network Controller
03:00.0 Non-Volatile memory controller: MAXIO Technology (Hangzhou) Ltd. NVMe SSD Controller MAP1202 (rev 01)
```

## Unboxing

The Mini PC comes in a stylish black box and is well packaged. It includes a 12V and 3A, i.e. 36W, power supply.
Unfortunately, it is not yet a USB-C power supply, but a barrel plug.

![Packaging]({static}/2025-03-02/box.jpg)
 
![Opened packagin]({static}/2025-03-02/box_offen.jpg)

![Soyo M4Pro top view]({static}/2025-03-02/oben.jpg)

![Power supply]({static}/2025-03-02/netzteil.jpg)

## The innards

To open the case, the rubber feet must first be removed. These can be easily popped out with your finger. Then you need
a small Phillips screwdriver to remove the four screws. The plastic cover can then be levered out with a fingernail or a
thin spatula. Underneath, a metal plate comes into view, which is also attached with four Phillips screws.

![Soyo M4Pro from below]({static}/2025-03-02/unten_schraube.jpg)

![Inside, metal plate]({static}/2025-03-02/metallplatte.jpg)

Once the metal plate is removed, you can see the RAM and the SSD. There is also an empty slot for another m.2 NVME SSD
in the 2242 format (i.e. 42mm long). Note that I tried to install an m.2 SATA SSD here, but it is not recognized. As we
can see in the above output of `lspci`, no SATA controller is installed. **So the Soyo M4Pro only supports NVMe/PCIe
SSDs.**

![Opened Soyo M4Pro, viewing RAM and SSD]({static}/2025-03-02/ram_ssd.jpg)

What you find under the RAM slot is probably the name of the motherboard/SOC. Unfortunately, an Internet search for
"AN15-MB-R13" and "CBM-AN15005-01" does not yield any helpful results. DY20241213003 probably indicates the production
date, i.e. the unit was probably manufactured on December 13, 2024. That's not that long ago and seems plausible.
According to [Intel's
website](https://www.intel.de/content/www/de/de/products/sku/241636/intel-processor-n150-6m-cache-up-to-3-60-ghz/specifications.html),
the Intel N150 was introduced in Q1 2025.

![View of the motherboard]({static}/2025-03-02/mobo.jpg)

![Wifi adapter by Realtek]({static}/2025-03-02/wlan.jpg)

### Intel N150

The processor has only been minimally improved compared to the Intel N100. Instead of 3.4GHz maximum clock speed, there
is now 3.6Ghz. Both have 4 cores and 6W TDP. In addition, the Intel graphics unit has been slightly improved and now has
1Ghz clock speed instead of 750MHz for its predecessor.

### USB

The Soyo M4Pro has a total of 4 USB-A and 2 USB-C ports. `lsusb` reports the following:  
```
Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 003 Device 003: ID 0bda:b85b Realtek Semiconductor Corp. Bluetooth Radio
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

Furthermore, here is the relevant output from `lspci` again:  
```
# lspci | grep -i usb
00:0d.0 USB controller: Intel Corporation Alder Lake-N Thunderbolt 4 USB Controller
00:14.0 USB controller: Intel Corporation Alder Lake-N PCH USB 3.2 xHCI Host Controller
```

I therefore assume that the two USB ports at the back only support USB 2.0. The front, blue USB ports probably support
USB 3.2. The USB-C port labeled SuperSpeed probably supports Thunderbolt, the other one only USB 3.2. However, I have
not tested this.

## Debian GNU/Linux auf dem Soyo M4Pro

The Soyo M4Pro comes with a preinstalled Windows 11. But I can't do anything with that. Since I want to use the mini PC
as a home server, I decided to install Debian 12 Bookworm. Unfortunately, I had no luck with the official Debian
installer. When formatting the SSD, there were always errors, sometimes the device node (i.e. `/dev/nvme0n1`)
disappeared.  Probably the kernel in the installer image is too old for the relatively new hardware.

I installed Debian 12 via `debootstrap` using [grml](https://grml.org/), and I will write a separate article about this.
At this point, I will only reveal that everything works fine with kernel 6.12.9 from [Debian
Backports](https://backports.debian.org/). The firmware for the Realtek LAN, Wifi and Bluetooth adapters come with the
`firmware-realtek` package. For the firmware of the Intel graphics unit, the `firmware-intel-graphics` package must be
installed. Both are only available in the `non-free-firmware` repository, i.e. the following line must be added to apt's
`sources.list`:
```
deb http://deb.debian.org/debian bookworm main non-free-firmware
```

For those who would like to get a complete picture of the hardware, I have stored the output of `lshw` [here]({static}/2025-03-02/lshw.txt).

*Translated with [DeepL](https://www.deepl.com/)*
