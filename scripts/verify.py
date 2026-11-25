"""Check the standalone distribution without using production credentials."""

import json
import os
import socket
import time
from urllib.request import urlopen
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile


def verify(filename):
    with tempfile.TemporaryDirectory() as temp:
        with tarfile.open(filename) as archive:
            archive.extractall(temp, filter="data")
        root = Path(temp) / "acemusic-chatgpt"
        for directory in ("dist", "profiles"):
            assert [child.name for child in (root / directory).iterdir()] == ["acemusic"]
        profile = json.loads((root / "profiles/acemusic/profile.json").read_text())
        assert profile["scope"] == "acemusic.tasks:read"
        assert profile["tool"] == "acemusic_get_existing_task"
        assert "ACE Music" in (root / "dist/acemusic/widget.html").read_text()
        subprocess.run(
            ["npm", "ci", "--omit=dev", "--ignore-scripts", "--no-audit", "--no-fund"],
            cwd=root, check=True,
        )
        with socket.socket() as socket_handle:
            socket_handle.bind(("127.0.0.1", 0))
            port = socket_handle.getsockname()[1]
        origin = "https://profile.example.invalid"
        env = {
            "PATH": os.environ["PATH"],
            "PORT": str(port),
            "APP_PROFILE": "suno",
            "PUBLIC_ORIGIN": origin,
            "OAUTH_AUDIENCE": origin + "/mcp",
            "OAUTH_ISSUER": "https://issuer.example.invalid/",
            "OAUTH_JWKS_URL": "https://issuer.example.invalid/keys",
            "OWNED_TASK_READBACK_URL": "https://reader.example.invalid/",
            "OWNED_TASK_READBACK_TOKEN": "loopback-test-only",
        }
        child = subprocess.Popen(["node", "run.mjs"], cwd=root, env=env)
        try:
            local = f"http://127.0.0.1:{port}"
            for _ in range(100):
                if child.poll() is not None:
                    raise RuntimeError("Standalone server exited before startup")
                try:
                    with urlopen(local + "/health", timeout=1) as result:
                        assert json.load(result)["app"] == "acemusic-by-ace-data-cloud"
                        break
                except OSError:
                    time.sleep(0.1)
            else:
                raise RuntimeError("Standalone server never reported readiness")
            with urlopen(local + "/.well-known/oauth-protected-resource/mcp", timeout=2) as result:
                metadata = json.load(result)
            assert metadata["resource"] == origin + "/mcp"
            assert metadata["scopes_supported"] == ["acemusic.tasks:read"]
        finally:
            child.terminate()
            child.wait(timeout=5)


if __name__ == "__main__":
    verify(sys.argv[1])
