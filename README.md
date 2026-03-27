Ejercicio 3ab:

Para ejecutar el código, se debe ubicar en la carpeta de exercise_03 en la terminal. El código recibe 1 imagen en formato .pgm, un valor size que indica el tamaño de la operación morfológica, y genera una imagen de salida en formato .pgm. Para calcular la erosión de la imagen, toca ejecutar lo siguiente: python3 exercise_03a_erosion.py immed_gray_inv.pgm 1 out_ero1.pgm Y para calcular la dilatación, se ejecuta lo siguiente: python3 exercise_03b_dilation.py immed_gray_inv.pgm 1 out_dil1.pgm

Si se desea aplicar la operación con un tamaño mayor, simplemente se cambia el valor de size; por ejemplo, usando 2 se obtiene una erosión o dilatación equivalente a aplicar la operación elemental dos veces consecutivas
