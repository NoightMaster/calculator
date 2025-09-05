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
        elif self.value.isalpha():
            self.type = "function"
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
            elif char.isdigit() or (char == '.' and self.index + 1 < len(self.expression) and self.expression[self.index+1].isdigit()):
                self.tokens.append(Token(self.read_number()))
            elif char == '(':
                self.tokens.append(Token('('))
                self.index += 1
            elif char == ')':
                self.tokens.append(Token(')'))
                self.index += 1
            elif char.isalpha():
                self.tokens.append(Token(self.read_function()))
            elif char in operation_map:
                self.tokens.append(Token(self.read_operator()))
            else:
                raise ValueError(f"Invalid character: {char}")

    def read_number(self):
        start = self.index
        while self.index < len(self.expression) and (self.expression[self.index].isdigit() or self.expression[self.index] == '.'):
            self.index += 1
        return self.expression[start:self.index]

    def read_function(self):
        start = self.index
        while self.index < len(self.expression) and self.expression[self.index].isalpha():
            self.index += 1
        string = self.expression[start:self.index]
        if string in operation_map:
            return string
        else:
            raise ValueError(f"Invalid function: {string}")

    def read_operator(self):
        start = self.index
        while self.index < len(self.expression) and self.expression[self.index] in operation_map:
            self.index += 1
        return self.expression[start:self.index]

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("peek from empty stack")

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

def ShuntingYard(expression : str):
    tokens = Tokenizer(expression).tokens
    output = []
    operator_stack = Stack()

    for token in tokens:
        if token.type == "number":
            output.append(token)
        elif token.type == "function":
            operator_stack.push(token)
        elif token.type == "operator":
            while (
                not operator_stack.is_empty()
                and operator_stack.peek().type == "operator"
                and (
                    (associativity[token.value] == 'left' and precedence[token.value] <= precedence[operator_stack.peek().value])
                    or (associativity[token.value] == 'right' and precedence[token.value] < precedence[operator_stack.peek().value])
                )
            ):
                output.append(operator_stack.pop())
            operator_stack.push(token)
        elif token.type == "leftParenthesis":
            operator_stack.push(token)
        elif token.type == "rightParenthesis":
            while not operator_stack.is_empty() and operator_stack.peek().type != "leftParenthesis":
                output.append(operator_stack.pop())
            if operator_stack.is_empty():
                raise ValueError("Mismatched parentheses")
            operator_stack.pop()
            if not operator_stack.is_empty() and operator_stack.peek().type == "function":
                output.append(operator_stack.pop())

    while not operator_stack.is_empty():
        if operator_stack.peek().type == "leftParenthesis":
            raise ValueError("Mismatched parentheses")
        output.append(operator_stack.pop())

    return output

def evaluate_rpn(rpn_tokens):
    stack = Stack()
    for token in rpn_tokens:
        if token.type == "number":
            stack.push(float(token.value))
        elif token.type == "operator" or token.type == "function":
            if token.associativity == 'binary':
                if stack.size() < 1:
                    raise ValueError("Invalid expression")
                operand = stack.pop()
                result = token.operation(operand)
                stack.push(result)
            else:
                if stack.size() < 2:
                    raise ValueError("Invalid expression")
                right = stack.pop()
                left = stack.pop()
                result = token.operation(left, right)
                stack.push(result)

    if stack.size() != 1:
        raise ValueError("Invalid expression")

    return stack.pop()
