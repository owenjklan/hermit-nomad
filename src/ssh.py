from pathlib import Path
from typing import Dict, Optional


def parse_ssh_config(ssh_config_path: Path = Path("~/.ssh/config")) -> Dict[str, Dict[str, Optional[str | int]]]:
    """
    Parses an SSH config file and returns a dictionary representation of its contents.

    Args:
        ssh_config_path (Path): Path to the SSH config file. Defaults to "~/.ssh/config".

    Returns:
        Dict[str, Dict[str, Optional[str | int]]]: A dictionary where each key is the host name
        and the value is another dictionary of the host's attributes.
    """
    # Expand the user path if necessary
    ssh_config_path = ssh_config_path.expanduser()

    # Check if the file exists
    if not ssh_config_path.exists():
        raise FileNotFoundError(f"SSH config file not found at {ssh_config_path}")

    hosts_config: Dict[str, Dict[str, Optional[str | int]]] = {}
    current_host = None
    current_host_data = {}

    # Read the config file line by line
    try:
        with ssh_config_path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                # Skip empty lines or comments
                if not line or line.startswith("#"):
                    continue

                # Check if the line defines a new host
                if line.lower().startswith("host "):
                    # Save the previous host's data if any
                    if current_host:
                        # Ensure mandatory fields are present or set to None
                        current_host_data["host_name"] = current_host_data.get("host_name")
                        current_host_data["user"] = current_host_data.get("user")
                        hosts_config[current_host] = current_host_data

                    # Start a new host entry
                    current_host = line[5:].strip()  # Extract the host name
                    current_host_data = {}
                else:
                    # Parse key-value pairs for the current host
                    if current_host:
                        key, value = line.split(None, 1)
                        key = key.lower()
                        value = value.strip()
                        # Map keys to required format
                        if key == "hostname":
                            current_host_data["host_name"] = value
                        elif key == "user":
                            current_host_data["user"] = value
                        elif key == "port":
                            current_host_data["port"] = int(value)
                        elif key == "identityfile":
                            current_host_data["identity_file"] = value
                        elif key == "proxyjump":
                            current_host_data["proxy_jump"] = value

            # Save the last host entry
            if current_host:
                current_host_data["host_name"] = current_host_data.get("host_name")
                current_host_data["user"] = current_host_data.get("user")
                hosts_config[current_host] = current_host_data

    except Exception as e:
        raise RuntimeError(f"Error parsing SSH config file: {e}")

    return hosts_config