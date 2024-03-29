# Original code:
# https://github.com/xharaken/step2015/blob/master/calculator_modularize_2.py


def lookNext(index):
    """Move the focused character or token one step forward.
    
    Args:
        index: Current index
    Returns:
        Next index
    """
    return index + 1

def numToToken(number):
    """Make a number token

    Args:
        number: A number put into 'number'
    Returns:
        Token of number
    """
    token = {'type': 'NUMBER', 'number': number}
    return token


def typeToToken(type):
    """Make a token with a specified type
        
    Args:
        type: Type of the token
    Returns:
        Token of a operator or a bracket
    """
    token = {'type': type}
    return token





def readNumber(line, index):
    """Make successive numbers (include decimal point) a token
        
    Args:
        line: Char array of user's input
        index: Index of the first number
    Returns:
        token: Created token
        index: Index of the line to see next
    """
    
    number = 0
    
    # While the focused character is a number
    while index < len(line) and line[index].isdigit():
        # 桁を上げる
        number = number * 10 + int(line[index])
        index = lookNext(index)
    
    # If the number has a value after decimal point
    if index < len(line) and line[index] == '.':
        index = lookNext(index)
        keta = 0.1
        # While the focused character is a number
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta /= 10
            index = lookNext(index)

    # Set the token type
    token = numToToken(number)
    return token, index

def readPlus(line, index):
    """Make '+' a token with type 'PLUS'
        
    Args:
        line: Char array of user's input
        index: Index of the first number
    Returns:
        token: Created token
        index: Index of the line to see next
    """
    token = typeToToken('PLUS')
    return token, lookNext(index)

def readMinus(line, index):
    """Make '-' a token with type 'MINUS'
        
    Args:
        line: Char array of user's input
        index: Index of the first number
    Returns:
        token: Created token
        index: Index of the line to see next
    """
    token = typeToToken('MINUS')
    return token, lookNext(index)

def readTimes(line, index):
    """Make '*' a token with type 'TIMES'
        
    Args:
        line: Char array of user's input
        index: Index of the first number
    Returns:
        token: Created token
        index: Index of the line to see next
    """
    token = typeToToken('TIMES')
    return token, lookNext(index)

def readDivide(line, index):
    """Make '/' a token with type 'DIVIDE'
        
    Args:
        line: Char array of user's input
        index: Index of the first number
    Returns:
        token: Created token
        index: Index of the line to see next
    """
    token = typeToToken('DIVIDE')
    return token, lookNext(index)

def readLeftBracket(line, index):
    """Make '(' a token with type 'LEFT'
        
    Args:
        line: Char array of user's input
        index: Index of the first number
    Returns:
        token: Created token
        index: Index of the line to see next
    """
    token = typeToToken('LEFT')
    return token, lookNext(index)

def readRightBracket(line, index):
    """Make ')' a token with type 'RIGHT'
        
    Args:
        line: Char array of user's input
        index: Index of the first number
    Returns:
        token: Created token
        index: Index of the line to see next
    """
    token = typeToToken('RIGHT')
    return token, lookNext(index)






def isOperator(token):
    """Detect if a token is a operator or not
        
    Args:
        token: Token to detect
    Returns:
        True or False
    """
    type = getType(token)
    if type == 'NUMBER' or type == 'LEFT' or type == 'RIGHT':
        return False
    else:
        return True


def lastIndex(l, element):
    """Return the last index that the element appear
        
    Args:
        l: List to seek in
        element: Element to seek
    Returns:
        Last index
    """
    return len(l) - 1 - l[::-1].index(element)


def checkCharacterError(line):
    """Detect errors before tokenize
        
    Args:
        line: Char array of user's input
    Returns:
        If any error was detected, True
        If there is no error, False
    """
    
    # If there is character that is not a number and not a correct operator
    acceptedChars = ['+', '-', '*', '/', '.', '(', ')']
    errorChars = []
    for c in line:
        if (not c.isdigit()) and (c not in acceptedChars):
            errorChars.append(c)
    if errorChars:
        print('Input Error: Invalid character found -> ' + ''.join(errorChars))
        return True


    # If there are successive dots
    if '..' in line:
        print('Input Error: Invalid number.')
        return True

    # line starts with . or the character before . is not a number (ex: .123, 1+.1)
    if line[0] == '.' or ('.' in line and not line[line.index('.') - 1].isdigit()):
        print('Input Error: Invalid number.')
        return True

    # If there is '()'
    if '()' in line:
        print('Input Error: No value in brackets.')
        return True
    
    return False


