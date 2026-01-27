import subprocess
from pathlib import Path
from .base_command import Command

class DockerDownCommand(Command):
    def __init__(self, compose_file: Path, env_file: Path | None = None, remove_volumes: bool = False):
        self.compose_file = compose_file
        self.env_file = env_file
        self.remove_volumes = remove_volumes

    def execute(self):
        print("🐳 Deteniendo contenedor Oracle...")
        cmd = ["docker", "compose", "-f", str(self.compose_file)]
        if self.env_file:
            cmd += ["--env-file", str(self.env_file)]
        cmd += ["down"]
        if self.remove_volumes:
            cmd.append("-v")
        subprocess.run(cmd, check=True)
