from pathlib import Path
from ssh import parse_ssh_config

def test_parse_ssh_config(tmp_path: Path):
    # Create a temporary SSH config file with the example content
    ssh_config_content = """
    Host newServer
      HostName newServer.url
      User adminuser
      Port 2222
      IdentityFile ~/.ssh/id_rsa.key
      ProxyJump bastion
    """
    ssh_config_path = tmp_path / "ssh_config"
    ssh_config_path.write_text(ssh_config_content.strip())

    # Expected output
    expected_output = {
        "newServer": {
            "host_name": "newServer.url",
            "user": "adminuser",
            "port": 2222,
            "identity_file": "~/.ssh/id_rsa.key",
            "proxy_jump": "bastion",
        }
    }

    # Call the function and assert the result
    result = parse_ssh_config(ssh_config_path)
    assert result == expected_output