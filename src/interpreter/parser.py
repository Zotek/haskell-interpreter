import ply.yacc as yacc
import ast
import nodeVisitor
from lexer import tokens


_globals = {
    'fst': (lambda x: x[0] if isinstance(x, tuple) and len(x) == 2 else None),
    'snd': (lambda x: x[1] if isinstance(x, tuple) and len(x) == 2 else None)
}


def p_general_expression(p):
    '''generalexpression : expression
                          | boolexpr
                          | STRING
                          | CHAR'''

    p[0] = p[1]

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


def p_factor_num(p):
    'factor : NUMBER'
    p[0] = ast.Num(p[1])


def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# #tuples and lists
#
# def p_tuple(p):
#     'tuple : LPAREN sequence RPAREN'
#     p[0] = tuple(p[2])
#
# def p_sequence(p):
#     'sequence : generalexpression COMMA generalexpression'
#     p[0] = [p[1], p[3]]
#
# def p_sequence_generalexpression(p):
#     'sequence : sequence COMMA generalexpression'
#     p[0] = p[1] + [p[3]]
#
# def p_generalexpression_IDENTIFIER(p):
#     'generalexpression : IDENTIFIER generalexpression'
#     p[0] = _globals.get(p[1])(p[2])

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

def p_boolval_bool(p):
    'boolval : BOOL'
    p[0] = ast.BoolOp(None,[p[1]])

def p_boolval_boolexpr(p):
    'boolval : LPAREN boolexpr RPAREN'
    p[0] = p[2]

#integer comparison

def p_boolval_comparison(p):
    'boolval : comparison'
    p[0] = p[1]

def p_gt_comparison(p):
    'comparison : NUMBER GT NUMBER'
    p[0] = p[1] > p[3]

def p_lt_comparison(p):
    'comparison : NUMBER LT NUMBER'
    p[0] = p[1] < p[3]

def p_ge_comparison(p):
    'comparison : NUMBER GE NUMBER'
    p[0] = p[1] >= p[3]

def p_le_comparison(p):
    'comparison : NUMBER LE NUMBER'
    p[0] = p[1] <= p[3]

def p_eq_comparison(p):
    'comparison : NUMBER EQUALS NUMBER'
    p[0] = p[1] == p[3]

def p_neq_comparison(p):
    'comparison : NUMBER NEQUALS NUMBER'
    p[0] = p[1] != p[3]

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

