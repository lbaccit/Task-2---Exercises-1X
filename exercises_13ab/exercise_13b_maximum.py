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

    return ancho, alto, max_valor, imagen

def bytes_matriz(imagen:bytes, ancho:int, alto:int):
    matriz = []
    for i in range(alto):
        fila = []
        for j in range(ancho):
            fila.append(imagen[i*ancho + j])
        matriz.append(fila)
    return matriz

def leer_parametros(path:str):
    with open(path, "r", encoding="utf-8") as f:
        lineas = [line.strip() for line in f if line.strip() != ""]
    if len(lineas) < 3:
        raise ValueError("Archivo de parámetros debe contener al menos 3 líneas")
    x = int(lineas[0])
    y = int(lineas[1])
    conectividad = int(lineas[2])
    return x, y, conectividad

def vecinos(x:int, y:int, ancho:int, alto:int, conectividad:int):
    if conectividad == 4:
        desplazamientos = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    else:
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

def es_maximo_regional(matriz, ancho:int, alto:int, zona, valor:int,conectividad:int):
    zona_set = set(zona)

    for x, y in zona:
        for nx, ny in vecinos(x, y, ancho, alto, conectividad):
            if (nx, ny) not in zona_set and matriz[ny][nx] >= valor:
                    return 0
    return 1

def main():
    if len(sys.argv) != 4:
        print("Uso: python exercise_13a_maximum.py input.txt input.pgm output.pgm")
        sys.exit(2)

    input_txt, input_pgm, _ = sys.argv[1], sys.argv[2], sys.argv[3]

    x, y, conectividad = leer_parametros(input_txt)
    ancho, alto, max_valor, imagen = leer_imagen(input_pgm)

    if not (0 <= x < ancho and 0 <= y < alto):
        raise ValueError("Coordenadas fuera de rango: ({}, {})".format(x, y))
    
    zona, valor = obtener_flat_zone(matriz=bytes_matriz(imagen, ancho, alto), ancho=ancho, alto_int=alto, x=x, y=y, conectividad=conectividad)

    matriz = bytes_matriz(imagen, ancho, alto)
    resultado = es_maximo_regional(matriz, ancho, alto, zona, valor, conectividad)

    with open("exercise_13b_output.txt", "w", encoding="utf-8") as f:
        f.write(str(resultado) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
