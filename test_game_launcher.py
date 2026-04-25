import os
import subprocess
import sys
import time

# Importing your custom data structures
# Assuming they are in a 'datastructures' folder in the same directory
from datastructures.array import ArrayList
from datastructures.hash_table import HashTable

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_port_mapping(file_path):
    """Parses ports.txt and stores values in a custom HashTable."""
    # Initialize with a reasonable capacity for game ports
    ports = HashTable(initial_capacity=32)
    
    if not os.path.exists(file_path):
        return ports

    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("GAME_") and "_PORT=" in line:
                try:
                    parts = line.split('=')
                    # Key: THELLUSOMA, Value: 50061
                    folder_name = parts[0].replace("GAME_", "").replace("_PORT", "").strip()
                    port = parts[1].strip()
                    ports.set(folder_name.upper(), port)
                except Exception:
                    continue
    return ports

def launch_manager():
    base_dir = "Games"
    ports_file = "Ports.txt"
    server_bin = os.path.abspath(os.path.join("game_server", "server_text_smoother"))
    
    # Use ArrayList to track running background processes
    running_servers = ArrayList()

    clear_screen()
    print("=== ECE-3822 Project Setup (Custom Data Structures) ===")
    user_name = input("Enter your name: ").strip() or "Player"
    start_servers = input("Launch game servers? (y/n): ").strip().lower()
    suppress_output = input("Suppress console output? (y/n): ").strip().lower() == 'y'
    
    output_dest = subprocess.DEVNULL if suppress_output else None

    # 1. Load ports into HashTable
    port_map = get_port_mapping(ports_file)

    # 2. Server Startup
    if start_servers == 'y':
        print("\n--- Initializing Servers ---")
        if os.path.exists(base_dir):
            game_folders = os.listdir(base_dir)
            for folder in game_folders:
                full_path = os.path.join(base_dir, folder)
                if os.path.isdir(full_path):
                    folder_upper = folder.upper()
                    # Use custom HashTable.get()
                    port = port_map.get(folder_upper)
                    
                    if port and (os.path.exists(server_bin) or os.path.exists(server_bin + ".exe")):
                        print(f"Launching server: {folder} on port {port}")
                        proc = subprocess.Popen(
                            [server_bin, "--port", port], 
                            cwd=full_path,
                            stdout=output_dest,
                            stderr=output_dest
                        )
                        running_servers.append(proc)
        time.sleep(1) 

    # 3. Main Selection Loop
    try:
        while True:
            clear_screen()
            print(f"=== Launcher | User: {user_name} | Servers: {len(running_servers)} ===")
            
            # Use ArrayList to store tuples of (game_name, script_path)
            valid_games = ArrayList()
            all_folders = os.listdir(base_dir)
            
            for folder in all_folders:
                script_path = os.path.join(base_dir, folder, "code", "game", "main.py")
                if os.path.exists(script_path):
                    valid_games.append((folder, script_path))

            # Display games using custom ArrayList iteration
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
        # Cleanup servers stored in custom ArrayList
        if len(running_servers) > 0:
            print("\nShutting down servers...")
            for proc in running_servers:
                proc.terminate()

if __name__ == "__main__":
    launch_manager()