import pyfiglet
import shutil
import sys
import psutil
import platform
import os
import time

# Import source
from src import *
from src.file_info_module import info

# Banner tool
def banner():
    term_width = shutil.get_terminal_size().columns
    ascii = pyfiglet.figlet_format("NO_ONX", font="slant")
    banner_lines = ascii.splitlines()
    max_line_length = max(len(line) for line in banner_lines)

    for line in banner_lines:
        print(f"\033[92m{line.center(term_width)}\033[0m")

    version_str = "v0.1.2a for Window"
    print(" " * (max_line_length - len(version_str)) + f"\033[90m{version_str}\033[0m\n")
    print("\033[96m📖 Usage: python <module_name>.py or python noonx.py <command>\033[0m\n")

# Help 
def help():
    print("""
\033[94mUsage:\033[0m
  \033[92m1.\033[0m python3 noonx.py <command> [arguments]
  \033[92m2.\033[0m python3 [FILE_MODULE_NAME].py

\033[94mCommands:\033[0m
  \033[96m--file_info\033[0m      - Retrieve detailed file information
  \033[96m--file_hash\033[0m    - Retrieve file hash
  \033[96m--dir_info\033[0m     - Retrieve directory information
  \033[96m--symlink_info\033[0m - Retrieve symlink information
  \033[96m--extended_info\033[0m - Retrieve extended file information

\033[94mOptions:\033[0m
  \033[93m--help\033[0m (-h)          - Show help
  \033[93m--system_info\033[0m (-si)  - Check system info
""")
    
def get_gpu_info():
    try:
        gpu_info = os.popen("wmic path win32_VideoController get name").read().split("\n")
        gpu_names = [line.strip() for line in gpu_info if line.strip() and "Name" not in line]
        return ", ".join(gpu_names) if gpu_names else "Unknown"
    except Exception:
        return "Unknown"
    
def get_system_info():
    print("\n\033[1m\033[92m[🔍 SYSTEM INFORMATION]\033[0m\n")
    print(f"\033[96m OS:\033[0m {platform.system()} {platform.version()}")
    print(f"\033[96m RAM:\033[0m {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
    print(f"\033[96m CPU:\033[0m {platform.processor() or 'Unknown'}")
    print(f"\033[96m Cores:\033[0m {psutil.cpu_count(logical=True)} logical / {psutil.cpu_count(logical=False)} physical")
    uptime_min = round((time.time() - psutil.boot_time()) / 60)
    print(f"\033[96m Uptime:\033[0m {uptime_min} minutes")
    print(f"\033[96m Kernel:\033[0m {platform.release()}")
    print(f"\033[96m GPU:\033[0m {get_gpu_info()}")
    print(f"\033[96m Distro ID:\033[0m {platform.system()}, Version: {platform.version()}\n")

def loading_effect(text="Loading modules", dots=3, delay=0.3):
    for _ in range(dots):
        print(f"\r\033[93m{text}{'.' * (_ + 1)}\033[0m", end='', flush=True)
        time.sleep(delay)
    print()

# ==== Main ====
def main():
    banner()
    if len(sys.argv) >= 2:
        arg = sys.argv[1]

        if arg in ('--help', '-h'):
            help()
        elif arg in ('--system_info', '--si'):
            loading_effect("Fetching system info")
            get_system_info()

        elif arg == '--file_info' and len(sys.argv) >= 3:
            info.file_info(sys.argv[2])

        elif arg == '--file_hash' and len(sys.argv) >= 3:
            path = sys.argv[2]
            algo = sys.argv[3] if len(sys.argv) >= 4 else "sha256"
            info.file_hash(path, algo)

        elif arg == '--dir_info' and len(sys.argv) >= 3:
            info.dir_info(sys.argv[2])

        elif arg == '--symlink_info' and len(sys.argv) >= 3:
            info.symlink_info(sys.argv[2])

        elif arg == '--extended_info' and len(sys.argv) >= 3:
            info.extended_info(sys.argv[2])

        else:
            print(f"\033[91m[!] Unknown or incomplete command:\033[0m {' '.join(sys.argv[1:])}")
            print("Run with \033[93m--help\033[0m to see available modules.\n")
    else:
        print("\033[90mTip:\033[0m Use --help for more commands")

if __name__ == "__main__":
    main()