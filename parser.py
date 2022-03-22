# --------------------------------------------------------
# Daniel Mestres Pinero_802-15-4744
# CIIC4030-036
# Assignment_3_&_4_Scanner_&_Parser
# Run: (Linux)
#   python3 file.py input_file_name
# References:
#   https://www.dabeaz.com/ply/ply.html
#   https://www.skenz.it/compilers/ply
# --------------------------------------------------------
from ply import lex as lex
from ply import yacc as yacc
import sys
import logging

##########################_Scanner_#############################

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

##########################_Parser_##############################

# Parser grammar rules, Personalize
def p_exp(p):
    '''exp : term
           | term SIGN exp
           | term BINOP exp
           | IF exp THEN exp ELSE exp
           | LET defplus IN exp
           | IN exp
           | MAP idlist TO exp
           | MAP TO exp
    '''
    pass

def p_term(p):
    '''term : factor
            | SIGN term
            | BINOP term
            | factor DELIMITER explist DELIMITER
            | NULL
            | INT
            | BOOL
    '''

def p_factor(p):
    '''factor : DELIMITER exp DELIMITER
              | PRIM
              | ID
    '''
    pass

def p_explist(p):
    '''explist : propexplist
    '''
    pass

def p_propexplist(p):
    '''propexplist : exp
                   | exp DELIMITER propexplist
    '''
    pass

def p_idlist(p):
    '''idlist : propidlist
    '''

def p_propidlist(p):
    '''propidlist : ID
                  | ID DELIMITER propidlist
    '''
    pass

def p_defplus(p):
    '''defplus : def
               | def defplus
    '''
    pass

def p_def(p):
    '''def : ID BINOP exp DELIMITER
    '''
    pass

# Error rule for syntax errors
def p_error(p):
    if p:
        print("Syntax error in input!", p, "line:", p.lexer.lineno)
        parser.errok()

##########################_Debug_&_Building_#############################

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
