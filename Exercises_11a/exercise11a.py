import sys
from collections import deque

def flat_zone(pixels, ancho, alto, x, y, label):

    valor = pixels[y*ancho + x]

    salida = bytearray(ancho*alto)

    Q = deque()
    Q.append((x,y))

    salida[y*ancho + x] = label

    while Q:

        cx, cy = Q.popleft()

        for dy in [-1,0,1]:
            for dx in [-1,0,1]:

                if dx == 0 and dy == 0:
                    continue

                nx = cx + dx
                ny = cy + dy

                if nx < 0 or ny < 0 or nx >= ancho or ny >= alto:
                    continue

                indice = ny*ancho + nx

                if salida[indice] == 0 and pixels[indice] == valor:

                    salida[indice] = label
                    Q.append((nx,ny))

    return salida


def exercise_11a(txt_path, input_pgm, output_pgm):

    with open(txt_path) as f:

        x = int(f.readline())
        y = int(f.readline())
        connectivity = int(f.readline())
        label = int(f.readline())

    with open(input_pgm,"rb") as f:

        tipo = f.readline()

        dimensiones = f.readline()
        while dimensiones.startswith(b"#"):
            dimensiones = f.readline()

        maximo = f.readline()
        while maximo.startswith(b"#"):
            maximo = f.readline()

        partes = dimensiones.split()

        ancho = int(partes[0])
        alto = int(partes[1])

        pixels = bytearray(f.read())

    salida = flat_zone(pixels, ancho, alto, x, y, label)

    with open(output_pgm,"wb") as f:

        f.write(tipo)
        f.write(dimensiones)
        f.write(maximo)
        f.write(salida)


if __name__ == "__main__":

    txt_path = sys.argv[1]
    input_pgm = sys.argv[2]
    output_pgm = sys.argv[3]

    exercise_11a(txt_path, input_pgm, output_pgm)