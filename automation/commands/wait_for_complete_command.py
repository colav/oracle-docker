import subprocess
import time


class WaitForKaypachaCommand:
    def __init__(self, container_name: str, poll_interval: int = 5):
        self.container_name = container_name
        self.poll_interval = poll_interval

    def execute(self):
        print(f"⏳ Esperando a que el contenedor termine: {self.container_name}")

        while True:
            result = subprocess.run(
                [
                    "docker",
                    "inspect",
                    "-f",
                    "{{.State.Status}} {{.State.ExitCode}}",
                    self.container_name,
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                raise RuntimeError(
                    f"No se pudo inspeccionar el contenedor {self.container_name}"
                )

            status, exit_code = result.stdout.strip().split()

            if status == "exited":
                exit_code = int(exit_code)
                if exit_code == 0:
                    print("✅ Kaypacha terminó exitosamente")
                else:
                    raise RuntimeError(
                        f"❌ Kaypacha terminó con error (exit code {exit_code})"
                    )
                return

            time.sleep(self.poll_interval)
