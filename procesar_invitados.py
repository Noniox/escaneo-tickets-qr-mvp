import pandas as pd
import random
import string
import os

# Archivo de entrada y salida
INPUT_FILE = "data/BORRADOR- LISTA INVITADOS VIP INAUGURACION ANFITEATRO LA GAVIOTA DIA 1.xlsx"
OUTPUT_FILE = "data/lista_maestra.csv"

# Mapeo de sectores (Texto en Excel -> Nombre Corto)
SECTOR_MAP = {
    "Linea de Honor": "POLITICO",
    "INVITADOS": "POLITICO",
    "DIPUTADOS - REGIDORES - EMPLEADOS ALCALDIA": "POLITICO",
    "MIEMBROS DE LA BANCA": "BANCA",
    "CONSTRUCTORES": "DESARROLLADORES",
    "PRESIDENTE DE CONSORCIO": "CONSORCIO",
    "LIDERES COMUNITARIOS": "COMUNITARIOS",
    "ADMINITRACION DE CONDOMINIO": "CONDOMINIOS",
    "Directores y Encargados Instituciones CJB": "CJB",
    "MEDIOS": "MEDIOS"
}

def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).strip()
    return " ".join(text.split())

def to_title_case(text):
    if not text:
        return ""
    # Capitalize first letter of each word
    return text.title()

def process_file():
    print(f"Leyendo {INPUT_FILE}...")
    
    # Leer el Excel sin headers para detectar la estructura
    df = pd.read_excel(INPUT_FILE, header=None)
    
    processed_rows = []
    seen_guests = set()
    current_sector = "INVITADO" # Default
    
    # Iterar filas
    for index, row in df.iterrows():
        col0 = clean_text(row[0])
        col1 = clean_text(row[1])
        
        # 1. Detectar Headers de Sector
        found_sector = False
        for key, value in SECTOR_MAP.items():
            if key in col0:
                current_sector = value
                print(f"--- Sector detectado: {key} -> {current_sector}")
                found_sector = True
                break
        
        if found_sector:
            continue
            
        # 2. Detectar Filas de Datos
        if col0.lower() == "no" or col1.lower() == "cargo" or "nombre" in str(row[2]).lower():
            continue
            
        raw_nombre = clean_text(row[2])
        raw_apellido = clean_text(row[3])
        cargo = clean_text(row[1])
        
        if not raw_nombre:
            continue
            
        if raw_nombre.lower() == "nombre" or cargo.lower() == "cargo":
            continue
            
        # Normalización
        nombre = to_title_case(raw_nombre)
        apellido = to_title_case(raw_apellido)
        
        # Limpiar apellidos vacíos o "Nan"
        if not apellido or apellido.lower() == "nan":
            apellido = ""
            
        # Detección de duplicados
        guest_key = f"{nombre}|{apellido}".lower()
        
        if guest_key in seen_guests:
            print(f"DUPLICADO ELIMINADO: {nombre} {apellido} ({current_sector})")
            continue
            
        seen_guests.add(guest_key)
        
        # Asignar Fila Aleatoria
        fila = random.choice(string.ascii_uppercase) # A-Z
        
        processed_rows.append({
            "Nombre": nombre,
            "Apellido": apellido,
            "Sector": current_sector,
            "Cargo": cargo,
            "Fila": fila
        })

    # Crear DataFrame final
    df_final = pd.DataFrame(processed_rows)
    
    if df_final.empty:
        print("ADVERTENCIA: No se detectaron filas. Revisar lógica.")
    else:
        print(f"Procesadas {len(df_final)} filas únicas.")
        
        # Guardar CSV
        df_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print(f"Archivo generado exitosamente: {OUTPUT_FILE}")

if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"ERROR: No se encuentra el archivo {INPUT_FILE}")
    else:
        process_file()