def checkTokenError(tokens):
    """Detect errors after tokenize
        
    Args:
        tokens: Array of token objects
    Returns:
        If any error was detected, True
        If there is no error, False
    """
    
    leftBracket = typeToToken('LEFT')
    rightBracket = typeToToken('RIGHT')
    
    ## Errors of bracket places

    # If the number of '(' and ')' are not same
    if not tokens.count(typeToToken('LEFT')) == tokens.count(typeToToken('RIGHT')):
        print('Input Error: There is a missing curly bracket.')
        return True

    # If there is ')' before '('
    if leftBracket in tokens and rightBracket in tokens:
        firstLeftIndex = tokens.index(leftBracket)
        firstRightIndex = tokens.index(rightBracket)
        lastLeftIndex = lastIndex(tokens, leftBracket)
        lastRightIndex = lastIndex(tokens, rightBracket)
        
        if not (firstLeftIndex < firstRightIndex and lastLeftIndex < lastRightIndex):
            print('Input Error: Strange order of curly brackets.')
            return True




    ## Errors of operators

    # If the first token is '-', insert 0 on the top.
    if getType(tokens[0]) == 'MINUS':
        tokens.insert(0, numToToken(0))
        
    # If the input is only a number, insert +0 at last.
    if len(tokens) == 1 and getType(tokens[0]) == 'NUMBER':
        tokens.append(typeToToken('PLUS'))
        tokens.append(numToToken(0))
    
    # Delete ()
    tokensCopy = tokens.copy()
    index = 0
    while index < len(tokensCopy):
        token = tokensCopy[index]
        if token == leftBracket or token == rightBracket:
            del tokensCopy[index]
        else:
            index = lookNext(index)


    # Check the order
    index = 0
    while index < len(tokensCopy) - 1:
        if isOperator(tokensCopy[index]) == isOperator(tokensCopy[index + 1]):
            print('Input Error: There are operators next to each other.')
            return True
            
        index = lookNext(index)

    # If the last token is operator
    if isOperator(tokensCopy[len(tokensCopy) - 1]):
        print('Input Error: This formula ends with operator.')
        return True


    return False





def getType(token):
    """Return type of the token
        
    Args:
        token: A token of any type
    Returns:
        Token's type
    """
    return token['type']


def getNumber(token):
    """Return number of the NUMBER token
        
    Args:
        token: A token of number
    Returns:
        Token's number
    """
    
    return token['number']




