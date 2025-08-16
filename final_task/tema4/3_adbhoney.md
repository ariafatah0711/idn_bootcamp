# adb honey
- [github.com/huuck/ADBHoney](https://github.com/huuck/ADBHoney)
- [github.com/pieterbork/ADBHoney](https://github.com/pieterbork/ADBHoney)

- port 5555

## setup
```bash
git clone https://github.com/huuck/ADBHoney
cd ADBHoney
```

### python
```bash
nohup python3 run.py &
```

### docker
```cd docker```
```bash
docker-compose up --build -d
```
atau
```bash
docker build -t adbhoney:latest .
docker run --name adbhoney --rm -p 5555:5555 -v $(pwd)/adbhoney.cfg:/etc/adbhoney.cfg adbhoney:latest
```

> You will probably want to save uploads and logs to the host machine, so add these volumes to the run command above -v $(pwd)/dl:/ADBHoney/dl -v $(pwd)/logs:/ADBHoney/logs

### pip
```bash
pip install adbhoney
adbhoney
```

### custom config
```bash
cat << EOF > adbhoney/responses.py
cmd_responses = {
    "ls": """acct
bt_firmware
bugreports
cache
charger
config
data
dev
dsp
etc
firmware
mnt
oem
persist
proc
sdcard
storage
system
vendor
""",

    "pwd": "/data/data\n",

    "id": "uid=2000(shell) gid=2000(shell) groups=1004(input),1007(log),1011(adb),1028(sdcard_rw)\n",

    "whoami": "shell\n",

    "uname -a": "Linux localhost 4.14.190-g1234567 #1 SMP PREEMPT armv8l Android\n",

    "cat /proc/version": "Linux version 4.14.190-g1234567 (android-build@google.com) (Android clang version 9.0.8) #1 SMP PREEMPT\n",

    "getprop": """[ro.build.version.release]: [10]
[ro.build.version.sdk]: [29]
[ro.product.model]: [Pixel 3]
[ro.product.manufacturer]: [Google]
""",

    "ps": """USER      PID   PPID  VSIZE  RSS   WCHAN            PC  NAME
root      1     0     752   552   SyS_epoll_ 00000000 S /init
root      2     0     0     0     kthreadd   00000000 S kthreadd
shell   1234  100   34567  2048  SyS_epoll_ 00000000 S sh
""",

    "ifconfig": """wlan0: ip 192.168.1.100  mask 255.255.255.0  up
lo: ip 127.0.0.1  mask 255.0.0.0  up
"""
}
EOF
```

## testing
```bash
adb devices

adb connect <ip>:<port>
adb disconnect <ip>:<port>

adb -s <ip>:<port> shell
adb shell ls

echo test > test.txt
adb push test.txt /test.txt
```
