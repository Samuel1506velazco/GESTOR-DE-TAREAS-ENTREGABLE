import json
import os
from datetime import datetime

# Archivo para almacenar los clientes
ARCHIVO_CLIENTES = "clientes.json"

"""
Sistema de Gestión de Clientes:

- Registrar clientes con nombre, DNI, teléfono, correo, dirección y FECHA DE ENTREGA.
- Visualizar todos los clientes registrados.
- Actualizar datos de clientes existentes.
- Eliminar clientes.
- Importar clientes desde archivo JSON externo.
- Validación de teléfono, correo electrónico y fecha.
- Manejo de errores (try except).
- Menú interactivo.
- Persistencia de datos en archivo JSON.
"""

# --- Funciones para Clientes ---

def cargar_clientes():
    """Carga la lista de clientes desde el archivo JSON."""
    if os.path.exists(ARCHIVO_CLIENTES):
        with open(ARCHIVO_CLIENTES, "r") as archivo:
            return json.load(archivo)
    return []

def guardar_clientes(clientes):
    """Guarda la lista de clientes en el archivo JSON."""
    with open(ARCHIVO_CLIENTES, "w") as archivo:
        json.dump(clientes, archivo, indent=4)

def generar_id_cliente(clientes):
    """Genera un ID único para un nuevo cliente."""
    if not clientes:
        return 1
    return max(c["id"] for c in clientes) + 1

def validar_telefono(telefono):
    """Valida que el teléfono tenga un formato básico (solo números, longitud mínima)."""
    if telefono.isdigit() and len(telefono) >= 7:
        return telefono
    else:
        print("ERROR: Teléfono inválido. Debe contener solo números y tener al menos 7 dígitos.")
        return None

def validar_correo(correo):
    """Valida que el correo tenga un formato básico (contiene @ y .)."""
    if "@" in correo and "." in correo:
        return correo
    else:
        print("ERROR: Correo electrónico inválido. Debe contener '@' y un punto '.'")
        return None

def validar_fecha(fecha):
    """
    Valida que la fecha tenga formato YYYY-MM-DD y sea una fecha válida.
    Permite fechas pasadas, presentes y futuras (sin restricción).
    """
    try:
        fecha_agregada = datetime.strptime(fecha, "%Y-%m-%d").date()
        return fecha_agregada.strftime("%Y-%m-%d")
    except ValueError:
        print("ERROR: Formato de fecha inválido. Use YYYY-MM-DD (ej. 2025-12-31)")
        return None

def crear_cliente(clientes):
    """Crea un nuevo cliente con los datos solicitados."""
    print("\n--- NUEVO CLIENTE ---")
    
    nombre = input("Nombre completo: ")
    dni = input("DNI: ")
    
    while True:
        telefono = input("Teléfono: ")
        telefono_validado = validar_telefono(telefono)
        if telefono_validado:
            break
    
    while True:
        correo = input("Correo electrónico: ")
        correo_validado = validar_correo(correo)
        if correo_validado:
            break
    
    direccion = input("Dirección: ")
    
    while True:
        fecha_entrega = input("Fecha de entrega (YYYY-MM-DD): ")
        fecha_validada = validar_fecha(fecha_entrega)
        if fecha_validada:
            break

    cliente = {
        "id": generar_id_cliente(clientes),
        "nombre": nombre,
        "dni": dni,
        "telefono": telefono_validado,
        "correo": correo_validado,
        "direccion": direccion,
        "fecha_entrega": fecha_validada,
        "estado": "pendiente"  # Estado de la entrega: pendiente, completada, cancelada
    }

    clientes.append(cliente)
    guardar_clientes(clientes)
    print("Cliente registrado exitosamente.")

