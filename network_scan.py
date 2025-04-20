import socket
import concurrent.futures
import ipaddress

def scan_port(target_ip, port, timeout=1):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except OSError:
                    service = "Unknown"
                return port, service
    except:
        pass
    return None

def port_scan(target_ip, ports=range(1, 1025), max_threads=100):
    open_ports = []

    print(f"[*] Starting scan on {target_ip}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_port = {executor.submit(scan_port, target_ip, port): port for port in ports}
        
        for future in concurrent.futures.as_completed(future_to_port):
            result = future.result()
            if result:
                open_ports.append(result)

    open_ports.sort()
    return open_ports

if __name__ == "__main__":
    try:
        # Get user input
        target = input("Enter target IP address: ").strip()
        ipaddress.ip_address(target)  # Validate IP

        port_range_input = input("Enter port range (e.g., 1-1024) or press Enter for default: ").strip()
        
        if port_range_input:
            start_port, end_port = map(int, port_range_input.split("-"))
            ports_to_scan = range(start_port, end_port + 1)
        else:
            ports_to_scan = range(1, 1025)

        # Run scan
        scanned_ports = port_scan(target, ports=ports_to_scan, max_threads=200)
        
        print("\n[+] Open Ports:")
        for port, service in scanned_ports:
            print(f" - Port {port}/tcp ({service})")

    except ValueError:
        print("Invalid IP address or port range.")

