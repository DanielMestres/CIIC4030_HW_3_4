# --------------------------------------------------------
# Daniel Mestres Pinero_802-15-4744
# CIIC4030-036
# Assignment_3_Scanner
# Run: (Linux)
#   python3 scanner.py input_file_name
# References:
#   https://www.dabeaz.com/ply/ply.html
#   https://www.skenz.it/compilers/ply
# --------------------------------------------------------
from ply import lex as lex
from ply import yacc as yacc
import sys
import logging

##########################_Scanner_################################

# Reserved words map ('word' : 'TOKEN')
words = {
    'if'    : 'IF',    'then'  : 'THEN',
    'else'  : 'ELSE',  'map'   : 'MAP',
    'to'    : 'TO',    'let'   : 'LET',
    'in'    : 'IN',    'null'  : 'NULL',

    'true'  : 'BOOL',  'false' : 'BOOL',

    'number?'   : 'PRIM', 'function?' : 'PRIM',
    'list?'     : 'PRIM', 'null?'     : 'PRIM',
    'cons?'     : 'PRIM', 'cons'      : 'PRIM',
    'first'     : 'PRIM', 'rest'      : 'PRIM',
    'arity'     : 'PRIM'
}

# Token list
tokens = [
    'INT',

    'ID',
    'IF',
    'THEN',
    'ELSE',
    'MAP',
    'TO',
    'LET',
    'IN',
    'NULL',
    'BOOL',
    'PRIM',

    'DELIMITER',
    'SIGN',
    'BINOP'
]

# Rules
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_COMMENT(t):
    r'\#.*'
    pass

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore  = ' \t'
t_INT = r'\d+'
t_DELIMITER = r'\(|\)|\[|\]|\,|\;'
t_SIGN = r'\+|\-'
t_BINOP = r'\~|\*|\/|\=|\!=|\<|\>|\<=|\>=|\&|\||\:='

# AlphaOther {AlphaOtherNumeric}*
def t_ID(t):
    r'[a-zA-Z_?][a-zA-Z0-9_?]*'
    # Checks for reserved words
    t.type = words.get(t.value, 'ID')
    return t

##########################_Debug_&_Building_#############################

# Build scanner
lexer = lex.lex()

# Open and input
data = open(sys.argv[1])

# Scanner input
with data as fp:
    for line in fp:
        try:
            lexer.input(line)

            for tok in lexer:
                print(tok)
        except EOFError:
            break