def visualizar_clientes(clientes):
    """Muestra todos los clientes registrados."""
    if not clientes:
        print("\nNo hay clientes registrados.")
        return
    
    print("\n" + "="*80)
    print("LISTA DE CLIENTES")
    print("="*80)
    
    fecha_actual = datetime.now().date()
    
    for cliente in clientes:
        # Calcular días restantes para la entrega
        fecha_entrega = datetime.strptime(cliente["fecha_entrega"], "%Y-%m-%d").date()
        dias_restantes = (fecha_entrega - fecha_actual).days
        
        # Determinar estado automático basado en la fecha
        estado_auto = ""
        if dias_restantes < 0:
            estado_auto = "VENCIDA"
        elif dias_restantes == 0:
            estado_auto = "HOY"
        elif dias_restantes <= 3:
            estado_auto = "PROXIMO"
        else:
            estado_auto = "OK"
        
        print(f"\nID: {cliente['id']}")
        print(f"Nombre: {cliente['nombre']}")
        print(f"DNI: {cliente['dni']}")
        print(f"Teléfono: {cliente['telefono']}")
        print(f"Correo: {cliente['correo']}")
        print(f"Dirección: {cliente['direccion']}")
        print(f"Fecha Entrega: {cliente['fecha_entrega']} ({dias_restantes} días) {estado_auto}")
        print(f"Estado: {cliente['estado']}")
        print("-" * 60)

def actualizar_cliente(clientes):
    """Actualiza los datos de un cliente existente."""
    try:
        id_cliente = int(input("\nIngrese el ID del cliente a actualizar: "))
    except ValueError:
        print("ERROR: ID inválido.")
        return

    for cliente in clientes:
        if cliente["id"] == id_cliente:
            print(f"\n--- Actualizando a {cliente['nombre']} ---")
            print("(Deje en blanco si no desea cambiar el valor)")
            
            nuevo_nombre = input(f"Nuevo nombre ({cliente['nombre']}): ")
            if nuevo_nombre:
                cliente["nombre"] = nuevo_nombre
            
            nuevo_dni = input(f"Nuevo DNI ({cliente['dni']}): ")
            if nuevo_dni:
                cliente["dni"] = nuevo_dni
            
            while True:
                nuevo_telefono = input(f"Nuevo teléfono ({cliente['telefono']}): ")
                if not nuevo_telefono:  # Si está vacío, mantenemos el actual
                    break
                telefono_validado = validar_telefono(nuevo_telefono)
                if telefono_validado:
                    cliente["telefono"] = telefono_validado
                    break
            
            while True:
                nuevo_correo = input(f"Nuevo correo ({cliente['correo']}): ")
                if not nuevo_correo:
                    break
                correo_validado = validar_correo(nuevo_correo)
                if correo_validado:
                    cliente["correo"] = correo_validado
                    break
            
            nueva_direccion = input(f"Nueva dirección ({cliente['direccion']}): ")
            if nueva_direccion:
                cliente["direccion"] = nueva_direccion
            
            while True:
                nueva_fecha = input(f"Nueva fecha de entrega ({cliente['fecha_entrega']}): ")
                if not nueva_fecha:
                    break
                fecha_validada = validar_fecha(nueva_fecha)
                if fecha_validada:
                    cliente["fecha_entrega"] = fecha_validada
                    break
            
            # Actualizar estado manualmente
            nuevo_estado = input(f"Nuevo estado (pendiente/completada/cancelada) [{cliente['estado']}]: ")
            if nuevo_estado in ["pendiente", "completada", "cancelada"]:
                cliente["estado"] = nuevo_estado
            elif nuevo_estado:
                print("Estado no válido. Se mantiene el anterior.")

            guardar_clientes(clientes)
            print("Cliente actualizado correctamente.")
            return
    
    print("ERROR: Cliente no encontrado.")

