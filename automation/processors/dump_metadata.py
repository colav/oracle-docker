import re
from pathlib import Path

class DumpMetadata:
    @staticmethod
    def extract(zip_filename: str):
        """
        Extrae prefijo y fecha del nombre del archivo ZIP.
        
        Soporta dos formatos:
        1. Formato antiguo: PREFIJO_YYYYMMDD.zip
        2. Formato nuevo: TIPO_ROR_YYYY-MM-DD_HH-MM.zip
        
        Retorna: (prefix, date)
        - Para formato antiguo: prefix, date (YYYYMMDD)
        - Para formato nuevo: ROR_ID, date (YYYYMMDD sin guiones)
        """
        # Intentar formato nuevo: TIPO_ROR_YYYY-MM-DD_HH-MM.zip
        # Ej: SCIENTI_03bp5hc83_2024-01-15_14-30.zip
        new_format = re.match(
            r"([A-Za-z]+)_([A-Za-z0-9]+)_(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})\.zip",
            zip_filename
        )
        
        if new_format:
            tipo = new_format.group(1)      # scienti
            ror_id = new_format.group(2)    # 03bp5hc83
            year = new_format.group(3)      # 2024
            month = new_format.group(4)     # 01
            day = new_format.group(5)       # 15
            
            # Retornar ror_id como prefix y fecha en formato YYYYMMDD
            date = f"{year}{month}{day}"
            return ror_id, date
        
        raise ValueError(
            f"Formato inválido de ZIP: {zip_filename}\n"
            f"Formatos esperados:\n"
            f"  - TIPO_ROR_YYYY-MM-DD_HH-MM.zip\n"
        )

    @staticmethod
    def detect_dump_files(prefix: str, date: str, folder: Path):
        """
        Busca archivos .dmp en la carpeta.
        
        Busca los siguientes patrones (en orden de prioridad):
        1. {prefix}_CV_{date}.dmp
        2. {prefix}_GR_{date}.dmp
        3. {prefix}_IN_{date}.dmp
        4. Cualquier archivo que contenga CV/GR/IN y termine en .dmp
        
        Retorna una tupla: (archivos_encontrados, prefijo_real)
        El prefijo_real se extrae del primer archivo encontrado.
        """
        expected = [
            f"{prefix}_CV_{date}.dmp",
            f"{prefix}_GR_{date}.dmp",
            f"{prefix}_IN_{date}.dmp",
        ]

        # Buscar archivos exactos con el prefijo del ZIP
        found = [f for f in expected if (folder / f).exists()]
        
        if found:
            return found, prefix
        
        # Si no se encontraron, buscar cualquier .dmp con CV/GR/IN
        print(f"  🔍 No se encontraron dumps con prefijo '{prefix}', buscando con cualquier prefijo...")
        all_dmps = list(folder.glob("*.dmp"))
        
        if not all_dmps:
            raise FileNotFoundError(
                f"No se encontraron archivos .dmp en la carpeta.\n"
                f"Esperados: {', '.join(expected)}"
            )
        
        # Buscar dumps que contengan CV, GR o IN
        flexible_found = []
        detected_prefix = None
        
        for dmp_file in all_dmps:
            name = dmp_file.name
            # Verificar si contiene CV, GR o IN
            if any(pattern in name.upper() for pattern in ["_CV_", "_GR_", "_IN_"]):
                flexible_found.append(name)
                
                # Intentar extraer el prefijo del primer archivo encontrado
                # Formato: PREFIJO_TIPO_FECHA.dmp
                if detected_prefix is None:
                    match = re.match(r"([A-Za-z0-9]+)_(CV|GR|IN)_", name, re.IGNORECASE)
                    if match:
                        detected_prefix = match.group(1)
        
        if flexible_found:
            # Usar el prefijo detectado o el original si no se pudo detectar
            final_prefix = detected_prefix if detected_prefix else prefix
            print(f"  ✅ Encontrados {len(flexible_found)} dumps con prefijo '{final_prefix}': {', '.join(flexible_found)}")
            return flexible_found, final_prefix
        
        raise FileNotFoundError(
            f"No se encontraron dumps válidos.\n"
            f"Esperados: {', '.join(expected)}\n"
            f"Encontrados en carpeta: {[f.name for f in all_dmps]}"
        )