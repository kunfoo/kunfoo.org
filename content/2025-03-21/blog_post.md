Title: Encrypted Debian by debootstrap
Category: Blog
Date: 2025-03-21
Tags: Komputer
Slug: 
Lang: en

I would like to explain how I installed Debian on an encrypted file system on my Soyo M4Pro. Surprisingly, I did not
find a similar guide on the internet, but maybe I did not search very well. Anyway, here is how:

I used the fantastic [grml](https://grml.org/) live distribution to boot a Debian-like system. Just download the ISO and write it to a USB
drive using something like `dd if=grml.iso of=/dev/usb-drive status=progress`.

Once you have booted grml, I recommend creating another partition on the USB drive and saving the following shell
script: 

```bash
#!/bin/bash

cryptsetup open /dev/nvme0n1p3 crypt-root

mount /dev/mapper/crypt-root /mnt
mount /dev/nvme0n1p2 /mnt/boot
mount /dev/nvme0n1p1 /mnt/boot/efi

mount --bind /sys /mnt/sys
mount --bind /dev /mnt/dev
mount --bind /dev/pts /mnt/dev/pts
mount --bind /proc /mnt/proc
mount -t efivarfs efivarfs /mnt/sys/firmware/efi/efivars

chroot /mnt /bin/bash
```

You will find this useful because, in my experience, you may have to reboot grml a few times because you forgot
something. Also, this guide may be incomplete, as I am writing it based on my memories and some notes I took during the
process.

## Partitioning

First, we need to partition the storage device. I only have one NVMe drive installed, which is called `/dev/nvme0n1`. We
will create an unencrypted partition for `/boot`, which will also contain the EFI partition. The rest will be on a large
additional partition. If you want to use suspend to disk, aka hibernate, you will need an additional swap partition that
is slightly larger than the amount of RAM you have installed (16 GiB on the Soyo M4Pro). I don't use swap because 16 GiB
of RAM ought to be enough for anybody.

```bash
cfdisk /dev/nvme0n1
# create 1GiB partition /dev/nvme0n1p1, type EFI System
# create 1GiB partition /dev/nvme0n1p2, type Linux file system
# create another partition /dev/nvme0n1p3, type Linux file system
```

Now we setup the encrypted main partition:

```bash
cryptsetup luksFormat /dev/nvme0n1p3
# type your password

cryptsetup open /dev/nvme0n1p3 crypt-root
# type your password
```

This will create a new device node `/dev/mapper/crypt-root`. Now we create the file systems. I use ext2 for `/boot`,
which is kind of old school, and ext4 for the main partition. Feel free to use the file system of your choice. However,
we need to use FAT32 for the EFI partition.

```bash
mkfs.vfat -F 32 /dev/nvme0n1p1
mkfs.ext2 /dev/nvme0n1p2
mkfs.ext4 /dev/mapper/crypt-root
```

## Installation

Now we mount everything to `/mnt` and run debootstrap.

```
mount /dev/mapper/crypt-root /mnt

mkdir /mnt/boot
mount /dev/nvme0n1p2 /mnt/boot

mkdir /mnt/boot/efi
mount /dev/nvme0n1p1 /mnt/boot/efi

debootstrap --arch=amd64 bookworm /mnt
```

Voila, we have a Debian installation. Don't try to boot the installation though, we're not done yet. To do the rest of
the installation, we need to chroot into our new installation. To do this, we need to mount some special file systems in
our installation directory.

```bash
mount --bind /sys /mnt/sys
mount --bind /dev /mnt/dev
mount --bind /dev/pts /mnt/dev/pts
mount --bind /proc /mnt/proc
mount -t efivarfs efivarfs /mnt/sys/firmware/efi/efivars

chroot /mnt /bin/bash
```

You may need to edit `/etc/resolv.conf` to get DNS to work. You should now be able to run `apt update` and `apt install
vim` (or your editor of choice). The problem with the official Debian installer on the Soyo M4Pro was that the kernel
shipped with Debian Bookworm seemed to be too old. To get a newer kernel, we use Debian backports. Feel free to skip
this step if you don't need a newer kernel.

```
echo 'deb http://deb.debian.org/debian bookworm-backports main' > /etc/apt/sources.list.d/backports.list
```

Unfortunately, we also need to install non-free firmware for the ethernet/wifi/bluetooth driver and the Intel graphics.
Since Debian does not ship non-free firmware in the main archive, we need to add the `non-free-firmware` archive to
`/etc/apt/sources.list`, like this

```bash
deb http://deb.debian.org/debian bookworm main non-free-firmware
```

After updating the package index, we can install the firmware.

```bash
apt update
apt install -t bookworm-backports linux-image-amd64 firmware-realtek firmware-intel-graphics
```

We also need a boot loader and cryptsetup to unlock the file system at boot time. I used grub as the bootloader and
installed it from backports. There is no newer cryptsetup version in backports, so I installed it from main.

```bash
apt install cryptsetup cryptsetup-initramfs
apt install -t bookworm-backports grub-efi
```

## Post installation

Now that we have all the necessary software installed, you might think we are done. In fact, this is only where the
tricky part begins. We need to do some additional plumbing to make the system bootable. Also, we haven't dealt with fun
stuff like localization, time zones, or users yet. Again, take the following with a grain of salt, as I am only writing
this from my notes. But it should give you a good idea.

First, we need to tell the system which file systems we need to mount. You can look up the UUIDs of your file systems with
`lsblk -f`. Create an `/etc/fstab` that looks something like this:

```bash
# <file sysytem> <mount point> <type> <options> <dump> <pass>
UUID=57f13bb6-b5cf-4420-ae37-7814320f26ed /boot ext2 defaults 0 2
UUID=9AE3-3961                            /boot/efi vfat defaults 0 2
# /dev/mapper/crypt-root
UUID=db568b93-9c7a-4512-b653-b113d16467c0  / ext4 errors=remount-ro 0 1
```

We also need to create `/etc/crypttab`, to tell `cryptsetup` about your encrypted file system and how it should be
mapped. It should look something like this:

```
# <target> <device> <key file> <options>
crypt-root UUID=597d2191-f966-4ac0-8450-992b86683bab none luks,discar
```

Now we want to install the boot loader on the EFI partition. Make sure the efivars pseudo filesystem is mounted and
install grub to `/dev/nvme0n1`. It also doesn't hurt to create the initramfs containing cryptsetup, your fstab and
crypttab if it hasn't already been created. Finally, we need to run `update-grub` to create a grub config. 

```bash
mount | grep efivars || mount -t efivarfs efivarfs /mnt/sys/firmware/efi/efivars
grub-install /dev/nvme0n1
update-initramfs -c -k all
update-grub
```

The system should now be bootable. However, you don't have a user to log in to your shiny new system. You may also be
missing some other parts. Here are a few things you might want to install, run, or try:

```bash
# set the password for the root user
passwd

# install some useful packages
apt install bash-completion console-setup locales man-db byobu ssh sudo

# set timezone
dpkg-reconfigure tzdata

# set hostname
vim /etc/hostname

# configure locales, I recommend at least "en_US.UTF-8 UTF-8"
vim /etc/locale.gen
locale-gen
echo 'LC_ALL=en_US.UTF-8' >> /etc/environment

# create your user
useradd -m your-user -s /bin/bash
adduser your-user sudo
passwd your-user
```

Regarding networking, the following may be useful. First, use `ip -br l` to check what your network adapter is called
(mine is `enp1s0`).

```bash
cat > /etc/hosts << HEREDOC
127.0.0.1 localhost
127.0.1.1 $(cat /etc/hostname)

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
HEREDOC

cat > /etc/systemd/network/enp1s0.network << HEREDOC
[Match]
Name=enp1s0

[Network]
DHCP=yes
HEREDOC

systemctl enable --now systemd-networkd.service
```

## Final words

Finally, it's time to boot into your new system.

The following links helped me and might also be useful for you in your debootstrapping endeavours:

- [Switch Debian from legacy to UEFI boot mode](https://web.archive.org/web/20250121115253/https://blog.getreu.net/projects/legacy-to-uefi-boot/)
- [Instructions how to install Debian using debootstrap](https://web.archive.org/web/20250308002224/https://gist.github.com/varqox/42e213b6b2dde2b636ef)
