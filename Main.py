from gramatica import GRAMATICA, DESCRIPCION_TOKENS

TT_ID = "ID"
TT_NUM = "NUM"
TT_ASIG = "ASIG"
TT_SUMA = "SUMA"
TT_RESTA = "RESTA"
TT_MULT = "MULT"
TT_DIV = "DIV"
TT_LPAREN = "("
TT_RPAREN = ")"
TT_SEP = "SEP"
TT_IMPR = "IMPR"
TT_EOF = "EOF"

KEYWORDS = {
    "impr": TT_IMPR,
}

class Token:
    def __init__(self, type_, value=None, line=1, col=1):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        if self.value is None:
            return f"{self.type}"
        return f"{self.type}({self.value})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1

    def current_char(self):
        if self.pos >= len(self.text):
            return None
        return self.text[self.pos]

    def advance(self):
        ch = self.current_char()
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        self.pos += 1

    def skip_whitespace(self):
        while self.current_char() is not None and self.current_char() in " \t\r":
            self.advance()

    def number(self):
        start_line, start_col = self.line, self.col
        num_str = ""
        while self.current_char() is not None and (
            self.current_char().isdigit() or self.current_char() == "."
        ):
            num_str += self.current_char()
            self.advance()
        return Token(TT_NUM, float(num_str), start_line, start_col)

    def identifier(self):
        start_line, start_col = self.line, self.col
        ident = ""
        while self.current_char() is not None and (
            self.current_char().isalnum() or self.current_char() == "_"
        ):
            ident += self.current_char()
            self.advance()
        if ident in KEYWORDS:
            return Token(KEYWORDS[ident], ident, start_line, start_col)
        return Token(TT_ID, ident, start_line, start_col)

    def get_tokens(self):
        tokens = []
        while True:
            ch = self.current_char()
            if ch is None:
                tokens.append(Token(TT_EOF, None, self.line, self.col))
                break

            if ch in " \t\r":
                self.skip_whitespace()
                continue

            if ch == "\n":
                self.advance()
                continue

            if ch.isdigit():
                tokens.append(self.number())
                continue

            if ch.isalpha() or ch == "_":
                tokens.append(self.identifier())
                continue

            if ch == "=":
                tokens.append(Token(TT_ASIG, ch, self.line, self.col))
                self.advance()
                continue

            if ch == "+":
                tokens.append(Token(TT_SUMA, ch, self.line, self.col))
                self.advance()
                continue

            if ch == "-":
                tokens.append(Token(TT_RESTA, ch, self.line, self.col))
                self.advance()
                continue

            if ch == "*":
                tokens.append(Token(TT_MULT, ch, self.line, self.col))
                self.advance()
                continue

            if ch == "/":
                tokens.append(Token(TT_DIV, ch, self.line, self.col))
                self.advance()
                continue

            if ch == "(":
                tokens.append(Token(TT_LPAREN, ch, self.line, self.col))
                self.advance()
                continue

            if ch == ")":
                tokens.append(Token(TT_RPAREN, ch, self.line, self.col))
                self.advance()
                continue

            if ch == ";":
                tokens.append(Token(TT_SEP, ch, self.line, self.col))
                self.advance()
                continue

            raise Exception(
                "Caracter ilegal %r en linea %d, columna %d"
                % (ch, self.line, self.col)
            )

        return tokens

class Node:
    pass

class Programa(Node):
    def __init__(self, bloque):
        self.bloque = bloque

class Asignar(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class Imprimir(Node):
    def __init__(self, expr):
        self.expr = expr

class BinOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class Numero(Node):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name):
        self.name = name

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[self.pos]

    def eat(self, type_):
        tok = self.current()
        if tok.type == type_:
            self.pos += 1
            return tok
        raise Exception(
            "Se esperaba %s y se encontró %s (linea %d, col %d)"
            % (type_, tok.type, tok.line, tok.col)
        )

    def parse(self):
        bloque = self.parse_bloque()
        if self.current().type != TT_EOF:
            raise Exception("Entrada extra después del fin del programa")
        return Programa(bloque)

    def parse_bloque(self):
        stmts = []
        while self.current().type in (TT_ID, TT_IMPR):
            stmts.append(self.parse_sentencia())
            if self.current().type == TT_SEP:
                self.eat(TT_SEP)
        return stmts

    def parse_sentencia(self):
        tok = self.current()
        if tok.type == TT_ID:
            name = self.eat(TT_ID).value
            self.eat(TT_ASIG)
            expr = self.parse_expresion()
            return Asignar(name, expr)
        if tok.type == TT_IMPR:
            self.eat(TT_IMPR)
            self.eat(TT_LPAREN)
            expr = self.parse_expresion()
            self.eat(TT_RPAREN)
            return Imprimir(expr)
        raise Exception(
            "Inicio de sentencia inesperado: %s (linea %d)" % (tok.type, tok.line)
        )

    def parse_expresion(self):
        node = self.parse_termino()
        while self.current().type in (TT_SUMA, TT_RESTA):
            op_tok = self.current()
            if op_tok.type == TT_SUMA:
                self.eat(TT_SUMA)
            else:
                self.eat(TT_RESTA)
            right = self.parse_termino()
            node = BinOp(op_tok.type, node, right)
        return node

    def parse_termino(self):
        node = self.parse_factor()
        while self.current().type in (TT_MULT, TT_DIV):
            op_tok = self.current()
            if op_tok.type == TT_MULT:
                self.eat(TT_MULT)
            else:
                self.eat(TT_DIV)
            right = self.parse_factor()
            node = BinOp(op_tok.type, node, right)
        return node

    def parse_factor(self):
        tok = self.current()
        if tok.type == TT_NUM:
            self.eat(TT_NUM)
            return Numero(tok.value)
        if tok.type == TT_ID:
            self.eat(TT_ID)
            return Variable(tok.value)
        if tok.type == TT_LPAREN:
            self.eat(TT_LPAREN)
            expr = self.parse_expresion()
            self.eat(TT_RPAREN)
            return expr
        raise Exception(
            "Factor inesperado %s (linea %d, col %d)" % (tok.type, tok.line, tok.col)
        )