def eliminar_cliente(clientes):
    """Elimina un cliente por su ID."""
    try:
        id_cliente = int(input("\nIngrese el ID del cliente a eliminar: "))
    except ValueError:
        print("ERROR: ID inválido.")
        return

    for i, cliente in enumerate(clientes):
        if cliente["id"] == id_cliente:
            print(f"\nCliente a eliminar: {cliente['nombre']} - {cliente['dni']}")
            print(f"Fecha de entrega: {cliente['fecha_entrega']}")
            confirmacion = input("¿Está seguro de eliminar este cliente? (s/n): ")
            if confirmacion.lower() == 's':
                del clientes[i]
                guardar_clientes(clientes)
                print("Cliente eliminado permanentemente.")
            else:
                print("Operación cancelada.")
            return
    
    print("ERROR: Cliente no encontrado.")

def buscar_cliente(clientes):
    """Busca clientes por nombre, DNI, teléfono o fecha de entrega."""
    if not clientes:
        print("\nNo hay clientes registrados.")
        return
    
    print("\n--- BUSCAR CLIENTE ---")
    print("1. Buscar por nombre")
    print("2. Buscar por DNI")
    print("3. Buscar por teléfono")
    print("4. Buscar por fecha de entrega")
    
    opcion = input("Seleccione criterio de búsqueda: ")
    
    resultados = []
    
    if opcion == "1":
        termino = input("Ingrese nombre o parte del nombre: ").lower()
        resultados = [c for c in clientes if termino in c["nombre"].lower()]
    elif opcion == "2":
        termino = input("Ingrese DNI: ")
        resultados = [c for c in clientes if termino == c["dni"]]
    elif opcion == "3":
        termino = input("Ingrese teléfono: ")
        resultados = [c for c in clientes if termino in c["telefono"]]
    elif opcion == "4":
        termino = input("Ingrese fecha (YYYY-MM-DD): ")
        resultados = [c for c in clientes if termino == c["fecha_entrega"]]
    else:
        print("Opción inválida.")
        return
    
    if resultados:
        print(f"\nSe encontraron {len(resultados)} cliente(s):")
        for cliente in resultados:
            print(f"\nID: {cliente['id']} | Nombre: {cliente['nombre']} | Entrega: {cliente['fecha_entrega']} | Estado: {cliente['estado']}")
    else:
        print("No se encontraron clientes con ese criterio.")

def mostrar_entregas_pendientes(clientes):
    """Muestra los clientes con entregas pendientes, ordenados por fecha."""
    if not clientes:
        print("\nNo hay clientes registrados.")
        return
    
    pendientes = [c for c in clientes if c["estado"] == "pendiente"]
    
    if not pendientes:
        print("\nNo hay entregas pendientes.")
        return
    
    # Ordenar por fecha de entrega (más próxima primero)
    pendientes.sort(key=lambda c: c["fecha_entrega"])
    
    print("\n" + "="*70)
    print("ENTREGAS PENDIENTES")
    print("="*70)
    
    fecha_actual = datetime.now().date()
    
    for cliente in pendientes:
        fecha_entrega = datetime.strptime(cliente["fecha_entrega"], "%Y-%m-%d").date()
        dias_restantes = (fecha_entrega - fecha_actual).days
        
        # Indicador de urgencia
        urgencia = ""
        if dias_restantes < 0:
            urgencia = "VENCIDA"
        elif dias_restantes == 0:
            urgencia = "HOY"
        elif dias_restantes <= 3:
            urgencia = "PROXIMO"
        else:
            urgencia = "OK"
        
        print(f"\nID: {cliente['id']} | Nombre: {cliente['nombre']}")
        print(f"   Fecha Entrega: {cliente['fecha_entrega']} ({dias_restantes} días) {urgencia}")
        print(f"   Teléfono: {cliente['telefono']} | Dirección: {cliente['direccion']}")

