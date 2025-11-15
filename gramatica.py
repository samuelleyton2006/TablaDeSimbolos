GRAMATICA = """
Programa   -> Bloque EOF

Bloque     -> Sentencia (SEP Sentencia)*

Sentencia  -> Asignacion
            | Impresion

Asignacion -> ID ASIG Expresion

Impresion  -> IMPR '(' Expresion ')'

Expresion  -> Termino ((SUMA | RESTA) Termino)*

Termino    -> Factor ((MULT | DIV) Factor)*

Factor     -> NUM
            | ID
            | '(' Expresion ')'
"""

DESCRIPCION_TOKENS = """
Tokens:
  ID       : identificadores (letras, dígitos, '_', empezando por letra o '_')
  NUM      : números reales (ej: 3, 4.5, 10.0)
  ASIG     : asignación (ej: '=')
  SUMA     : suma (ej: '+')
  RESTA    : resta (ej: '-')
  MULT     : multiplicación (ej: '*')
  DIV      : división (ej: '/')
  '(' ')'  : paréntesis
  SEP      : separador de sentencias (ej: ';')
  IMPR     : palabra reservada para impresión (ej: 'impr')
  EOF      : fin de entrada
"""
