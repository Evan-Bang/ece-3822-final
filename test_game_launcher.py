import os
import subprocess
import sys
import time

from datastructures.array import ArrayList
from datastructures.hash_table import HashTable

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_port_mapping(file_path):
    """Parses ports.txt and stores values in a custom HashTable."""
    ports = HashTable(initial_capacity=32)
    
    if not os.path.exists(file_path):
        return ports

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("GAME_") and "_PORT=" in line:
                try:
                    parts = line.split('=')
                    folder_name = parts[0].replace("GAME_", "").replace("_PORT", "").strip()
                    port = parts[1].strip()
                    ports.set(folder_name.upper(), port)
                except Exception:
                    continue
    return ports

def setup_ssh_tunnels(port_map, user_name, ssh_host, running_tunnels, suppress_output):
    """
    Opens an SSH tunnel for each game port found in port_map.
    Maps each remote game port (500XX) to the same port locally.
    e.g. ssh -L 500XX:localhost:500XX user@host -N
    """
    output_dest = subprocess.DEVNULL if suppress_output else None
    print("\n--- Setting Up SSH Tunnels ---")

    # Collect all ports from the HashTable by iterating its internal buckets
    all_ports = []
    for bucket in port_map.buckets:
        if bucket:
            for key, value in bucket:
                all_ports.append((key, value))

    if not all_ports:
        print("No ports found in port map. Skipping tunnels.")
        return

    for game_name, port in all_ports:
        local_port = port  # map the same port locally for simplicity
        ssh_cmd = [
            "ssh",
            "-L", f"{local_port}:localhost:{port}",
            "-N",
            "-o", "StrictHostKeyChecking=no",  # avoids interactive host key prompt
            f"{user_name}@{ssh_host}"
        ]
        print(f"Tunneling {game_name}: localhost:{local_port} -> {ssh_host}:{port}")
        proc = subprocess.Popen(
            ssh_cmd,
            stdout=output_dest,
            stderr=output_dest
        )
        running_tunnels.append(proc)

    print(f"{len(all_ports)} tunnel(s) established.")
    time.sleep(1)

def launch_manager():
    base_dir = "games"
    ports_file = "ports.txt"
    server_bin = os.path.abspath(os.path.join("game_server", "server_text_smoother"))
    ssh_host = "ece-000.eng.temple.edu"

    running_servers = ArrayList()
    running_tunnels = ArrayList()  # track tunnel processes separately

    clear_screen()
    print("=== ECE-3822 Project Setup (Custom Data Structures) ===")
    user_name = input("Enter your name: ").strip() or "Player"
    start_servers = input("Launch game servers? (y/n): ").strip().lower()
    setup_tunnels = input("Set up SSH port forwarding? (y/n): ").strip().lower()
    suppress_output = input("Suppress console output? (y/n): ").strip().lower() == 'y'

    output_dest = subprocess.DEVNULL if suppress_output else None

    # 1. Load ports into HashTable
    port_map = get_port_mapping(ports_file)

    # 2. SSH Tunnel Setup (before servers, so ports are ready)
    if setup_tunnels == 'y':
        setup_ssh_tunnels(port_map, user_name, ssh_host, running_tunnels, suppress_output)

    # 3. Server Startup
    if start_servers == 'y':
        print("\n--- Initializing Servers ---")
        if os.path.exists(base_dir):
            game_folders = os.listdir(base_dir)
            for folder in game_folders:
                full_path = os.path.join(base_dir, folder)
                if os.path.isdir(full_path):
                    folder_upper = folder.upper()
                    port = port_map.get(folder_upper)

                    if port and (os.path.exists(server_bin) or os.path.exists(server_bin + ".exe")):
                        print(f"Launching server: {folder} on port {port}")
                        proc = subprocess.Popen(
                            [server_bin, "--port", port, "-n", folder_upper],
                            cwd="game_server",
                            stdout=output_dest,
                            stderr=output_dest
                        )
                        running_servers.append(proc)
        time.sleep(1)

    # 4. Main Selection Loop
    try:
        while True:
            clear_screen()
            print(f"=== Launcher | User: {user_name} | Servers: {len(running_servers)} | Tunnels: {len(running_tunnels)} ===")

            valid_games = ArrayList()
            all_folders = os.listdir(base_dir)

            for folder in all_folders:
                script_path = os.path.join(base_dir, folder, "code", "game", "main.py")
                if os.path.exists(script_path):
                    valid_games.append((folder, script_path))

            for i in range(len(valid_games)):
                name, _ = valid_games[i]
                p_num = port_map.get(name.upper(), "???")
                print(f"{i + 1}. {name} (Port: {p_num})")

            print("------------------------------------------------")
            choice = input("\nSelect index (q to quit): ").strip().lower()

            if choice == 'q':
                break

            try:
                index = int(choice) - 1
                if 0 <= index < len(valid_games):
                    name, path = valid_games[index]
                    game_port = port_map.get(name.upper(), "0")

                    cmd = [sys.executable, "main.py", user_name, "--port", game_port]

                    print(f"\n>> Launching {name}...")
                    subprocess.run(
                        cmd,
                        cwd=os.path.dirname(path),
                        stdout=output_dest,
                        stderr=output_dest
                    )
                    input("\nGame ended. Press Enter to return...")
            except ValueError:
                pass

    finally:
        # Cleanup tunnels
        if len(running_tunnels) > 0:
            print("\nClosing SSH tunnels...")
            for proc in running_tunnels:
                proc.terminate()

        # Cleanup servers
        if len(running_servers) > 0:
            print("Shutting down servers...")
            for proc in running_servers:
                proc.terminate()

if __name__ == "__main__":
    launch_manager()