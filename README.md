


# Análisis de Código Fuente y Generación de Código Intermedio

Este programa realiza el análisis de un código fuente escrito en un subconjunto de lenguaje de programación, generando el Árbol de Sintaxis Abstracta (AST), la tabla de símbolos y el código en tres direcciones (TAC) a partir del AST decorado.

## Estructura del Proyecto

- **entrada.py**: Contiene el código fuente a analizar. Modifica este archivo para cambiar el código fuente.
- **gramatica.py**: Define la gramática y la descripción de tokens utilizados en el análisis.
- **Main.py**: Programa principal que realiza el análisis léxico, sintáctico y semántico, generando el AST, la tabla de símbolos y el código en tres direcciones.
- **ast.txt**: Contiene la representación textual del AST generado.
- **tabla_simbolos.txt**: Contiene la tabla de símbolos con los nombres de las variables, su tipo y el número de ocurrencias.
- **tac.txt**: Contiene el código en tres direcciones generado a partir del AST decorado.

## Funcionalidades

- **Análisis Léxico**: Separa el código fuente en tokens.
- **Análisis Sintáctico**: Construye el AST a partir de la gramática definida.
- **Análisis Semántico**: Genera la tabla de símbolos y el código en tres direcciones.
- **Generación de Código Intermedio**: Produce instrucciones de tres direcciones a partir del AST decorado.

## Uso

1. Modifica el archivo `entrada.py` con el código fuente que deseas analizar.
2. Ejecuta el programa con `python Main.py`.
3. El programa mostrará el código en tres direcciones en la terminal y generará los archivos de salida.

## Ejemplo de Código Fuente

x = 1;
y = 2;
z = x + y * 5;
impr(z);

## Ejemplo de Salida

### AST

Programa
Asignar(name=x)
Numero(1.0)
Asignar(name=y)
Numero(2.0)
Asignar(name=z)
BinOp(op=SUMA)
Variable(x)
BinOp(op=MULT)
Variable(y)
Numero(5.0)
Imprimir
Variable(z)

### Tabla de Símbolos

x          tipo=num ocurrencias=2
y          tipo=num ocurrencias=2
z          tipo=num ocurrencias=2

### Código en Tres Direcciones

t1 = 1.0
t2 = 2.0
t3 = 5.0
t4 = t2 * t3
t5 = t1 + t4
z = t5
impr z

## Notas

- El análisis se realiza a partir del archivo `entrada.py`.
- El programa no guarda los archivos de salida si solo necesitas ver el resultado en la terminal.


⸻

