import math

operation_map = {
    '+': lambda x, y: x + y,
    '-': lambda x, y: x - y,
    '*': lambda x, y: x * y,
    '/': lambda x, y: x / y if y != 0 else "Division by zero",
    '%': lambda x, y: x%y,
    '**' : lambda x,y: x**y,
    'abs' : lambda x: abs(x),
    'sin' : lambda x: math.sin(x),
    'cos' : lambda x: math.cos(x),
    'tan' : lambda x: math.tan(x),
    'cosec' : lambda x: 1/math.sin(x),
    'sec' : lambda x: 1/math.cos(x),
    'cot' : lambda x: 1/math.tan(x),
    'arcsin' : lambda x: math.asin(x),
    'arccos' : lambda x: math.acos(x),
    'arctan' : lambda x: math.atan(x),
    'arccosec' : lambda x: math.asin(1/x),
    'arcsec' : lambda x: math.acos(1/x),
    'arccot' : lambda x: math.atan(1/x),
}
precedence = {
    '**': 3,
    '*': 2,
    '/': 2,
    '%': 2,
    '+': 1,
    '-': 1,
    'abs': 4,
    'sin': 4,
    'cos': 4,
    'tan': 4,
    'cosec': 4,
    'sec': 4,
    'cot': 4,
    'arcsin': 4,
    'arccos': 4,
    'arctan': 4,
    'arccosec': 4,
    'arcsec': 4,
    'arccot': 4,
}
associativity = {
    '+': 'left',
    '-': 'left',
    '*': 'left',
    '/': 'left',
    '%': 'left',
    '**': 'right',
    'abs': 'binary',
    'sin': 'binary',
    'cos': 'binary',
    'tan': 'binary',
    'cosec': 'binary',
    'sec': 'binary',
    'cot': 'binary',
    'arcsin': 'binary',
    'arccos': 'binary',
    'arctan': 'binary',
    'arccosec': 'binary',
    'arcsec': 'binary',
    'arccot': 'binary',
}
class Token:
    def __init__(self, value : str):
        self.value = value
        self.type = None
        self.operation = None
        self.associativity = None
        self.precedence = None
        self.assign()
    def assign(self):
        if self.value == "(":
            self.type = "leftParenthesis"
        elif self.value == ")":
            self.type = "rightParenthesis"
        elif self.value in operation_map:
            self.type = "operator"
            self.operation = operation_map[self.value]
            self.associativity = associativity[self.value]
            self.precedence = precedence[self.value]
        else:
            self.type = "number"

class Tokenizer:
    def __init__(self, expression : str):
        self.expression = expression
        self.tokens = []
        self.index = 0
        self.tokenize()

    def tokenize(self):
        while self.index < len(self.expression):
            char = self.expression[self.index]
            if char.isspace():
                self.index += 1
            elif char.isdigit():
                self.tokens.append(Token(self.read_number()))
            elif char == '(':
                self.tokens.append(Token('('))
            elif char == ')':
                self.tokens.append(Token(')'))
            elif char.isalpha():
                self.functionValidatorThingy()
            else:
                raise ValueError(f"Invalid character: {char}")

    def read_number(self):
        start = self.index
        while self.index < len(self.expression) and self.expression[self.index].isdigit():
            self.index += 1
        return self.expression[start:self.index]

    def functionValidatorThingy(self):
        string = ""
        while self.index < len(self.expression) and self.expression[self.index].isalpha():
            self.index += 1
            string += self.expression[self.index]
        if string in operation_map:
            self.tokens.append(Token(string))
        else:
            raise ValueError(f"Invalid function: {string}")
