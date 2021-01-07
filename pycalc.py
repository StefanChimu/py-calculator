import ply.lex as lex
import ply.yacc as yacc
import math

def make_input_friendly(s):
    s = s.replace("rad", "//")
    s = s.replace("^^", "^")
    s = s.replace("log", "!")
    s = s.replace("sin", "@")
    s = s.replace("cos", "#")
    s = s.replace("ctg", "&")
    s = s.replace("tg", "$")
    return s

def tilda(a,b):
    return (a/b) - 1

# tokens def

tokens = ['INT', 'FLOAT', 'PLUS', 'MINUS', 'DIVIDE', 'MULTIPLY', 'POW', 'SQRT',
          'LPAREN', 'RPAREN', 'COMMA', 'LOG',
          'SIN', 'COS', 'TG', 'CTG', 'NEWOP']

# basic operations

t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_MULTIPLY = r'\*'
t_POW = r'\^'
t_SQRT = r'\//'
t_NEWOP = r'\~'

# parantheses

t_LPAREN  = r'\('
t_RPAREN  = r'\)'

# separator used for log: log(x, y)

t_COMMA = r'\,'
t_LOG = r'\!'

# trigon. funcs

t_SIN = r'\@'
t_COS = r'\#'
t_TG = r'\$'
t_CTG = r'\&'

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
              ('left', 'POW', 'MULTIPLY', 'DIVIDE', 'NEWOP'),
              ('right', 'FUNC'),
              ('right', 'UMINUS'))

def p_calc(p):
    '''
    calc : expression
         | empty
    '''
    print(eval(p[1]))

def p_expression_func(p):
    '''
     expression : SQRT expression %prec FUNC
                | LOG expression %prec FUNC
                | SIN expression %prec FUNC
                | COS expression %prec FUNC
                | TG expression %prec FUNC
                | CTG expression %prec FUNC
    '''
    if p[1] == '//': # rad
        p[0] = math.sqrt(p[2])
    elif p[1] == '!': # log
        p[0] = math.log(p[2][1], p[2][2])
    elif p[1] == '@': # sin
        p[0] = math.sin(p[2])
    elif p[1] == '#': # cos
        p[0] = math.cos(p[2])
    elif p[1] == '$': # tg
        p[0] = math.tan(p[2])
    elif p[1] == '&': # ctg:
        p[0] = 1 / math.tan(p[2])

def p_binop(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression POW expression
               | expression PLUS expression
               | expression MINUS expression
               | expression COMMA expression
               | expression NEWOP expression
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
        elif p[0] == '~':
            return tilda(p[1], p[2])
        elif p[0] == '//' or p[0] == '!' or p[0] == '@'\
                or p[0] == '#' or p[0] == '$' or p[0] == '&':
            return eval(p[1])
    else:
        return p

while True:
    s = input('pycalc >> ')
    if s == "exit":
        break
    s = make_input_friendly(s)
    parser.parse(s)