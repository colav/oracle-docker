import argparse
from pathlib import Path
from drive.drive_service import DriveService
from workflows.folder_workflow import FolderWorkflow
from config.settings import settings


def parse_arguments():
    """Parsea los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description='Automatización de descarga y procesamiento de dumps desde Google Drive'
    )
    parser.add_argument(
        '--ror',
        type=str,
        help='ID del ROR para filtrar carpetas específicas (ej: 03bp5hc83)',
        default=None
    )
    return parser.parse_args()


def filter_folders_by_ror_id(folders: list, ror_id: str) -> list:
    """
    Filtra carpetas que coincidan con el ror_id.
    Formato esperado: rorid_nombre-institucion (ej: 03bp5hc83_Universidad-de-Antioquia)
    """
    filtered = []
    for folder in folders:
        folder_name = folder['name']
        # Extraer el ror_id del nombre de la carpeta (parte antes del primer _)
        if '_' in folder_name:
            folder_ror_id = folder_name.split('_')[0]
            if folder_ror_id == ror_id:
                filtered.append(folder)
    return filtered


def main():
    args = parse_arguments()
    
    drive_service = DriveService(settings.GOOGLE_CREDENTIALS)

    # Obtener todas las carpetas
    folders = drive_service.get_folders(settings.GOOGLE_PARENT_ID)
    if not folders:
        print("⚠️ No se encontraron carpetas.")
        return

    # Filtrar por ror_id si se especificó
    if args.ror:
        print(f"\n🔍 Filtrando carpetas con ROR ID: {args.ror}")
        folders = filter_folders_by_ror_id(folders, args.ror)
        if not folders:
            print(f"❌ No se encontraron carpetas con ROR ID '{args.ror}'")
            return
        print(f"✅ Se encontraron {len(folders)} carpeta(s) con el ROR ID especificado")

    project_root = Path(__file__).resolve().parents[1]
    workflow = FolderWorkflow(
        drive=drive_service,
        base_dump=Path.home() / "dump",
        project_root=project_root
    )

    successful = 0
    failed = 0
    errors = []

    for folder in folders:
        try:
            print(f"\n{'='*60}")
            result = workflow.process_folder(folder)
            if result:
                successful += 1
                print(f"✅ Carpeta '{folder['name']}' procesada exitosamente")
            else:
                failed += 1
                print(f"⚠️ Carpeta '{folder['name']}' sin .env generado")
        except Exception as e:
            failed += 1
            error_msg = f"❌ Error en carpeta '{folder['name']}': {str(e)}"
            print(error_msg)
            errors.append(error_msg)

    print(f"\n{'='*60}")
    print("\n🎉 Proceso completado.")
    print(f"✅ Exitosas: {successful}")
    print(f"❌ Fallidas: {failed}")
    
    if errors:
        print("\n📋 Detalle de errores:")
        for error in errors:
            print(f"  {error}")


if __name__ == "__main__":
    main()