def importar_clientes(clientes):
    """Importa clientes desde un archivo JSON externo."""
    print("\n--- IMPORTAR CLIENTES ---")
    nombre_archivo = input("Ingrese el nombre del archivo JSON a importar (ej. clientes_import.json): ")
    
    try:
        if not os.path.exists(nombre_archivo):
            print(f"ERROR: El archivo '{nombre_archivo}' no existe.")
            return
        
        with open(nombre_archivo, "r", encoding='utf-8') as archivo:
            nuevos_clientes = json.load(archivo)
        
        if not isinstance(nuevos_clientes, list):
            print("ERROR: El archivo no contiene una lista válida de clientes.")
            return
        
        print(f"\nSe encontraron {len(nuevos_clientes)} cliente(s) en el archivo.")
        
        # Validar estructura de los clientes
        clientes_validos = []
        clientes_invalidos = 0
        
        for cliente in nuevos_clientes:
            # Verificar que tenga los campos necesarios
            campos_requeridos = ["nombre", "dni", "telefono", "correo", "direccion", "fecha_entrega", "estado"]
            if all(campo in cliente for campo in campos_requeridos):
                # Validar teléfono
                if not validar_telefono(cliente["telefono"]):
                    clientes_invalidos += 1
                    print(f"  - Cliente '{cliente.get('nombre', 'Desconocido')}' omitido: teléfono inválido")
                    continue
                
                # Validar correo
                if not validar_correo(cliente["correo"]):
                    clientes_invalidos += 1
                    print(f"  - Cliente '{cliente.get('nombre', 'Desconocido')}' omitido: correo inválido")
                    continue
                
                # Validar fecha
                if not validar_fecha(cliente["fecha_entrega"]):
                    clientes_invalidos += 1
                    print(f"  - Cliente '{cliente.get('nombre', 'Desconocido')}' omitido: fecha inválida")
                    continue
                
                # Validar estado
                if cliente["estado"] not in ["pendiente", "completada", "cancelada"]:
                    cliente["estado"] = "pendiente"  # Asignar estado por defecto
                
                # Asignar nuevo ID
                cliente["id"] = generar_id_cliente(clientes)
                clientes_validos.append(cliente)
            else:
                clientes_invalidos += 1
                print(f"  - Cliente omitido: faltan campos requeridos")
        
        if clientes_validos:
            print(f"\nClientes válidos a importar: {len(clientes_validos)}")
            print("Clientes a importar:")
            for i, c in enumerate(clientes_validos, 1):
                print(f"  {i}. {c['nombre']} - {c['fecha_entrega']} - {c['estado']}")
            
            confirmacion = input(f"\n¿Desea importar estos {len(clientes_validos)} cliente(s)? (s/n): ")
            if confirmacion.lower() == 's':
                clientes.extend(clientes_validos)
                guardar_clientes(clientes)
                print(f"✓ {len(clientes_validos)} cliente(s) importado(s) exitosamente.")
                if clientes_invalidos > 0:
                    print(f"✗ {clientes_invalidos} cliente(s) omitido(s) por datos inválidos.")
            else:
                print("Operación cancelada.")
        else:
            print("No hay clientes válidos para importar.")
            
    except json.JSONDecodeError:
        print("ERROR: El archivo no tiene un formato JSON válido.")
    except Exception as e:
        print(f"ERROR inesperado: {e}")

# --- Menú Principal ---

def menu():
    """Menú principal del sistema de gestión de clientes."""
    clientes = cargar_clientes()

    while True:
        print("\n" + "="*60)
        print("GESTIÓN DE CLIENTES")
        print("="*60)
        print("1. Registrar nuevo cliente")
        print("2. Ver todos los clientes")
        print("3. Buscar cliente")
        print("4. Ver entregas pendientes")
        print("5. Actualizar cliente")
        print("6. Eliminar cliente")
        print("7. Importar clientes desde archivo")
        print("8. Salir")
        print("-" * 60)
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            crear_cliente(clientes)
        elif opcion == "2":
            visualizar_clientes(clientes)
        elif opcion == "3":
            buscar_cliente(clientes)
        elif opcion == "4":
            mostrar_entregas_pendientes(clientes)
        elif opcion == "5":
            actualizar_cliente(clientes)
        elif opcion == "6":
            eliminar_cliente(clientes)
        elif opcion == "7":
            importar_clientes(clientes)
        elif opcion == "8":
            print("\n¡Gracias por usar el sistema! Hasta pronto.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
