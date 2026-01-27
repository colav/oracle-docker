import subprocess
from pathlib import Path
from .base_command import Command

class DockerUpCommand(Command):
    def __init__(self, compose_file: Path, env_file: Path):
        self.compose_file = compose_file
        self.env_file = env_file

    def execute(self):
        print("🐳 Iniciando contenedor Oracle con docker-compose...")
        subprocess.run(
            [
                "docker", "compose",
                "-f", str(self.compose_file),
                "--env-file", str(self.env_file),
                "up", "-d"
            ],
            check=True
        )
