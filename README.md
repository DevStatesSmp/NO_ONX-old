![have background](https://github.com/user-attachments/assets/0deb4708-e3a9-4219-85e4-3072af962c90)
(This is invincible title card, btw for fun)<br>

[CHANGELOG](https://github.com/DevStatesSmp/NO_ONX/blob/NO_ONX/CHANGELOG.md)

# NO_ONX
NO_ONX is a lightweight tool but useful to analysis, investigattion, security monitoring for Linux System
## Requirement
- OS: Linux (Ubuntu, Debian, Arch Linux), Window 10+ (can be lower than Window 10)
- Python: 3.1x
- C++17 and C++ Compiler (`g++`) (Note: If you using Window, you don't have to install C++)

## Installation
### Installing Python and C++ (Skip this if you have)<br>
For Ubuntu and Debian:
```bash
sudo apt update
sudo apt install python3 g++
```

For Arch Linux:
```bash
sudo pacman -Sy
sudo pacman -S python python-pip gcc base-devel openssl
```

For Window, you must have to access Python website to download their new release (Ex: 3.14)

### Install required libary
(Note: If you're using Kali Linux, you can skip this step)<br>
For python:
```bash
pip install -r python_requirements.txt # For Linux

pip install -r requirement.txt # for window
```

If using Arch:
```bash
sudo pacman -S python-psutil python-pyfiglet python-distro
```

and C++: (If using Linux)
```bash
sudo apt install build-essential libssl-dev
```


## Install NO_ONX
(Make sure that you have git)<br>
Use git clone:
```bash
git clone https://github.com/DevStatesSmp/NO_ONX
```
(Note: if you're using Window, you should remove the rest of the file and only keep the "window-version" folder.)<br>

Or if you prefer to download a specific version manually, visit the [Releases page](https://github.com/DevStatesSmp/NO_ONX/releases) and download the ZIP or tarball of the version you want.
## How to use

To view version and available command:

```bash
python noonx.py
```

More commands and feature will be added in future, stay tuned!
