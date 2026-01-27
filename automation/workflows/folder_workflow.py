from pathlib import Path
from datetime import datetime

from commands.wait_for_complete_command import WaitForKaypachaCommand
from commands.docker_down_command import DockerDownCommand
from commands.docker_up_command import DockerUpCommand
from orchestrator.command_executor import CommandExecutor
from drive.drive_service import DriveService
from processors.config_env_generator import EnvGenerator
from processors.dump_metadata import DumpMetadata
from processors.zip_processor import ZipProcessor


class FolderWorkflow:
    def __init__(self, drive: DriveService, base_dump: Path, project_root: Path):
        self.drive = drive
        self.base_dump = base_dump
        self.project_root = project_root

    def parse_zip_date(self, filename: str) -> datetime | None:
        """
        Extrae la fecha del nombre del archivo ZIP.
        Formato esperado: TIPO_ROR_YYYY-MM-DD_HH-MM.zip
        Ej: scienti_03bp5hc83_2024-01-15_14-30.zip
        """
        try:
            # Remover extensión .zip
            name_without_ext = filename.replace('.zip', '')
            parts = name_without_ext.split('_')
            
            # El formato esperado tiene al menos 5 partes: TIPO_ROR_YYYY-MM-DD_HH-MM
            if len(parts) >= 4:
                # Las partes de fecha deberían ser las últimas dos
                date_part = parts[-2]  # YYYY-MM-DD
                time_part = parts[-1]  # HH-MM
                
                # Parsear fecha y hora
                datetime_str = f"{date_part} {time_part.replace('-', ':')}"
                return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        except (ValueError, IndexError) as e:
            print(f"  ⚠️ No se pudo parsear fecha del archivo '{filename}': {e}")
            return None
        
        return None

    def get_most_recent_zip(self, files: list) -> dict | None:
        """
        Selecciona el archivo ZIP más reciente basándose en:
        1. La fecha en el nombre del archivo (formato estándar)
        2. Si no se puede parsear, usa createdTime de Drive
        """
        zip_files = [f for f in files if f["name"].endswith(".zip")]
        
        if not zip_files:
            return None
        
        if len(zip_files) == 1:
            return zip_files[0]
        
        print(f"  📦 Se encontraron {len(zip_files)} archivos ZIP, seleccionando el más reciente...")
        
        # Intentar ordenar por fecha en el nombre del archivo
        files_with_dates = []
        for zip_file in zip_files:
            parsed_date = self.parse_zip_date(zip_file["name"])
            if parsed_date:
                files_with_dates.append((zip_file, parsed_date))
                print(f"    - {zip_file['name']} → {parsed_date.strftime('%Y-%m-%d %H:%M')}")
        
        # Si se pudieron parsear fechas de los nombres, usar esa
        if files_with_dates:
            most_recent = max(files_with_dates, key=lambda x: x[1])
            print(f"  ✅ Seleccionado: {most_recent[0]['name']} (más reciente por nombre)")
            return most_recent[0]
        
        # Si no, usar createdTime de Drive
        print("  ⚠️ No se pudo extraer fecha de los nombres, usando createdTime de Drive")
        most_recent = max(zip_files, key=lambda x: x.get("createdTime", ""))
        print(f"  ✅ Seleccionado: {most_recent['name']} (más reciente por createdTime)")
        return most_recent

    def process_folder(self, folder):
        folder_name = folder["name"]
        folder_id = folder["id"]

        local_folder = self.base_dump / folder_name
        local_folder.mkdir(exist_ok=True)

        print(f"\n📁 Carpeta: {folder_name}")

        files = self.drive.get_files(folder_id)
        if not files:
            print("  ⚠️ Vacía.")
            return None

        # Seleccionar el ZIP más reciente
        most_recent_zip_file = self.get_most_recent_zip(files)
        
        if not most_recent_zip_file:
            print("  ⚠️ No hay archivos ZIP → no se genera .config.env")
            return None

        # Descargar solo el ZIP más reciente
        zip_path = local_folder / most_recent_zip_file["name"]
        print(f"  ⬇️ Descargando ZIP más reciente: {most_recent_zip_file['name']}")
        self.drive.download_file(most_recent_zip_file["id"], zip_path)

        # Descomprimir
        ZipProcessor.unzip(zip_path, local_folder)

        # Extraer metadata y buscar dumps
        prefix, date = DumpMetadata.extract(zip_path.name)
        dump_files, detected_prefix = DumpMetadata.detect_dump_files(prefix, date, local_folder)

        # Generar archivo .env con el prefijo detectado (puede ser diferente al del ZIP)
        env_file = EnvGenerator.create(
            prefix=detected_prefix,
            date=date,
            dump_files=dump_files,
            project_root=Path(__file__).resolve().parents[2],
            dump_folder=local_folder,
        )

        if env_file:
            executor = CommandExecutor()

            compose_file = self.project_root / "scienti" / "docker-compose.yml"

            executor.add(DockerUpCommand(compose_file=compose_file, env_file=env_file))
            executor.add(WaitForKaypachaCommand(container_name="scienti-oracle-docker-1"))
            executor.add(DockerDownCommand(compose_file=compose_file, env_file=env_file))

            executor.run()

        return env_file