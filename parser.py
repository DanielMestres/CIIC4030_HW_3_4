# --------------------------------------------------------
# Daniel Mestres Pinero_802-15-4744
# CIIC4030-036
# Assignment_4_Parser_&_Int_Code
# Server Functional Declarative Language
# Run: (in separate terminals)
#   python3 parser.py testRemote
#   python3 parser.py testLocal
# References:
#   https://www.dabeaz.com/ply/ply.html
#   https://www.skenz.it/compilers/ply
#   https://realpython.com/python-sockets/
#   https://cs.lmu.edu/~ray/notes/pythonnetexamples/
# --------------------------------------------------------
from ply import lex as lex
from ply import yacc as yacc
import sys
import socketserver
import threading
import socket
import logging

############################_Lexer_################################

# Reserved words map ('id' : 'TOKEN')
words = {
    'start-remote' : 'START_REMOTE',
    'start-local' : 'START_LOCAL',
    'end-local' : 'END_LOCAL'
}

# Token list
tokens = [
    'ID',
    'NUM',
    'LPAREN',
    'RPAREN',

    'START_REMOTE',
    'START_LOCAL',
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
local = None

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class PrintHandler(socketserver.StreamRequestHandler):
    def handle(self):
        client = f'{self.client_address} on {threading.current_thread().name}'
        print(f'Connected: {client}')
        while True:
            data = self.rfile.readline()
            if not data:
                break
            decoded = data.decode('utf-8')
            self.wfile.write(decoded.encode('utf-8'))
            print(f"{self.client_address} says: {decoded}")
        print(f'Closed: {client}')

def runserver(port):
    with ThreadedTCPServer(('', port), PrintHandler) as server:
        print(f'The server is running...')
        server.serve_forever()

class Local:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, port):
        with self.sock as sock:
            sock.connect((socket.gethostname(), port))
            print('Enter lines of text then Ctrl+D or Ctrl+C to quit')
            while True:
                line = sys.stdin.readline()
                if not line:
                    # End of standard input, exit this entire script
                    break
                sock.sendall(f'{line}'.encode('utf-8'))
                while True:
                    data = sock.recv(128)
                    print("Server received: " + data.decode("utf-8"), end='')
                    if len(data) < 128:
                        # No more of this message, go back to waiting for next message
                        break

    def close(self):
        self.sock.close

############################_Parser_##################################
def p_program(p):
    ''' program : explist '''

def p_explist(p):
    ''' explist : exp
                | exp explist '''

def p_exp(p):
    ''' exp : startremote
            | startlocal
            | endlocal '''

def p_startremote(p):
    ''' startremote : START_REMOTE LPAREN NUM RPAREN '''
    runserver(p[3])

def p_startlocal(p):
    ''' startlocal : START_LOCAL LPAREN NUM RPAREN '''
    global local
    local = Local()
    local.connect(p[3])

def p_endlocal(p):
    ''' endlocal : END_LOCAL '''
    # global local
    # local.close()

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
