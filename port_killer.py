import psutil

def kill_port(port):
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        info = proc.info
        if info is not None and isinstance(info.get('connections'), list):
            for conn in info.get('connections'):
                if conn and conn.laddr and conn.laddr.port == port:
                    print(f"Process {info['pid']} using port {port} found, terminating...")
                    # proc.terminate()
                    return True
    print(f"No process found using port {port}")
    return False

# Example usage:
port_to_kill = 12345  # Specify the port you want to kill
kill_port(port_to_kill)
