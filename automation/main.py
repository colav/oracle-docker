from pathlib import Path
from drive.drive_service import DriveService
from workflows.folder_workflow import FolderWorkflow
from config.settings import settings


def main():
    drive_service = DriveService(settings.GOOGLE_CREDENTIALS)

    folders = drive_service.get_folders(settings.GOOGLE_PARENT_ID)
    if not folders:
        print("⚠️ No se encontraron carpetas.")
        return

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