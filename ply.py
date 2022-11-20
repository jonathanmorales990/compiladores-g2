from ply.lex import lex
from ply.yacc import yacc
from yaml import dump

tokens = (
    'TO',
    'ID',
    'NUMBER',
    'END',
    'COLON',
    'IF',
    'THEN',
    'ELSE',
    'WHILE',
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "LPAREN",
    "RPAREN"
)

reserveds = {
   'IF': 'IF',
   'THEN': 'THEN',
   'ELSE': 'ELSE',
   'END': 'END',
   'WHILE': 'WHILE',
   'NOT': 'NOT',
   'TO': 'TO',
   'AND': 'AND',
   'OR': 'OR',
   'SET': 'SET',
}

t_ignore = ' \t'

t_COLON = r':'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserveds.get(t.value.upper(), 'ID')
    return t

def t_ignore_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print(f'Illegal character {t.value[0]!r}')
    t.lexer.skip(1)

lexer = lex()


def p_program(p):
    """program : statements"""
    p[0] = new_node('Program', p[1])


def p_statements(p):
    """statements : statement statements
                      |
    """
    if len(p) > 2:
        if p[2] is None:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]]
            p[0].extend(p[2])


def p_statement(p):
    """statement : declare_func
                 | call_func
                 | if
                 | if_else
                 | while
                 | expression
    """
    p[0] = new_leaf('Statement', p[1])

def p_call_func(p):
    """call_func : ID func_params"""
    p[0] = new_leaf('Call function', p[1], p[2])

def p_declare_func(p):
    'declare_func : TO ID func_params statements END'
    # p[0] = ('declare function', p[1], p[2], p[3], p[4])
    p[0] = new_leaf('Declare function', p[1], p[2], p[3], p[4])
def p_number(p):
    'number : NUMBER'
    p[0] = ('number', p[1])

def p_id(p):
    'id : ID'
    p[0] = ('Identifier', p[1])

def p_func_params(p):
    """func_params :
                    | func_param func_params
    """
    if len(p) > 2:
        if p[2] is None:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]]
            p[0].extend(p[2])
def p_func_param(p):
    """func_param : COLON id
                  | number
    """
    if len(p) > 2:
        p[0] = ('Parameter', p[2])
    else:
        p[0] = ('Parameter', p[1])


def p_error(p):
    print(f'Syntax error at {p.value!r}')

def new_node(name, *children):
     return {"name":name, "children": children}

def new_leaf(name, *value):
    return {"name": name, "value": value}

def p_if(p):
    """if : IF ID THEN statements END"""
    p[0] = new_leaf("IF", p[2], p[4])

def p_if_else(p):
    """if_else : IF ID THEN statements ELSE statements END"""
    p[0] = new_leaf("IF ELSE", p[2], p[4], p[6])


def p_while(p):
    """while : WHILE ID statements END"""
    p[0] = new_leaf("WHILE", p[2], p[3])

def p_factor_unary(p):
    '''
    factor : PLUS factor
           | MINUS factor
    '''
    p[0] = new_leaf('MATH EXPRESSION', p[1], p[2])

def p_factor_grouped(p):
    '''
    factor : LPAREN expression RPAREN
    '''
    p[0] = new_leaf('MATH EXPRESSION', p[2])

def p_expression(p):
    '''
    expression : term PLUS term
               | term MINUS term
    '''
    p[0] = new_leaf('MATH EXPRESSION', p[2], p[1], p[3])

def p_expression_term(p):
    '''
    expression : term
    '''
    p[0] = p[1]

def p_term(p):
    '''
    term : factor TIMES factor
         | factor DIVIDE factor
    '''
    p[0] = new_leaf('MATH EXPRESSION', p[2], p[1], p[3])

def p_term_factor(p):
    '''
    term : factor
    '''
    p[0] = p[1]

def p_factor_number(p):
    '''
    factor : NUMBER
    '''
    p[0] = new_leaf('Number', p[1])

parser = yacc()

expression = """
    TO SQUARE :length
        FORWARD :length
        RIGHT 90
    END

    SETXY 20 20
    SQUARE 30

    IF TESTE THEN SQUARE 30 END
    1 + 1
"""
expression_result = parser.parse(expression)
print(expression_result)
print(dump(expression_result, sort_keys=False, indent=2))
