import pyfiglet
import subprocess
import shutil
import sys
import distro
import psutil
import platform
import os
import time

# ==== Style & Banner ====
def print_banner():
    term_width = shutil.get_terminal_size().columns
    ascii_banner = pyfiglet.figlet_format("NO_ONX", font="slant")
    banner_lines = ascii_banner.splitlines()
    max_line_length = max(len(line) for line in banner_lines)

    # Green ANSI for a hacker feel
    for line in banner_lines:
        print(f"\033[92m{line.center(term_width)}\033[0m")

    version_str = "v0.1.2 beta"
    print(" " * (max_line_length - len(version_str)) + f"\033[90m{version_str}\033[0m\n")
    print("\033[96m📖 Usage: python3 <module_name>.py or python3 noonx.py <command>\033[0m\n")

# ==== Help Menu ====
def show_help():
    print("""
\033[94mUsage:\033[0m
  \033[92m1.\033[0m python3 noonx.py <command>
  \033[92m2.\033[0m python3 [FILE_MODULE_NAME].py

\033[94mModules:\033[0m
  \033[96mdetective\033[0m      - Monitor file & system changes
  \033[96mreadfile\033[0m       - Read file content

\033[94mScanning:\033[0m
  \033[96mnetwork_scan\033[0m   - Scan ports or network issues
  \033[96mfile_scan\033[0m      - Scan files for threats
  \033[96mmalware_scan\033[0m   - Malware signature scanner

\033[94mOptions:\033[0m
  \033[93m--help\033[0m (-h)          - Show help
  \033[93m--system_info\033[0m (-si)  - Check system info
""")

# ==== System Info Module ====
def get_gpu_info():
    try:
        with os.popen("lspci | grep VGA") as f:
            return f.read().strip()
    except Exception as e:
        return f"Could not retrieve GPU info: {e}"

def get_system_info():
    print("\n\033[1m\033[92m[🔍 SYSTEM INFORMATION]\033[0m\n")
    print(f"\033[96m🖥️  OS:\033[0m {distro.name(pretty=True)}")
    print(f"\033[96m🧠  RAM:\033[0m {round(psutil.virtual_memory().total / (1024**3), 2)} GB")
    print(f"\033[96m🔢 CPU:\033[0m {platform.processor() or 'Unknown'}")
    print(f"\033[96m⚙️  Cores:\033[0m {psutil.cpu_count(logical=True)} logical / {psutil.cpu_count(logical=False)} physical")
    uptime_min = round((time.time() - psutil.boot_time()) / 60)
    print(f"\033[96m🕒 Uptime:\033[0m {uptime_min} minutes")
    print(f"\033[96m🧾 Kernel:\033[0m {platform.release()}")
    print(f"\033[96m🖼️  GPU:\033[0m {get_gpu_info()}")
    print(f"\033[96m🔍 Distro ID:\033[0m {distro.id()}, Version: {distro.version()}\n")

# Optional: Fake "hacker-style" loading
def loading_effect(text="Loading modules", dots=3, delay=0.3):
    for _ in range(dots):
        print(f"\r\033[93m{text}{'.' * (_ + 1)}\033[0m", end='', flush=True)
        time.sleep(delay)
    print()

# ==== Main ====
def main():
    print_banner()
    if len(sys.argv) == 2:
        arg = sys.argv[1]
        if arg in ('--help', '-h'):
            show_help()
        elif arg in ('--system_info', '--si'):
            loading_effect("Fetching system info")
            get_system_info()
        else:
            print(f"\033[91m[!] Unknown command:\033[0m {arg}")
            print("Run with \033[93m--help\033[0m to see available modules.\n")
    else:
        print("\033[90mTip:\033[0m Use --help for more commands")

if __name__ == "__main__":
    main()


