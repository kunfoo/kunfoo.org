# Schnipsel

## apt/dpkg
- `apt-file search $FILE`
- `dpkg -S $FILE`

## adb
- `adb shell am stack list`
- `adb shell 'su -c /data/local/tmp/frida-server -D'`

## awk
- `awk -F ',' '{ print $1 "\t" $NF}'`
    - print the first and the last column, separated by tab, use field separator ","
- `awk '{ if ($3 == "something") print}'`
    - print if condition is met

## capabilities
- `setcap all+eip /path/to/$BINARY`
    - assign all capabilities (in the effective, inheritable and permitted sets) to $BINARY
- setpriv --bounding-set +all --ambient-caps +all --inh-caps +all $BINARY
    - run $BINARY with all capabilities

## curl
- `curl --resolve ccc.de:443:127.0.0.1 -k https://ccc.de`
    - resolve ccc.de to localhost address and don't check certificate

## docker
- `docker run -it debian`
- `docker run -it --mount type=bind,source=/some/dir,target=/mnt/foo debian`
- `docker start -ai $CONTAINER`
- `docker exec -it $CONTAINER /bin/bash`

## find
- `find . -perm -a+w -type d,f -ls`
    - find and list world-writable files and directories in cwd and subdirectories
- `find /usr -type f \( -perm -04000 -o -perm -02000 \)`
    - find suid/sgid executables in /usr and subdirectories

## grep
- `grep -v -f file1 file2`
    - find lines in file2 that are not in file1

## iptables
- `iptables -L | grep Chain`
    - list all chains
- `iptables -n -L INPUT`
- `iptables -S INPUT`
    - list all rules of the INPUT chain
- `iptables -vnL FORWARD --line-numbers`
    - list rules of the FORWARD chain with line numbers and packet counters
- `iptables -D FORWARD 23`
    - delete rule 23 in FORWARD chain
- `iptables -Z INPUT 42`
    - reset packet counter for rule 42 in INPUT chain
- `iptables -F OUTPUT`
    - delete all rules in the OUTPUT chain (flush)

## jq
- `jq -r '.[].ip' foo.json`
    - get field "ip" from json-formatted data

## k8s
- kubectl get pods -n $NAMESPACE
- kubectl get pods -n $NAMESPACE --show-labels
- kubectl get pod -n $NAMESPACE $POD -o yaml
- kubectl -n $NAMESPACE logs $POD --all-containers=true --since=5m
- kubectl run -n $NAMESPACE $POD --image=$IMAGE --command -- /bin/bash -c 'while :; do sleep 60; done'
- kubectl apply -f $YAML
    - get from `kubectl get ... -o yaml`
- kubectl exec -it $POD -- /bin/bash
- kubectl delete pod $POD
- kubectl attach $POD -c $CONTAINER -it
- kubectl port-forward $POD $PORT
- kubectl get events
- kubectl auth can-i --list
- kubectl label pods -n $NAMESPACE $POD {foo=bar,name=crazycat}

### cilium
- `kubectl get ciliumnetworkpolicies.cilium.io -n $NAMESPACE $NETWORK_POLICY -o yaml`
- `kubectl delete ciliumnetworkpolicies.cilium.io -n $NAMESPACE $NETWORK_POLICY`
- [Network Policy Editor](https://editor.cilium.io/)

## mdadm
- `mdadm --auto-detect`
- `mdadm --assemble --scan`
- `mdadm --detail /dev/md0`

## misc
- `iconv -f utf-16 -t utf-8 $FILE`
    - convert utf-16 encoded file to utf-8
- `podman run -it ubuntu`
- `mount.cifs //$HOST/$SHARE /$MNT/$POINT -o user=$USER,uid=1000`
- `mount -t nfs $HOST:/$SHARE /$MNT/$POINT
- `gpg -c --cipher-algo AES256 $FILE`
- `echo 100 | sudo tee /sys/class/backlight/amdgpu_bl0/brightness`
- `pandoc -t slidy -o presentation.html -s presentation.md`
- `update-alternatives --list editor`
    - list alternatives for `editor`
- `update-alternatives --set editor /usr/bin/vim.basic`
    - set `/usr/bin/vim.basic` as alternative for `editor`

## nft
- `nft list ruleset`
    - list all rules

## nmap
- `nmap -sS -sV -p0-65535 -iL list.txt`
    - do a syn scan and version scan of all tcp ports on hosts listed in list.txt
- `nmap --script \*ms-sql\* -p 1433 some.host.tld`
    - run all ms-sql scripts (scripts are located in `/usr/share/nmap/scripts/`)
- `--max-retries 2`
    - decrease retries, if a probe times out (default 10, or if _magic_ applies only 1)

## openssl
- `openssl x509 -in /tmp/cert.der -inform der -text -noout`
- `openssl x509 -in /tmp/cert.der -inform der -outform pem -out /tmp/cert.pem`
- `openssl rsa -in /tmp/key.der -inform der -check -noout -text`

## ps
- `ps auxwww`
    - list all processes, including the complete cmdline
```
ps faux
ps axjf
pstree
```
    - show processes as a tree

## ssh
- `ssh -NfL 8080:localhost:1337 user@host.tld`
    - make remote port 1337 accessible on port 8080 on local side and go to background (do not present a remote shell)
- `ssh user@host sudo tcpdump -i wlan0 -w - | wireshark -k -i -`
    - run tcpdump on remote host and pipe traffic to local wireshark instance
- `ssh-keygen -r $HOST\_FQDN`
    - generate sshfp dns records
- `ssh-keygen -l -E sha256 -f /etc/ssh/id\_ed25519.pub`
    - print host key fingerprint as shown upon first connection

## sqlmap
- `sqlmap --proxy=http://localhost:8080 -r request.txt --ignore-code 401 --dbms postgresql`
    - run sqlmap through Burp and use a recorded request file, which has injection marker \* included

## systemd
- `systemd-run --on-calendar="2023-01-01 01:00:00 UTC" systemctl reboot`
    - schedule reboot at certain point in time

## tmux
- `tmux -S $SESSION ls`
    - list tmux sessions on socket $SOCKET as defined by byobu -S $SESSION
- `tmux -S $SESSION attach -t $NUM`
    - attach to tmux session $NUM on socket $SOCKET

## vim
- `:g/pattern/d`
    - delete all lines matching pattern
- `:g!/pattern/d`
    - delete all lines NOT matching pattern
- `"\*y`
    - copy to clipboard (the \* buffer)

## xrandr
- `cvt 1920 1080 60`
- `xrandr --newmode 1920x1080 173.00 1920 2048 2248 2576 1080 1083 1088 1120 -hsync +vsync`
- `xrandr --addmode Virtual1 1920x1080`
- `xrandr --output Virtual1 --mode 1920x1080`

## yum/dnf/rpm
- `yum whatprovides $FILE`
    - search for packet which installs $FILE
- `rpm -qf $FILE`
    - tell which packet installed $FILE
