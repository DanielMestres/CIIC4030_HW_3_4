# --------------------------------------------------------
# Daniel Mestres Pinero_802-15-4744
# CIIC4030-036
# Assignment_4_Parser_&_Int_Code
# Server Functional Declarative Language
# Run: (Linux)
#   python3 parser.py input_file
# References:
#   https://www.dabeaz.com/ply/ply.html
#   https://www.skenz.it/compilers/ply
# --------------------------------------------------------
from ply import lex as lex
from ply import yacc as yacc
import sys
import socket
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
    'LPAREN',
    'RPAREN',
    'QUOTE',

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

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_QUOTE = r'\"'

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

#######################_Intermediate_Code_############################
# TODO: use socket lib

############################_Parser_##################################
# TODO: implement intermediate code
def p_program(p):
    ''' program : explist '''

def p_explist(p):
    ''' explist : exp
                | exp explist '''

def p_exp(p):
    ''' exp : startremote
            | startlocal
            | setport
            | getserver
            | send
            | end '''

def p_startremote(p):
    ''' startremote : START_REMOTE '''

def p_startlocal(p):
    ''' startlocal : START_LOCAL '''

def p_setport(p):
    ''' setport : SET_PORT LPAREN NUM RPAREN '''

def p_getserver(p):
    ''' getserver : GET_SERVER LPAREN NUM RPAREN '''

def p_send(p):
    ''' send : SEND LPAREN QUOTE idlist QUOTE RPAREN '''

def p_end(p):
    ''' end : END '''

def p_idlist(p):
    ''' idlist : ID
               | NUM
               | NUM idlist
               | ID idlist '''


# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error in input!", p, "line:", p.lexer.lineno)
        parser.errok()

##########################_Build_&_Debug_#############################

# Set up a logging object
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

# Build scanner and parser with logger
lexer = lex.lex()
parser = yacc.yacc(debug=True, debuglog=log)

# Open and Read input
data = open(sys.argv[1])

# Parse input
parser.parse(data.read())
