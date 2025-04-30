import os
import stat
import time
import hashlib
import getpass
import argparse
import platform

# Optional: only import win32security if on Windows and available
try:
    if platform.system() == "Windows":
        import win32security
except ImportError:
    win32security = None

# Define info class with static methods for file operations
class info:
    @staticmethod
    def get_owner(path):
        if platform.system() == "Windows" and win32security:
            try:
                sd = win32security.GetFileSecurity(path, win32security.OWNER_SECURITY_INFORMATION)
                owner_sid = sd.GetSecurityDescriptorOwner()
                name, domain, _ = win32security.LookupAccountSid(None, owner_sid)
                return f"{domain}\\{name}"
            except Exception:
                return getpass.getuser()
        elif platform.system() != "Windows":  # Check if not on Windows
            try:
                import pwd  # Import pwd only if not on Windows
                return pwd.getpwuid(os.stat(path).st_uid).pw_name
            except Exception:
                return getpass.getuser()
        else:
            return getpass.getuser()  # Default to current user on other systems

    @staticmethod
    def file_info(path):
        if not os.path.exists(path):
            print(f"❌ Path not found: {path}")
            return

        try:
            stat_info = os.lstat(path)
            file_type = "Directory" if stat.S_ISDIR(stat_info.st_mode) else \
                        "Symlink" if stat.S_ISLNK(stat_info.st_mode) else \
                        "File"

            print(f"📄 Path: {path}")
            print(f"🔍 Type: {file_type}")
            print(f"📦 Size: {stat_info.st_size} bytes")
            print(f"👤 Owner: {info.get_owner(path)}")
            print(f"🔒 Permissions: {oct(stat_info.st_mode)[-3:]}")
            print(f"🕓 Last modified: {time.ctime(stat_info.st_mtime)}")
            print(f"🕓 Last accessed: {time.ctime(stat_info.st_atime)}")
            print(f"🕓 Created (inode change): {time.ctime(stat_info.st_ctime)}")
        except Exception as e:
            print(f"❌ Error retrieving file info: {e}")

    @staticmethod
    def file_hash(path, algo="sha256"):
        if not os.path.isfile(path):
            print(f"❌ Not a valid file: {path}")
            return

        hash_func = getattr(hashlib, algo.lower(), None)
        if hash_func is None:
            print(f"❌ Unsupported hash algorithm: {algo}")
            return

        try:
            with open(path, "rb") as f:
                hasher = hash_func()
                while chunk := f.read(8192):
                    hasher.update(chunk)
                print(f"🔑 {algo.upper()} hash of {path}: {hasher.hexdigest()}")
        except Exception as e:
            print(f"❌ Error computing hash: {e}")

    @staticmethod
    def symlink_info(path):
        if not os.path.islink(path):
            print(f"❌ Not a symlink: {path}")
            return
        try:
            target = os.readlink(path)
            print(f"🔗 Symlink: {path} -> {target}")
        except Exception as e:
            print(f"❌ Error reading symlink: {e}")

    @staticmethod
    def dir_info(path):
        if not os.path.isdir(path):
            print(f"❌ Not a directory: {path}")
            return
        try:
            print(f"📁 Contents of directory {path}:")
            for item in os.listdir(path):
                full = os.path.join(path, item)
                print(f" - {item} ({'dir' if os.path.isdir(full) else 'file'})")
        except Exception as e:
            print(f"❌ Error listing directory: {e}")

    @staticmethod
    def extended_info(path):
        print("📌 Extended Information\n")
        info.file_info(path)
        if os.path.isfile(path):
            info.file_hash(path)
        if os.path.islink(path):
            info.symlink_info(path)


class check_permission:
    """Class to analyze and print file/directory permissions along with special flags."""

    @staticmethod
    def analyze(path):
        """Analyzes and prints file/directory permissions along with special flags."""
        try:
            # Check if path exists
            if not os.path.exists(path):
                print(f"[-] Path does not exist: {path}")
                return

            # For Windows, use win32security to get the permissions
            if platform.system() == "Windows" and win32security:
                try:
                    # Get the file security descriptor
                    sd = win32security.GetFileSecurity(path, win32security.DACL_SECURITY_INFORMATION)
                    # Get the DACL (Discretionary Access Control List)
                    dacl = sd.GetSecurityDescriptorDacl()

                    # Get file owner SID
                    owner_sid = sd.GetSecurityDescriptorOwner()
                    owner_name, domain, _ = win32security.LookupAccountSid(None, owner_sid)

                    print(f"[+] {path} (Windows)")
                    print(f"    Owner : {domain}\\{owner_name}")
                    print(f"    Permissions:")

                    # Display ACE (Access Control Entries)
                    for i in range(dacl.GetAceCount()):
                        ace = dacl.GetAce(i)
                        print(f"      ACE {i}: {ace}")

                except Exception as e:
                    print(f"[-] Error reading security descriptor: {e}")

            # Integrate with file info methods (for any other information)
            info.file_info(path)

        except FileNotFoundError:
            print(f"[-] File not found: {path}")
        except PermissionError:
            print(f"[-] Permission denied: {path}")
        except Exception as e:
            print(f"[-] Error analyzing {path}: {e}")


def main():
    """Main function to handle argument parsing and execute the permission check."""
    parser = argparse.ArgumentParser(description="Analyze file/folder permissions and retrieve additional information")
    parser.add_argument("target", nargs='+', help="Target file(s) or directory(ies) to check permissions")
    args = parser.parse_args()

    for path in args.target:
        check_permission.analyze(path)

if __name__ == "__main__":
    main()

