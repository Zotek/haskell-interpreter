import ply.yacc as yacc
import ast
import nodeVisitor
from lexer import tokens


# _globals = {
#     'fst': (lambda x: x[0] if isinstance(x, tuple) and len(x) == 2 else None),
#     'snd': (lambda x: x[1] if isinstance(x, tuple) and len(x) == 2 else None)
# }

def p_statement(p):
    '''statement : generalexpression
                 | assignment
                 | fundef'''
    p[0] = p[1]


#functions
def p_fundef(p):
    '''fundef : IDENTIFIER argument-list ASSIGN generalexpression'''
    p[0] = ast.FunctionDef(p[1],p[2],p[4],None)

def p_argument_list(p):
    '''argument-list : IDENTIFIER argument-list
                     | IDENTIFIER
    '''
    if len(p) == 2: p[0] = [p[1]]
    elif len(p) == 3: p[0] = [p[1]] + p[2]

def p_parameters(p):
    '''parameters : atom parameters
                  | atom
    '''
    if len(p) == 2: p[0] = [p[1]]
    elif len(p) == 3: p[0] = [p[1]] + p[2]

def p_funcall(p):
    '''funcall : IDENTIFIER parameters
    '''
    p[0] = ast.Call(p[1],p[2],None,None,None)

#general
def p_assignment(p):
    '''assignment : LET IDENTIFIER ASSIGN generalexpression'''
    p[0] = ast.Assign(p[2],p[4])

def p_general_expression(p):
    '''generalexpression : expression
                          | boolexpr
                          | STRING
                          | CHAR
                          | funcall
                          | tuple
                          | list'''

    p[0] = p[1]

def p_atom_id(p):
    '''atom : IDENTIFIER'''
    p[0] = ast.Name(p[1],None)

def p_atom_number(p):
    '''atom : NUMBER'''
    p[0] = ast.Num(p[1])

def p_atom_bool(p):
    '''atom : BOOL'''
    p[0] = ast.BoolOp(None,[p[1]])

#integer arithmetics

def p_expression_operation(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    operator = ast.Add if p[2]=="+" else ast.Sub
    p[0] = ast.BinOp(p[1],operator,p[3])



def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_operation(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    operator = ast.Mult if p[2]=="*" else ast.Div
    p[0] = ast.BinOp(p[1],operator,p[3])



def p_term_factor(p):
    'term : factor'
    p[0] = p[1]



def p_factor_atom(p):
    '''factor : atom'''
    p[0] = p[1]


def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

#tuples and lists

def p_tuple(p):
    'tuple : LPAREN sequence RPAREN'
    p[0] = ast.Tuple(p[2], ast.Store())

def p_sequence(p):
    'sequence : generalexpression COMMA generalexpression'
    p[0] = [p[1], p[3]]

def p_sequence_generalexpression(p):
    'sequence : sequence COMMA generalexpression'
    p[0] = p[1] + [p[3]]

def p_list(p):
    'list : LBRACKET sequence RBRACKET'
    p[0] = ast.List(p[2], ast.Store())

def p_list_prepand(p):
    'list : generalexpression COLON list'
    p[0] = ast.List([p[1]] + p[3].elts, ast.Store())

def p_list_INDEX(p):
    'generalexpression : list INDEX expression'
    p[0] = ast.Subscript(p[1], ast.Index(p[3]), ast.Load())

def p_list_CONCAT(p):
    'list : list CONCAT list'
    p[0] = ast.List(p[1].elts + p[3].elts, ast.Store())

#bool arithmetics

def p_boolexpr_boolterm(p):
    'boolexpr : boolterm'
    p[0] = p[1]

def p_bool_or(p):
    'boolexpr : boolexpr OR boolterm'
    p[0] = ast.BoolOp(ast.Or,[p[1],p[3]])

def p_bool_and(p):
    'boolexpr : boolexpr AND boolterm'
    p[0] = ast.BoolOp(ast.And,[p[1],p[3]])


def p_not_boolterm(p):
    'boolterm : NOT boolterm'
    p[0] = ast.BoolOp(ast.Not,[p[2]])

def p_boolterm_boolval(p):
    'boolterm : boolval'
    p[0] = p[1]

def p_boolval_atom(p):
    '''boolval : atom'''
    p[0] = p[1]

def p_boolval_boolexpr(p):
    'boolval : LPAREN boolexpr RPAREN'
    p[0] = p[2]

#integer comparison

def p_boolval_comparison(p):
    'boolval : comparison'
    p[0] = p[1]

def p_comparison(p):
    '''comparison : expression GT expression
                  | expression LT expression
                  | expression GE expression
                  | expression LE expression
                  | expression EQUALS expression
                  | expression NEQUALS expression'''
    operator = None
    if p[2] == ">": operator = ast.Gt
    elif p[2] == ">=": operator = ast.GtE
    elif p[2] == "<": operator = ast.Lt
    elif p[2] == "<=": operator = ast.LtE
    elif p[2] == "==": operator = ast.Eq
    elif p[2] == "!=": operator = ast.NotEq
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

