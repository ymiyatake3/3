# Move the focused character or token one step forward
def lookNext(index):
    return index + 1

# Make a number token
def numToToken(number):
    token = {'type': 'NUMBER', 'number': number}
    return token

# Make an other token
def typeToToken(type):
    token = {'type': type}
    return token



# Define the token of each input characters
#-----------------------------

def readNumber(line, index):
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
    token = typeToToken('PLUS')
    return token, lookNext(index)

def readMinus(line, index):
    token = typeToToken('MINUS')
    return token, lookNext(index)

def readTimes(line, index):
    token = typeToToken('TIMES')
    return token, lookNext(index)

def readDivide(line, index):
    token = typeToToken('DIVIDE')
    return token, lookNext(index)

def readLeftBracket(line, index):
    token = typeToToken('LEFT')
    return token, lookNext(index)

def readRightBracket(line, index):
    token = typeToToken('RIGHT')
    return token, lookNext(index)

#-----------------------------

def isOperator(token):
    type = getType(token)
    if type == 'NUMBER' or type == 'LEFT' or type == 'RIGHT':
        return False
    else:
        return True

# Check if there is strange character
def checkErrorInput(line):
    
    # If there is character that is not a number and not a correct operator
    acceptedChars = ['+', '-', '*', '/', '.', '(', ')']
    errors = []
    for c in line:
        if (not c.isdigit()) and (c not in acceptedChars):
            errors.append(c)
    if errors:
        print('Input Error: Invalid character found -> ' + ''.join(errors))
        return True


    # If there are successive dots
    if '..' in line:
        print('Input Error: Invalid number.')
        return True

    # line starts with . or the character before . is not a number (ex: .123, 1+.1)
    if line[0] == '.' or ('.' in line and not line[line.index('.') - 1].isdigit()):
        print('Input Error: Invalid number.')
        return True
    
    return False

def lastIndex(list, element):
    len(list) - 1 - tokens[::1].index(element)


# Check if the tokens are in correct order (number and operator take turns)
def checkTokenOrder(tokens):
    
    # If the first token is '-'
    if getType(tokens[0]) == 'MINUS':
        # Insert 0 befere the '-'
        tokens.insert(0, numToToken(0))
    
    # If the input is only a number
    if len(tokens) == 1 and getType(tokens[0]) == 'NUMBER':
        # Insert +0 after the number
        tokens.append(typeToToken('PLUS'))
        tokens.append(numToToken(0))
    
    # Check the order
    index = 0
    while index < len(tokens) - 1:
        if isOperator(tokens[index]) == isOperator(tokens[index + 1]):
            print('Input Error: There are operators next to each other.')
            return True
        
        index = lookNext(index)
    
    # If the last token is operator
    if isOperator(tokens[len(tokens) - 1]):
        print('Input Error: This formula ends with operator.')
        return True

    leftBracket = typeToToken('LEFT')
    rightBracket = typeToToken('RIGHT')

    # If the number of '(' and ')' are not same
    if not tokens.count(typeToToken('LEFT')) == tokens.count(typeToToken('RIGHT')):
        print('Input Error: There is a missing curly bracket')
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

    return False


def getType(token):
    return token['type']

def getNumber(token):
    return token['number']



# Look each character and separate to tokens
def tokenize(line):
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

# Do calculation of the operations in argument 'operations'
def calculate(formula, operations):
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


def calculate1(formula):
    # Multiplication and division
    formula = calculate(formula, ['TIMES', 'DIVIDE'])
    
    # Addition and subtraction
    formula = calculate(formula, ['PLUS', 'MINUS'])

    # Finally remained value is the answer
    answer = getNumber(formula[0])

    return answer


# Get an answer from the list of tokens
def evaluate(tokens):
    answer = 0
    
    while typeToToken('LEFT') in tokens:
        lastLeftIndex = lastIndex(tokens, typeToToken('LEFT'))
        index = lastLeftIndex + 1
        while not getType(tokens(index)) == 'RIGHT':
            index = lookNext(index)
            
            # Calculate inside of the brackets
            result = calculate1(tokens[lastLeftIndex + 1 : index])
            
            # Delete from ( to )
            del tokens[lastLeftIndex : index + 1]
            
            tokens.insert(lastLeftIndex, result)
    
    answer = calculate1(tokens)

    return answer


# Return if the calculated answer is true or false
def test(line):
    if len(line) == 0:
        print('Please input some value.')
        return
    if checkErrorInput(line):
        return
    tokens = tokenize(line)
    if checkTokenOrder(tokens):
        return
    actualAnswer = evaluate(tokens)
    expectedAnswer = eval(line)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
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
    test("(1+1)")           # simple ()
    test("2*(1+1)")         # calculation order change
    test("2*(1+1)/2")       # calculation after ()
    test("1+(1+(1+1))")     # () in ()
    test("2*(1+1)*(1+1)")   # () after ()
    
  
    # error inputs
    test("")              # blank
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
  
    print("==== Test finished! ====\n")




runTest()

while True:
    print('> ', end="")
    line = input()
    if len(line) == 0:
        print('Please input some value.')
        continue
    if checkErrorInput(line):
        continue
    tokens = tokenize(line)
    if checkTokenOrder(tokens):
        continue
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)
