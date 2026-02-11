import sys
import os
import pandas as pd

# Add parent directory to path to import database module
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import database as db

def main():
    print("Inicializando base de datos...")
    
    csv_file = os.path.join(parent_dir, 'data', 'lista_maestra.csv')
    
    if not os.path.exists(csv_file):
        print(f"ERROR: No se encuentra el archivo {csv_file}")
        return

    try:
        df = pd.read_csv(csv_file)
        print(f"Cargando {len(df)} invitados desde {csv_file}...")
        
        # Reset DB
        db.init_db()
        db.clear_guests()
        
        count = 0
        for _, row in df.iterrows():
            nombre = str(row['Nombre']).strip()
            apellido = str(row['Apellido']).strip() if not pd.isna(row['Apellido']) else ""
            sector = str(row['Sector']).strip()
            cargo = str(row['Cargo']).strip()
            fila = str(row['Fila']).strip()
            
            db.add_guest(nombre, apellido, sector, cargo, fila)
            count += 1
            
        print(f"EXITO: Base de datos recreada con {count} invitados.")
        
    except Exception as e:
        print(f"ERROR CRITICO: {e}")

if __name__ == "__main__":
    main()
