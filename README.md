Ejercicio 13ab:

Para ejecutar el código, se debe ubicar en la carpeta donde se encuentran los archivos de exercises_13ab en la terminal. El código recibe un archivo de entrada en formato .txt, una imagen en formato .pgm, y genera un archivo de salida en formato .txt. El archivo .txt debe contener tres líneas: la coordenada x, la coordenada y y la conectividad (generalmente 8). Para calcular si una flat zone corresponde a un mínimo regional, se ejecuta lo siguiente: 

python3 exercise_13a_minimum.py exercise_13a_input_01.txt immed_gray_inv_20051218_frgr4.pgm output_dummy.pgm. 
Para calcular si corresponde a un máximo regional, se ejecuta: 

python3 exercise_13b_maximum.py exercise_13b_input_01.txt immed_gray_inv_20051218_frgr4.pgm output_dummy.pgm.

El resultado de estos ejercicios no se refleja en la imagen de salida, sino en un archivo de texto generado automáticamente. Para el ejercicio 13a, el resultado se guarda en exercise_13a_output_01.txt, y para el ejercicio 13b en exercise_13b_output_01.txt. En estos archivos se escribe un único valor: 1 si la flat zone del píxel indicado cumple la condición de mínimo o máximo regional, o 0 si no la cumple. Para validar el funcionamiento, se pueden usar diferentes coordenadas cambiando los valores en el archivo .txt

Ejercicio 13cd:

Para ejecutar el código, se debe ubicar en la carpeta donde se encuentran los archivos de exercise_13 en la terminal. El código recibe una imagen en formato .pgm y genera una nueva imagen en formato .pgm como salida. Para calcular todas las regiones que corresponden a mínimos regionales, se ejecuta lo siguiente: 

python3 exercise_13c_minima.py immed_gray_inv_20051218_frgr4.pgm out_min.pgm. 
Para calcular las regiones que corresponden a máximos regionales, se ejecuta: 

python3 exercise_13d_maxima.py immed_gray_inv_20051218_frgr4.pgm out_max.pgm.

Las imágenes generadas como salida contienen los resultados del procesamiento. En estas imágenes, los píxeles con valor 255 representan las flat zones que cumplen la condición (mínimo o máximo regional), mientras que los píxeles con valor 0 representan el resto. Para verificar que el resultado es correcto, se pueden comparar las imágenes generadas con las imágenes de referencia proporcionadas, observando que coincidan visualmente o píxel a píxel.