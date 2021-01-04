import ply.lex as lex
import ply.yacc as yacc

# tokens def

tokens = ['INT', 'FLOAT', 'NAME', 'PLUS', 'MINUS', 'DIVIDE', 'MULTIPLY']

t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_MULTIPLY = r'\*'
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

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t

def t_error(t):
    print("Bad characters!\n")
    t.lexer.skip(1)

# operation priority

precedence = (('left', 'PLUS', 'MINUS'), ('left', 'MULTIPLY', 'DIVIDE'))

def p_calc(p):
    '''
    calc : expression
         | empty
    '''
    print(eval(p[1]))

def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0] = p[1]

def p_expression_var(p):
    '''
    expression : NAME
    '''
    p[0] = ('var', p[1])

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
            return eval(p[1]) + eval(p[2])
        elif p[0] == '*':
            return eval(p[1]) * eval(p[2])
        elif p[0] == '/':
            return eval(p[1]) / eval(p[2])
    else:
        return p

while True:
    s = input('-> ')
    parser.parse(s)