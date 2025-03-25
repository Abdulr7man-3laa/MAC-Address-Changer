# MAC Address Changer 🖥️🔧

## 🌟 Overview

A Python script for changing network interface MAC addresses on Linux systems. Allows users to modify MAC addresses with robust validation and interface detection.

## ✨ Features

- 🔍 Detect available network interfaces
- 🔄 Change MAC address for specified interface
- 🛡️ MAC address format validation
- 📋 Informative interface listing
- 🔒 Safe interface handling (down/up)

## 🚀 Prerequisites

- Python 3.x
- Linux Operating System
- Root/Sudo privileges
- `subprocess` module
- `optparse` module

## 💻 Usage

```bash
sudo python Mac_Changer.py -i <interface> -m <new_mac_address>
```

### Examples

- List interfaces: `sudo python Mac_Changer.py`
- Change MAC: `sudo python Mac_Changer.py -i eth0 -m 00:11:22:33:44:55`

## 🛠️ Command-line Options

|Option|Description|
|---|---|
|`-i`, `--interface`|Specify network interface|
|`-m`, `--mac`|Specify new MAC address|
|`-h`, `--help`|Show help information|

## ⚠️ Important Notes

- Requires root/sudo permissions
- Works on Linux systems with `ifconfig`
- Temporarily disables network interface during change
