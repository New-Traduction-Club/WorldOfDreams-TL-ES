import re
from pathlib import Path

def contar_traduccion(directorio_base="files"):
    total = 0
    traducidas = 0
    
    regex_original = re.compile(r'^#\s*(?:[a-zA-Z0-9_]+\s+)*".*"')

    for archivo in Path(directorio_base).rglob("*.rpy"):
        with open(archivo, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            
        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line.startswith('old "'):
                total += 1
                j = i + 1
                while j < len(lines):
                    next_line = lines[j].strip()
                    if next_line.startswith('new '):
                        if next_line != 'new ""':
                            traducidas += 1
                        i = j
                        break
                    j += 1
                i += 1
                continue

            if line.startswith('#') and regex_original.search(line):
                j = i + 1
                es_valido = False
                
                while j < len(lines):
                    next_line = lines[j].strip()
                    
                    if not next_line:
                        j += 1
                        continue
                        
                    if next_line.startswith('#'):
                        j += 1
                        continue
                        
                    if next_line.startswith('translate '):
                        break
                    
                    total += 1
                    es_valido = True
                    
                    if '""' not in next_line:
                        traducidas += 1
                        
                    i = j
                    break
                
                if not es_valido:
                    i += 1
                continue
                
            i += 1
            
    return total, traducidas

def actualizar_readme(progreso_md):
    ruta_readme = Path("README.md")
    
    if not ruta_readme.exists():
        print("No readme")
        return

    readme = ruta_readme.read_text(encoding="utf-8")
    inicio_tag = "<!-- PROGRESO_TRADUCCION_START -->"
    fin_tag = "<!-- PROGRESO_TRADUCCION_END -->"
    
    inicio = readme.find(inicio_tag)
    fin = readme.find(fin_tag)

    if inicio != -1 and fin != -1 and inicio < fin:
        contenido_limpio = progreso_md.replace('# Progreso de traducción\n\n', '')
        
        nuevo_readme = (
            f"{readme[:inicio]}{inicio_tag}\n"
            f"{contenido_limpio}"
            f"{readme[fin:]}"
        )
        ruta_readme.write_text(nuevo_readme, encoding="utf-8")
    else:
        print("error")

def main():
    total, traducidas = contar_traduccion("files")
    porcentaje = (traducidas / total * 100) if total > 0 else 0
    
    progreso_md = (
        f"# Progreso de traducción\n\n"
        f"**{traducidas} de {total} líneas traducidas**\n\n"
        f"**Progreso:** {porcentaje:.2f}%\n"
    )
    
    Path("TRANSLATION_PROGRESS.md").write_text(progreso_md, encoding="utf-8")
    actualizar_readme(progreso_md)
    
if __name__ == "__main__":
    main()
