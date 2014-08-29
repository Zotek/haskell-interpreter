import ply.yacc as yacc

from lexer import tokens

def p_general_expression(p):
    '''generalexpression : expression
                          | boolexpr'''
    p[0] = p[1]

#integer arithmetics

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]


def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]


def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]


def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]


def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]


#bool arithmetics

def p_boolexpr_boolterm(p):
    'boolexpr : boolterm'
    p[0] = p[1]

def p_bool_or(p):
    'boolexpr : boolexpr OR boolterm'
    p[0] = p[1] or p[3]

def p_bool_and(p):
    'boolexpr : boolexpr AND boolterm'
    p[0] = p[1] and p[3]


def p_not_boolterm(p):
    'boolterm : NOT boolterm'
    p[0] = not p[2]

def p_boolterm_boolval(p):
    'boolterm : boolval'
    p[0] = p[1]

def p_boolval_bool(p):
    'boolval : BOOL'
    p[0] = p[1]

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

while True:
    try:
        s = raw_input('> ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print result


def p_error(p):
    print "Syntax error in input"


parser = yacc.yacc()
