# --------------------------------------------------------
# Daniel Mestres Pinero_802-15-4744
# CIIC4030-036
# Assignment_3_Scanner
# Server Functional Declarative Language
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

############################_Lexer_################################

# Reserved words map ('id' : 'TOKEN')
words = {
    'start-remote' : 'START_REMOTE',
    'start-local' : 'START_LOCAL',
    'set-port'  : 'SET_PORT',
    'get-server'    : 'GET_SERVER',
    'send' : 'SEND',
    'end'  : 'END'
}

# Token list
tokens = [
    'ID',
    'NUM',
    'DELIMITER',

    'START_REMOTE',
    'START_LOCAL',
    'SET_PORT',
    'GET_SERVER',
    'SEND',
    'END'
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

t_DELIMITER = r'\(|\)|\"|\"'

# AlphaOther {AlphaOtherNumeric}*
def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_-]*'
    # Checks for reserved words
    t.type = words.get(t.value, 'ID')
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

############################_Parser_##################################
# TODO: Implement for assignment 4

##########################_Build_&_Debug_#############################

# Build scanner
lexer = lex.lex()

# Open and input
data = open(sys.argv[1])

# Scanner input
lexer.input(data.read())

while True:
    tok = lexer.token()
    if not tok: break
    print(tok)
