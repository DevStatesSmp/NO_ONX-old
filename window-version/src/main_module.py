# THIS IS MODULE, DO NOT RUN THIS FILE DIRECTLY

import psutil
import os
import time
import platform
import sys
import pyfiglet
import shutil

# Import source
from .file_info_module import info, check_permission, hidden_file_info
from .modification import mod
from . import file_scan
from .compare_module import deep_compare_files, simple_compare_files



# Banner tool
def banner():
    term_width = shutil.get_terminal_size().columns
    ascii = pyfiglet.figlet_format("NO_ONX", font="slant")
    banner_lines = ascii.splitlines()
    max_line_length = max(len(line) for line in banner_lines)

    for line in banner_lines:
        print(f"\033[92m{line.center(term_width)}\033[0m")

    version_str = "v0.1.2 for Window"
    print(" " * (max_line_length - len(version_str)) + f"\033[90m{version_str}\033[0m\n")
    print("\033[96m📖 Usage: python <module_name>.py or python noonx.py <command>\033[0m\n")

# Help 
def help():
    print("""
\033[94mUsage:\033[0m
  \033[92m1.\033[0m python3 noonx.py <command> [arguments]
  \033[92m2.\033[0m python3 src/[FILE_MODULE_NAME].py

\033[94mCommands:\033[0m
  \033[96m--file_info\033[0m [file_path]      - Retrieve detailed file information
      \033[93mArguments:\033[0m <file_path> - Path to the file you want information about.
  
  \033[96m--file_hash\033[0m [file_path] [algorithm] - Retrieve file hash
      \033[93mArguments:\033[0m <file_path> - Path to the file.
                  <algorithm> (optional) - Hashing algorithm (default: sha256).

  \033[96m--dir_info\033[0m [directory_path]     - Retrieve directory information
      \033[93mArguments:\033[0m <directory_path> - Path to the directory.

  \033[96m--symlink_info\033[0m [symlink_path] - Retrieve symlink information
      \033[93mArguments:\033[0m <symlink_path> - Path to the symlink.

  \033[96m--extended_info\033[0m [file_path] - Retrieve extended file information
      \033[93mArguments:\033[0m <file_path> - Path to the file.

  \033[96m--scan_dir\033[0m [directory_path] [algorithm] - Scan directory for malware
      \033[93mArguments:\033[0m <directory_path> - Path to the directory.
                  <algorithm> (optional) - Hashing algorithm (default: sha256).

  \033[96m--check_permission\033[0m [file_path] - Check file or directory permissions
      \033[93mArguments:\033[0m <file_path> - Path to the file or directory.
          
  \033[96m--hidden_file_info\033[0m [file_path] - Check hidden file or directory
      \033[93mArguments:\033[0m <file_path> - Path to the file or directory.
          

  \033[96m--compare\033[0m [path1] [path2]       - Compare two files or directories
      \033[93mArguments:\033[0m <path1> - Path to the first file or directory.
                  <path2> - Path to the second file or directory. (IN DEVELOPMENT)


\033[94mModification Commands:\033[0m
  \033[96m--modify_file_permission\033[0m [file_path] [permissions]    - Modify the file permission
      \033[93mArguments:\033[0m <file_path> - Path to the file.
                  <permissions> - New permission (e.g., 755).

  \033[96m--modify_file_content\033[0m [file_path] [operation] [target_text] [optional_text]       - Modify the file content
      \033[93mArguments:\033[0m <file_path> - Path to the file.
                  <operation> - Operation to perform: 'replace', 'delete', or 'append'.
                  <target_text> - Text to target for the operation.
                  <optional_text> - (For replace operation) New text to replace with. (For append) Text to append.

  \033[96m--modify_file_name\033[0m [old_name] [new_name]          - Modify the file name
      \033[93mArguments:\033[0m <old_name> - Current file name.
                  <new_name> - New file name.

  \033[96m--modify_file_metadata\033[0m [file_path] [metadata_type] [value]     - Modify the file metadata
      \033[93mArguments:\033[0m <file_path> - Path to the file.
                  <metadata_type> - Type of metadata to modify (e.g., timestamp).
                  <value> - New value for the metadata.

  \033[96m--modify_file_line\033[0m [file_path] [line_number] [operation] [optional_new_line]          - Modify a specific line in the file
      \033[93mArguments:\033[0m <file_path> - Path to the file.
                  <line_number> - Line number to modify.
                  <operation> - Operation: 'replace' or 'insert'.
                  <optional_new_line> - (For replace/insert) New content for the line.

  \033[96m--modify_file_symlink\033[0m [target_path] [symlink_path] [operation]       - Modify the symlink of a file
      \033[93mArguments:\033[0m <target_path> - Path to the target file or directory.
                  <symlink_path> - Path to the symlink.
                  <operation> - Operation: 'create', 'remove', or 'update'.

  \033[96m--modify_directory\033[0m [dir_path] [operation] [new_path]          - Modify the directory (move, rename, etc.)
      \033[93mArguments:\033[0m <dir_path> - Path to the directory.
                  <operation> - Operation: 'move' or 'rename'.
                  <new_path> - New path for the directory (only needed for move/rename).

  \033[96m--modify_directory_permissions\033[0m [dir_path] [permissions]          - Modify the permissions of a directory
      \033[93mArguments:\033[0m <dir_path> - Path to the directory.
                  <permissions> - New permission (e.g., 755).

  \033[96m--modify_file_owner\033[0m [file_path] [new_owner]         - Modify the owner of a file
      \033[93mArguments:\033[0m <file_path> - Path to the file.
                  <new_owner> - New owner ID (e.g., user ID).

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

def loading_effect(text="Loading modules", delay=0.3):
    spinner = ['/', '|', '\\', '-'] 
    for _ in range(10):
        for symbol in spinner:
            print(f"\r\033[93m{text} {symbol}\033[0m", end='', flush=True)
            time.sleep(delay)
    print()


# ==== Main ====
def main():
    banner()
    if len(sys.argv) >= 2:
        arg = sys.argv[1]

        # Main argument for noonx.py
        if arg in ('--help', '-h'):
            help()
        elif arg in ('--system_info', '-si'):
            loading_effect("Fetching system info")
            get_system_info()

        ## Class info
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

        ## class check_permission
        elif arg == '--check_permission' and len(sys.argv) >= 3:
            path = sys.argv[2]
            check_permission.analyze(path)
        
        ## Class hidden_file_info
        elif arg == '--hidden_file_info' and len(sys.argv) >= 3:
            path = sys.argv[2]
            hidden_scanner = hidden_file_info(path)
            hidden_scanner.scan_hidden()


        # Modification
        elif arg == '--modify_file_permission' and len(sys.argv) >= 4:
            path = sys.argv[2]
            permission = sys.argv[3]
            mod.modify.modify_file_permission(path, permission)

        elif arg == '--modify_file_content' and len(sys.argv) >= 5:
            path = sys.argv[2]
            operation = sys.argv[3]
            if operation == 'replace' or operation == 'delete':
                target_text = sys.argv[4]
                text = sys.argv[5] if operation == 'replace' and len(sys.argv) >= 6 else None
                mod.modify.modify_file_content(path, operation, text, target_text)
            elif operation == 'append':
                text = sys.argv[4]
                mod.modify.modify_file_content(path, operation, text)

        elif arg == '--modify_file_name' and len(sys.argv) >= 4:
            old_name = sys.argv[2]
            new_name = sys.argv[3]
            mod.modify.modify_file_name(old_name, new_name)

        elif arg == '--modify_file_metadata' and len(sys.argv) >= 5:
            path = sys.argv[2]
            metadata_type = sys.argv[3]
            value = float(sys.argv[4])
            mod.modify.modify_file_metadata(path, metadata_type, value)

        elif arg == '--modify_file_line' and len(sys.argv) >= 5:
            path = sys.argv[2]
            line_number = int(sys.argv[3])
            operation = sys.argv[4]
            new_line = sys.argv[5] if operation in ('replace', 'insert') and len(sys.argv) >= 6 else None
            mod.modify.modify_file_line(path, line_number, operation, new_line)

        elif arg == '--modify_file_symlink' and len(sys.argv) >= 5:
            target_path = sys.argv[2]
            symlink_path = sys.argv[3]
            operation = sys.argv[4]
            mod.modify.modify_file_symlink(target_path, symlink_path, operation)

        elif arg == '--modify_directory' and len(sys.argv) >= 5:
            path = sys.argv[2]
            operation = sys.argv[3]
            new_path = sys.argv[4]
            mod.modify.modify_directory(path, operation, new_path)

        elif arg == '--modify_directory_permissions' and len(sys.argv) >= 4:
            path = sys.argv[2]
            permission = sys.argv[3]
            mod.modify.modify_directory_permissions(path, permission)

        elif arg == '--modify_file_owner' and len(sys.argv) >= 4:
            path = sys.argv[2]
            new_owner = int(sys.argv[3])
            mod.modify.modify_file_owner(path, new_owner)

        # File Scan
        elif arg in ('--scan_dir') and len(sys.argv) >= 3:
            path = sys.argv[2]
            algo = sys.argv[3] if len(sys.argv) >= 4 else "sha256"
            loading_effect(f"Scanning directory ({path}) using {algo.upper()}")
            file_scan.reset_results()
            file_scan.scan_directory(path, algo)
            file_scan.print_results()

        

        else:
            print(f"\033[91m[!] Unknown or incomplete command:\033[0m {' '.join(sys.argv[1:])}")
            print("Run with \033[93m--help\033[0m to see available modules.\n")
    else:
        print("\033[90mTip:\033[0m Use --help for more commands")