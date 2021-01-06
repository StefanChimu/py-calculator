import ply.lex as lex
import ply.yacc as yacc
import math

# tokens def

tokens = ['INT', 'FLOAT', 'PLUS', 'MINUS', 'DIVIDE', 'MULTIPLY', 'POW', 'SQRT',
          'LPAREN', 'RPAREN', 'COMMA', 'LOGARITHM']

# basic operations

t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_MULTIPLY = r'\*'
t_POW = r'\^'
t_SQRT = r'\//'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA = r'\,'
t_LOGARITHM = r'\@'

t_ignore = r' '

# representation of every type

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Bad characters!\n")
    t.lexer.skip(1)

# operation priority

precedence = (('left', 'PLUS', 'MINUS'),
              ('left', 'POW', 'MULTIPLY', 'DIVIDE'),
              ('right', 'UMINUS', 'RAD', 'LOG'))

def p_calc(p):
    '''
    calc : expression
         | empty
    '''
    print(eval(p[1]))

def p_expression_rad(p):
    'expression : SQRT expression %prec RAD'
    p[0] = math.sqrt(p[2])

def p_expression_log(p):
    'expression : LOGARITHM expression %prec LOG'
    p[0] = math.log(p[2][1], p[2][2])

def p_binop(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression POW expression
               | expression PLUS expression
               | expression MINUS expression
               | expression COMMA expression
    '''
    p[0] = (p[2], p[1], p[3])  # 1 + 2 => (+, (1, 2))

def p_expression_uminus(p):
    '''
    expression : MINUS expression %prec UMINUS
    '''
    p[0] = -p[2]

def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0] = p[1]

def p_expression_paren(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    p[0] = p[2]

def p_error(p):
    print("Syntax error occured!\n")

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None


parser = yacc.yacc()
lexer = lex.lex()


def eval(p):
    if type(p) == tuple:
        if p[0] == '+':
            return eval(p[1]) + eval(p[2])
        elif p[0] == '-':
            return eval(p[1]) - eval(p[2])
        elif p[0] == '*':
            return eval(p[1]) * eval(p[2])
        elif p[0] == '/':
            return eval(p[1]) / eval(p[2])
        elif p[0] == '^':
            return pow(eval(p[1]), eval(p[2]))
        elif p[0] == '//':
            return eval(p[1])
        elif p[0] == '@':
            return eval(p[1])
    else:
        return p

while True:
    s = input('pycalc >> ')
    parser.parse(s)
