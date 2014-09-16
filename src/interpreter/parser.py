import ply.yacc as yacc
import ast
import nodeVisitor
from lexer import tokens



precedence = (
               ('left', 'GT', 'LT', 'GE', 'LE', 'EQUALS', 'NEQUALS'),
               ('left', 'PLUS', 'MINUS'),
               ('left', 'TIMES', 'DIVIDE'),
)

def p_statement(p):
    '''statement : fundef
                 | parameters'''
    ret = p[1]
    if isinstance(ret, list):
        if len(ret) == 1:
            ret = ret[0]
        else:
            ret = ast.Call(ret[0], ret[1:],None,None,None)

    p[0] = ret


def p_if(p):
    '''statement : IF atom THEN statement ELSE statement
    '''
    p[0] = ast.If(p[2],p[4],p[6])

#functions
def p_parameters(p):
    '''parameters : parameters atom
                  | atom
    '''
    if len(p) == 2: p[0] = [p[1]]
    elif len(p) == 3: p[0] = p[1] + [p[2]]

def p_fundef(p):
    '''fundef : parameters ASSIGN atom'''
    p[0] = ast.FunctionDef(p[1][0], p[1][1:], p[3], None)

#general
def p_assignment(p):
    '''statement : LET atom ASSIGN atom'''
    p[0] = ast.Assign(p[2],p[4])

def p_atom_id(p):
    '''atom : IDENTIFIER'''
    p[0] = ast.Name(p[1],None)

def p_atom_number(p):
    '''atom : NUMBER'''
    p[0] = ast.Num(p[1])

def p_atom_bool(p):
    '''atom : BOOL'''
    p[0] = ast.BoolOp(None,[p[1]])


def p_atom_list(p):
    '''atom : list'''
    p[0] = p[1]


def p_atom_tuple(p):
    '''atom : tuple'''
    p[0] = p[1]

#integer arithmetics

def p_expression_operation(p):
    '''atom : atom PLUS atom
            | atom MINUS atom
            | atom TIMES atom
            | atom DIVIDE atom'''
    p[0] = ast.BinOp(p[1], {'+': ast.Add, '-': ast.Sub, '*': ast.Mult, '/': ast.Div}[p[2]], p[3])

def p_factor_expr(p):
    'atom : LPAREN statement RPAREN'

    ret = p[2]
    if isinstance(ret, list):
        if len(ret) == 1:
            ret = ret[0]
        else:
            ret = ast.Call(ret[0], ret[1:],None,None,None)

    p[0] = ret

#tuples and lists

def p_tuple(p):
    'tuple : LPAREN sequence RPAREN'
    p[0] = ast.Tuple(p[2], ast.Store())

def p_sequence(p):
    'sequence : atom COMMA atom'
    p[0] = [p[1], p[3]]

def p_sequence_generalexpression(p):
    'sequence : sequence COMMA statement'
    p[0] = p[1] + [p[3]]

def p_list(p):
    'list : LBRACKET sequence RBRACKET'
    p[0] = ast.List(p[2], ast.Store())

def p_list_singleelem(p):
    'list : LBRACKET statement RBRACKET'
    p[0] = ast.List([p[2]], ast.Store())

def p_list_empty(p):
    'list : LBRACKET RBRACKET'
    p[0] = ast.List([], ast.Store())

def p_list_prepand(p):
    'list : atom COLON atom'
    p[0] = ast.BinOp(ast.List([p[1]], ast.Store), ast.Add, p[3])

def p_list_INDEX(p):
    'atom : atom INDEX atom'
    p[0] = ast.Subscript(p[1], ast.Index(p[3]), ast.Load())

def p_list_CONCAT(p):
    'list : atom CONCAT atom'
    p[0] = ast.BinOp(p[1], ast.Add, p[3])

def p_list_range(p):
    '''list : LBRACKET atom COMMA atom RANGE atom RBRACKET
            | LBRACKET atom RANGE atom RBRACKET'''
    if len(p) == 8:
        p[0] = ast.Subscript(None, ast.Slice(p[2], p[6], ast.BinOp(p[4], ast.Sub, p[2])), ast.Load())
    else:
        p[0] = ast.Subscript(None, ast.Slice(p[2], p[4], ast.Num(1)), ast.Load())

def p_list_STRING(p):
    'list : STRING'
    p[0] = ast.List(list(p[1]), ast.Store())

#bool arithmetics


def p_bool_or(p):
    'atom : atom OR atom'
    p[0] = ast.BoolOp(ast.Or,[p[1],p[3]])

def p_bool_and(p):
    'atom : atom AND atom'
    p[0] = ast.BoolOp(ast.And,[p[1],p[3]])


def p_not_boolterm(p):
    'atom : NOT atom'
    p[0] = ast.BoolOp(ast.Not,[p[2]])


def p_char(p):
    'atom : CHAR'
    p[0] = p[1]

def p_bool(p):
    '''atom : FALSE
            | TRUE'''
    p[0] = p[1]

#integer comparison

def p_comparison(p):
    '''atom       : atom GT atom
                  | atom LT atom
                  | atom GE atom
                  | atom LE atom
                  | atom EQUALS atom
                  | atom NEQUALS atom'''
    operator = None
    if p[2] == ">": operator = ast.Gt
    elif p[2] == ">=": operator = ast.GtE
    elif p[2] == "<": operator = ast.Lt
    elif p[2] == "<=": operator = ast.LtE
    elif p[2] == "==": operator = ast.Eq
    elif p[2] == "/=": operator = ast.NotEq
    p[0] = ast.Compare(p[1],[operator],[p[3]])

# Build the parser
parser = yacc.yacc()
visitor = nodeVisitor.HaskellASTVisitor()
while True:
    try:
        s = raw_input('> ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print visitor.visit(result)


def p_error(p):
    print "Syntax error in input"