def tokenize(line):
    """Separate the input array into tokens
        
    Args:
        line: Char array of user's input
    Returns:
        Array of token objects
    """
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readTimes(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        elif line[index] == '(':
            (token, index) = readLeftBracket(line, index)
        elif line[index] == ')':
            (token, index) = readRightBracket(line, index)
        
        tokens.append(token)

    return tokens


def binaryOperation(operator, num1, num2):
    """Do binary operation and returns the result
        
    Args:
        operator: Operator token
        num1: 1st operand
        num2: 2nd operand
    Returns:
        The result of calculation (as a number)
    """
    result = 0
    
    if operator == 'PLUS':
        result = num1 + num2
    elif operator == 'MINUS':
        result = num1 - num2
    elif operator == 'TIMES':
        result = num1 * num2
    elif operator == 'DIVIDE':
        result = num1 / num2
    
    return result


def evaluateSpecifiedOperation(formula, operations):
    """Do calculation of the specified operations
        
    Args:
        formula: Array of token objects
        operations: Array of operators to calculate
    Returns:
        The result of calculation (as a token array)
    """
    index = 0
    while index < len(formula):
        type = getType(formula[index])
        if type in operations:
            # Calculate
            result = binaryOperation(type, getNumber(formula[index - 1]), getNumber(formula[index + 1]))
            
            # Delete the calculated part (ex: 2, *, 3)
            del formula[index - 1 : index + 2]
                
            # Insert the result instead (ex: 6)
            formula.insert(index - 1, numToToken(result))
        else:
            index = lookNext(index)

    return formula


def evaluateInTwoStage(formula):
    """Do multiplication and division first, addition and subtraction second
        
    Args:
        formula: Array of token objects
    Returns:
        The result of calculation (as a token array)
    """
    
    # * and /
    formula = evaluateSpecifiedOperation(formula, ['TIMES', 'DIVIDE'])
    
    # + and -
    formula = evaluateSpecifiedOperation(formula, ['PLUS', 'MINUS'])

    return formula


# Get an answer from the list of tokens
def evaluate(tokens):
    """Evaluates the expression represented by tokens and returns a final number
        
    Args:
        token: Array of token objects
    Returns:
        A single number after processing all tokens
    """

    answer = 0

    # Inside of the brackets
    while typeToToken('LEFT') in tokens:
        lastLeftIndex = lastIndex(tokens, typeToToken('LEFT'))
        index = lastLeftIndex + 1
        while not getType(tokens[index]) == 'RIGHT':
            index = lookNext(index)
            
        # Calculate inside of the brackets
        result = evaluateInTwoStage(tokens[lastLeftIndex + 1 : index])

        # Delete from '(' to ')'
        del tokens[lastLeftIndex : index + 1]
        
        # Insert result token instead
        tokens[lastLeftIndex:lastLeftIndex] = result
    
    # Calculate with no brackets
    tokens = evaluateInTwoStage(tokens)
    
    # Finally remained is answer
    return getNumber(tokens[0])


def test(line):
    """Evaluate the input expression and check if the answer is right
        
    Args:
        line: Char array of user's input
    Returns:
        None (Print the result)
    """
    if len(line) == 0:
        print('Please input some value.')
        return
    if checkCharacterError(line):
        return
    tokens = tokenize(line)
    if checkTokenError(tokens):
        return
    actualAnswer = evaluate(tokens)
    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
    """Execute tests
        
    Args:
        None
    Returns:
        None
    """
    
    print("==== Test started! ====")
  
    test("1")         # only number
    test("12345678")  # number with more than 2 character
  
    test("1+2")   # +
    test("3-1")   # -
    test("1-3")   # answer is negative number
    test("2*2")   # *
    test("4/2")   # /
      
    test("1+2+3")     # +, +
    test("10-2-1")    # -, -
    test("2*2*2")     # *, *
    test("8/2/2")     # /, /
    
    test("1+2*3")         # +, *
    test("1-2*3")         # -, *
    test("1+2*3-1")       # +, -, *
    test("1+4/2")         # +, /
    test("1-4/2")         # -, /
    test("1+4/2-1")       # +, -, /
    test("3*4/2")         # *, /
    test("1+3*4/2")       # +, *, /
    test("1-3*4/2")       # -, *, /
    test("1+3*4/2-1")     # +, -, *, /
  
    # with decimal
    test("1.2")         # only number
    test("1.234")       # decimal part has more than 2 characters
    test("123.456")     # integer part has more than 2 characters
    test("1.2+1.1")     # more than 2 decimal numbers
    test("1.5+1")       # decimal number & integer
    
    # with brackets
    test("(1)")             # simple ()
    test("(1+1)")
    test("2*(1+1)")         # calculation order change
    test("2*(1+1)/2")       # calculation after ()
    test("1+(1+(1+1))")     # nest
    test("2*(1+1)*(1+1)")   # () after ()
    
  
    # error inputs
    test("")               # blank
    #test("10000000000")   # too big
    test("+")             # only operator
    test("*")
    test("1++1")
    test("1*+1")
    test("1*/1")
    test("1..1")
    test(".1")
    test("a")
    test("32+a+b+c")
    test("()")              # Only bracket
    test("(1+1))")          # The numbers of left and right brackets are different
    test(")1+1(")           # Numbers are same but not starts with (
    test("(1+1))(")         # Start with ( but not end with )
  
    print("==== Test finished! ====\n")




runTest()

while True:
    print('> ', end="")
    line = input()
    if len(line) == 0:
        print('Please input some value.')
        continue
    if checkCharacterError(line):
        continue
    tokens = tokenize(line)
    if checkTokenError(tokens):
        continue
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