def construir_tabla_simbolos(ast):
    tabla = {}
    def visitar(nodo):
        if isinstance(nodo, Programa):
            for s in nodo.bloque:
                visitar(s)
        elif isinstance(nodo, Asignar):
            info = tabla.get(nodo.name)
            if info is None:
                info = {"tipo": "num", "ocurrencias": 0}
                tabla[nodo.name] = info
            info["ocurrencias"] += 1
            visitar(nodo.expr)
        elif isinstance(nodo, Imprimir):
            visitar(nodo.expr)
        elif isinstance(nodo, BinOp):
            visitar(nodo.left)
            visitar(nodo.right)
        elif isinstance(nodo, Variable):
            info = tabla.get(nodo.name)
            if info is None:
                info = {"tipo": "num", "ocurrencias": 0}
                tabla[nodo.name] = info
            info["ocurrencias"] += 1
    visitar(ast)
    return tabla

def ast_a_string(ast, indent=""):
    espacio = indent
    if isinstance(ast, Programa):
        s = espacio + "Programa\n"
        for stmt in ast.bloque:
            s += ast_a_string(stmt, indent + "  ")
        return s
    if isinstance(ast, Asignar):
        s = espacio + "Asignar(name=%s)\n" % ast.name
        s += ast_a_string(ast.expr, indent + "  ")
        return s
    if isinstance(ast, Imprimir):
        s = espacio + "Imprimir\n"
        s += ast_a_string(ast.expr, indent + "  ")
        return s
    if isinstance(ast, BinOp):
        s = espacio + "BinOp(op=%s)\n" % ast.op
        s += ast_a_string(ast.left, indent + "  ")
        s += ast_a_string(ast.right, indent + "  ")
        return s
    if isinstance(ast, Numero):
        return espacio + "Numero(%s)\n" % ast.value
    if isinstance(ast, Variable):
        return espacio + "Variable(%s)\n" % ast.name
    return espacio + "Nodo_desconocido\n"

def tabla_simbolos_a_string(tabla):
    lineas = []
    lineas.append("== Tabla de símbolos ==")
    for nombre in sorted(tabla.keys()):
        info = tabla[nombre]
        lineas.append(
            "%-10s tipo=%s ocurrencias=%d"
            % (nombre, info["tipo"], info["ocurrencias"])
        )
    return "\n".join(lineas) + "\n"

class TACGenerator:
    def __init__(self):
        self.temp_count = 0
        self.code = []

    def nuevo_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generar(self, ast):
        self.code = []
        if isinstance(ast, Programa):
            for stmt in ast.bloque:
                self.gen_stmt(stmt)
        else:
            self.gen_stmt(ast)
        return self.code

    def gen_stmt(self, nodo):
        if isinstance(nodo, Asignar):
            place = self.gen_expr(nodo.expr)
            self.code.append(f"{nodo.name} = {place}")
        elif isinstance(nodo, Imprimir):
            place = self.gen_expr(nodo.expr)
            self.code.append(f"impr {place}")
        else:
            raise Exception("Sentencia desconocida en TAC")

    def gen_expr(self, nodo):
        if isinstance(nodo, Numero):
            tmp = self.nuevo_temp()
            self.code.append(f"{tmp} = {nodo.value}")
            return tmp
        if isinstance(nodo, Variable):
            return nodo.name
        if isinstance(nodo, BinOp):
            left_place = self.gen_expr(nodo.left)
            right_place = self.gen_expr(nodo.right)
            tmp = self.nuevo_temp()
            op_map = {
                TT_SUMA: "+",
                TT_RESTA: "-",
                TT_MULT: "*",
                TT_DIV: "/"
            }
            op = op_map.get(nodo.op, "?")
            self.code.append(f"{tmp} = {left_place} {op} {right_place}")
            return tmp
        raise Exception("Nodo de expresión desconocido en TAC")

def tac_a_string(tac_code):
    lineas = ["== Código en tres direcciones =="]
    for inst in tac_code:
        lineas.append(inst)
    return "\n".join(lineas) + "\n"

def main():
    print("¡Bienvenido! Todo el análisis se realiza a partir del archivo 'entrada.py'.")
    print("Modifica 'entrada.py' para cambiar el código fuente a analizar.\n")

    with open("entrada.py", "r", encoding="utf-8") as f:
        fuente = f.read()

    lexer = Lexer(fuente)
    tokens = lexer.get_tokens()

    parser = Parser(tokens)
    ast = parser.parse()

    tabla = construir_tabla_simbolos(ast)

    tac_generator = TACGenerator()
    tac_code = tac_generator.generar(ast)

    # Imprimir TAC en terminal
    print(tac_a_string(tac_code))

if __name__ == "__main__":
    main()
