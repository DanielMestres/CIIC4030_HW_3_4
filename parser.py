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
#   https://realpython.com/python-sockets/
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
    'send' : 'SEND',
    'end-remote'  : 'END_REMOTE',
    'end-local' : 'END_LOCAL'
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
    'SEND',
    'END_REMOTE',
    'END_LOCAL'
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
class Remote:
    def __init__(self, port):
        self.running = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((socket.gethostname(), port))
        self.s.listen(5)
        print("Waiting for connections...")

        while self.running:
            self.lSocket, self.addr = self.s.accept()
            print(f"Connection from { self.addr } has been established!")
            self.lSocket.send(bytes("Welcome to the server!", "utf-8"))

    def close(self):
        self.s.close()
        self.running = False

class Local:
    def __init__(self):
        self.running = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def find(self, port):
        self.s.connect((socket.gethostname(), port))
        while self.running:
            msg = self.s.recv(1024) # 1024 bytes
            print(msg.decode("utf-8"))

    def close(self):
        self.s.close()
        self.running = False


############################_Parser_##################################
def p_program(p):
    ''' program : explist '''

def p_explist(p):
    ''' explist : exp
                | exp explist '''

def p_exp(p):
    ''' exp : startremote
            | startlocal
            | send
            | endremote
            | endlocal '''

def p_startremote(p):
    ''' startremote : START_REMOTE LPAREN NUM RPAREN '''
    remote = Remote(p[3])

def p_startlocal(p):
    ''' startlocal : START_LOCAL LPAREN NUM RPAREN '''
    local = Local()
    local.find(p[3])

def p_send(p):
    ''' send : SEND LPAREN QUOTE idlist QUOTE RPAREN '''

def p_endremote(p):
    ''' endremote : END_REMOTE '''
    remote.close()

def p_endlocal(p):
    ''' endlocal : END_LOCAL '''
    local.close()

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
