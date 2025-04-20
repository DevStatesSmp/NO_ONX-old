import subprocess
import sys
import os

def fix_permissions_for_cpp():
    # Ensure the detective binary is executable
    if not os.access('./detective', os.X_OK):
        print("\n⚠️ Permission denied on 'detective' executable!")
        confirm = input("👉 WARNING: This will grant execute permissions (chmod +x) to 'detective'. Proceed? (y/n): ").lower()
        if confirm == 'y':
            try:
                subprocess.run(['chmod', '+x', './detective'], check=True)
                print("✅ Permissions updated. Retrying...\n")
            except subprocess.CalledProcessError:
                print("❌ Failed to change permissions. Try running with sudo.")
                sys.exit(1)
        else:
            print("❌ Skipped changing permissions. Exiting.")
            sys.exit(1)

def run_detective():
    print("🔍 Enter directory path to watch (example: /home/your-user):")
    watch_path = input(">>> ").strip()

    if not watch_path or not os.path.exists(watch_path):
        print("[!] Invalid path. Exiting.")
        sys.exit(1)

    print(f"\n📂 Watching: {watch_path}\n")

    try:
        process = subprocess.Popen(
            ['./detective', watch_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in process.stdout:
            print(line, end='')

            # If permission error detected from C++ output
            if "Permission denied" in line:
                process.kill()
                print("\n⚠️ C++ executable is not executable. Fixing permissions...")
                fix_permissions_for_cpp()
                run_detective()  # Retry after fixing permissions
                break

    except FileNotFoundError:
        print("[!] Error: 'detective' binary not found. Did you compile it?")
        print("    Try: g++ -o detective no_onx_watcher.cpp")
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting...")

if __name__ == "__main__":
    run_detective()



