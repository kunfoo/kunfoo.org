Title: Soyo M4Pro Mini PC
Category: Blog
Date: 2025-03-02
Tags: Komputer
Slug: 
Lang: de

Da ich im Internet bisher nur sehr wenige Informationen über den Soyo M4 Pro finden konnte, hier eine kleine
Vorstellung. Der Mini PC hat folgende Spezifikationen:  

- Intel N150 CPU
- 16 GiB RAM  (SODIMM DDR4 3200Mhz von Mougul)
- 512 GiB m.2 SATA SSD (Aosenke AS500 m.2-2280)
- RealTek RTL-8169 Gigabit Ethernet
- RealTek RTL8852BE 802.11ax Wifi6/Bluetooth
- 4 USB-A
- 2x USB-C
- 2x HDMI
- 1x 3,5mm Klinke (vorn)

Wichtig zu wissen ist, dass m.2-SATA-SSDs nicht unterstüzt werden, dazu komme ich aber später nochmal.

Hier ist die komplette Ausgabe von `lspci`:  
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

Der Mini PC kommt in einer schicken schwarzen Kiste und ist gut verpackt. Mit dabei ist ein Netzteil mit 12V und 3A,
also 36W. Leider handelt es sich noch nicht um ein USB-C-Netzteil, sondern um einen Hohlstecker ("barrel plug").

![Verpackung]({static}/2025-03-02/box.jpg)
 
![Verpackung geöffnet]({static}/2025-03-02/box_offen.jpg)

![Soyo M4Pro von oben]({static}/2025-03-02/oben.jpg)

![Netzteil]({static}/2025-03-02/netzteil.jpg)

## Die Innereien

Zum Öffnen des Gehäuses müssen zuerst die Gummifüße entfernt werden. Die kann man einfach mit dem Finger herauspopeln.
Dann braucht man einen kleinen Kreuzschraubenzieher um die 4 Schrauben zu entfernen. Den Plastikdeckel kann man dann mit
dem Fingernagel oder einem dünnen Spachtel heraushebeln. Darunter kommt eine Metallplatte zum Vorschein, die auch
nochmal mit 4 Kreuzschrauben befestigt ist.

![Soyo M4Pro von unten]({static}/2025-03-02/unten_schraube.jpg)

![Innen, Metallplatte]({static}/2025-03-02/metallplatte.jpg)

Wenn auch die Metallplatte entfernt ist, sieht man den RAM und die SSD. Außerdem gibt es einen unbelegten Slot für eine
weitere m.2 NVME SSD in der 2242-Bauform (d.h. 42mm Länge). Achtung, ich habe versucht hier eine m.2 SATA SSD zu
verbauen, die wird jedoch nicht erkannt. Wie wir in der obigen Ausgabe von `lspci` erkennen können, ist kein
SATA-Controller verbaut. **Der Soyo M4Pro unterstützt also nur NVMe/PCIe-SSDs**.

![Soyo M4Pro geöffnet, Blick auf RAM und SSD]({static}/2025-03-02/ram_ssd.jpg)

Unter dem RAM-Riegel befindet sich vermutlich die Bezeichnung des Motherboards/SOC. Eine Internetsuche nach
"AN15-MB-R13" und "CBM-AN15005-01" bringt leider keine hilfreichen Ergebnisse. DY20241213003 bezeichnet wahrscheinlich
das Produktionsdatum, d.h. das Gerät wurde vermutlich am 13.12.2024 hergestellt. Das ist gar nicht lange her und
erscheint plausibel. Laut
[Intel-Webseite](https://www.intel.de/content/www/de/de/products/sku/241636/intel-processor-n150-6m-cache-up-to-3-60-ghz/specifications.html)
wurde der Intel N150 erst im Q1 2025 auf den Markt gebracht.

![Blick auf das Motherboard]({static}/2025-03-02/mobo.jpg)

![Der verbaute WLAN-Adapter von Realtek]({static}/2025-03-02/wlan.jpg)

### Intel N150

Der Prozessor wurde nur minmal gegenüber dem Intel N100 verbessert. Statt 3,4GHz maximaler Taktfrequenz gibt es jetzt
3,6 Ghz. Beide haben 4 Kerne und 6W TDP. Außerdem wurde die Intel-Grafikeinheit leicht verbessert und hat nun 1Ghz
Taktfrequenz statt 750MHz beim Vorgänger.

### USB

Der Soyo M4Pro hat insgesamt 4 USB-A und 2 USB-C-Schnittstellen. `lsusb` meldet folgendes:  
```
Bus 004 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 003 Device 003: ID 0bda:b85b Realtek Semiconductor Corp. Bluetooth Radio
Bus 003 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

Außerdem hier nochmal die relevante Ausgabe von `lspci`:  
```
# lspci | grep -i usb
00:0d.0 USB controller: Intel Corporation Alder Lake-N Thunderbolt 4 USB Controller
00:14.0 USB controller: Intel Corporation Alder Lake-N PCH USB 3.2 xHCI Host Controller
```

Ich gehe daher davon aus, dass die hinteren beiden USB-Ports nur USB 2.0 unterstützen. Die vorderen, blauen USB-Ports
unterstützen vermutlich USB 3.2. Der mit SuperSpeed gelabelte USB-C-Port unterstützt vermutlich Thunderbolt, der andere
lediglich USB 3.2. Getestet habe ich das allerdings nicht.

## Debian GNU/Linux auf dem Soyo M4Pro

Der Soyo M4Pro kommt mit einem vorinstallierten Windows 11. Damit kann ich aber nichts anfangen. Da ich den Mini PC als
Heimserver einsetzen will, habe ich mich entschieden Debian 12 Bookworm zu installieren. Leider hatte ich mit dem
offiziellen Debian-Installer kein Glück. Beim Formatieren der SSD gab es immer wieder Fehler, teilweise ist die
Device-Node (also `/dev/nvme0n1`) verschwunden. Vermutlich ist der Kernel im Installer-Image zu alt für die relativ neue
Hardware.

Debian 12 habe ich per `debootstrap` mit [grml](https://grml.org/) installiert, dazu schreibe ich noch einen separaten
Artikel. An dieser Stelle sei nur soviel verraten, dass mit Kernel 6.12.9 aus dem [Debian
Backports](https://backports.debian.org/) alles wunderbar läuft. Die Firmware für die Realtek LAN-, WLAN- und
Bluetooth-Adapter kommt mit dem `firmware-realtek`-Paket. Für die Firmware der Intel-Grafikeinheit muss das Paket
`firmware-intel-graphics` installiert werden. Beides ist nur im `non-free-firmware`-Repository enthalten, d.h. die
folgende Zeile muss zur `sources.list` von apt hinzugefügt werden:  
```
deb http://deb.debian.org/debian bookworm main non-free-firmware
```

Für alle die sich gerne ein vollständiges Bild über die Hardware machen wollen, habe ich [hier]({static}/2025-03-02/lshw.txt) noch die
komplette Ausgabe von `lshw` abgelegt.
