import sys 
import traceback

def limpiar_informacion(datos:bytes, i:int) -> int: 
    n = len(datos)
    while i < n:
        linea = datos[i]
        if linea in b"\t\r\n ":
            i += 1
            continue
        if linea == ord("#"):
            while i < n and datos[i] not in (10,13):
                 i += 1
            continue
        break
    return i

def obtener_informacion(datos:bytes, i:int):
    info = limpiar_informacion(datos, i)
    if info >= len(datos):
        raise ValueError("No se encontró información despues de limpiar los datos")
    inicio = info
    while info < len(datos) and datos[info] not in b"\t\r\n# ":
        info += 1
    token = datos[inicio:info].decode("ascii")
    return token, info

def leer_imagen(path:str):
    data = open(path, "rb").read()
    i = 0

    formato, i = obtener_informacion(data, i)
    if formato not in ("P5", "P2"):
        raise ValueError("Formato no soportado: {}".format(formato))
    
    ancho, i = obtener_informacion(data, i)
    ancho = int(ancho)
    alto, i = obtener_informacion(data, i)
    alto = int(alto)

    max_valor, i = obtener_informacion(data, i)
    max_valor = int(max_valor)

    if max_valor > 255:
        raise ValueError("Valor máximo no soportado: {}".format(max_valor))
    if ancho <= 0 or alto <= 0:
        raise ValueError("Dimensiones no válidas: {}x{}".format(ancho, alto))
    
    i = limpiar_informacion(data, i)
    pixeles = ancho * alto

    if formato == "P5":
        if i + pixeles > len(data):
            raise ValueError("No hay suficientes datos para los pixeles")
        imagen = data[i:i+pixeles]
    else:
        valores = []
        index = i 
        for _ in range(pixeles):
            t , index = obtener_informacion(data, index)
            valor = int(t)
            if not (0 <= valor <= max_valor):
                raise ValueError("Valor de pixel fuera de rango: {}".format(valor))
            valores.append(valor)
        imagen = bytes(valores)

    header = f"P5\n{ancho} {alto}\n{max_valor}\n".encode("ascii")
    return ancho, alto, max_valor, imagen, header

def escribir_pgm(path:str, header:bytes, pixeles:bytes):
    with open(path, "wb") as f:
        f.write(header)
        f.write(pixeles)

def bytes_matriz(imagen:bytes, ancho:int, alto:int):
    matriz = []
    for i in range(alto):
        fila = []
        for j in range(ancho):
            fila.append(imagen[i*ancho + j])
        matriz.append(fila)
    return matriz

def matriz_bytes(matriz) -> bytes:
    pixeles = []
    for fila in matriz:
        pixeles.extend(fila)
    return bytes(pixeles)

def vecinos(x:int, y:int, ancho:int, alto:int, conectividad:int):
    desplazamientos = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]
    vecinos = []
    for dx, dy in desplazamientos:
        nx, ny = x + dx, y + dy
        if 0 <= nx < ancho and 0 <= ny < alto:
            vecinos.append((nx, ny))
    return vecinos

def obtener_flat_zone(matriz,ancho:int, alto_int, x:int, y:int, conectividad:int):
    valor = matriz[y][x]
    visitado = [[False] * ancho for _ in range(alto_int)]
    pila = [(x, y)]
    visitado[y][x] = True
    zona = []

    while pila:
        cx, cy = pila.pop()
        zona.append((cx, cy))
        for nx, ny in vecinos(cx, cy, ancho, alto_int, conectividad):
            if not visitado[ny][nx] and matriz[ny][nx] == valor:
                visitado[ny][nx] = True
                pila.append((nx, ny))
    return zona, valor

def es_minimo_regional(matriz, ancho:int, alto:int, zona, valor:int,conectividad:int):
    zona_set = set(zona)

    for x, y in zona:
        for nx, ny in vecinos(x, y, ancho, alto, conectividad):
            if (nx, ny) not in zona_set and matriz[ny][nx] <= valor:
                    return False
    return True

def main():
    if len(sys.argv) != 3:
        print("Uso: python exercise_13c_minimum.py input.pgm input.pgm output.pgm")
        sys.exit(2)

    input_pgm, output_pgm = sys.argv[1], sys.argv[2]
    ancho, alto, max_valor, imagen, header = leer_imagen(input_pgm)    
    matriz = bytes_matriz(imagen, ancho, alto)
    visitado = [[False for _ in range(ancho)] for _ in range(alto)]
    resultado = [[0 for _ in range(ancho)] for _ in range(alto)]

    for y in range(alto):
        for x in range(ancho):
            if not visitado[y][x]:
                zona, valor = obtener_flat_zone(matriz, ancho, alto, x, y, conectividad=8)
                if es_minimo_regional(matriz, ancho, alto, zona, valor, valor):
                    for zx, zy in zona:
                        resultado[zy][zx] = 255
    escribir_pgm(output_pgm, header, matriz_bytes(resultado))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
