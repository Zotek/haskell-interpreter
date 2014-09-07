import ply.lex as lex

keywords = ('TRUE', 'FALSE', 'NOT')

tokens = keywords + (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'NEQUALS', 'LPAREN', 'RPAREN', 'OR', 'AND', 'BOOL', 'GT', 'LT', 'GE',
    'LE', 'SUCC', 'MIN', 'COMMA', 'STRING', 'CHAR', 'IDENTIFIER'
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'=='
t_NEQUALS = r'/='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_OR = r'\|\|'
t_AND = r'\&\&'
t_NOT = r'not'
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_COMMA = r','

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_STRING(t):
    r'\"[^\"]*\"'
    t.value = t.value[1:-1]
    return t

def t_CHAR(t):
    r'\'[^\']\''
    t.value = t.value[1]
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    return t

def t_BOOL(t):
    r'True|False'
    if (t.value == 'True'):
        t.value = True
    else:
        t.value = False
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lex.lex()
