# Move the focused character or token one step forward
def lookNext(index):
    return index + 1

def setNumToken(number):
    token = {'type': 'NUMBER', 'number': number}
    return token

def setToken(type):
    token = {'type': type}
    return token


# Define the token of each input characters
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

    # Set the token type in the token dictionary
    token = setNumToken(number)
    return token, index

def readPlus(line, index):
    token = setToken('PLUS')
    return token, lookNext(index)

def readMinus(line, index):
    token = setToken('MINUS')
    return token, lookNext(index)

def readTimes(line, index):
    token = setToken('TIMES')
    return token, lookNext(index)

def readDivide(line, index):
    token = setToken('DIVIDE')
    return token, lookNext(index)


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
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)

    #print(tokens)
    return tokens


def canCalculate(tokens, index):
    operator = tokens[index - 1]['type']
    
    if (len(tokens) > index + 1):
        if (operator == 'PLUS' || operator == 'MINUS'):
            # If the next token is number
            if (tokens[index + 1]['type'] == 'NUMBER'):
                return True
        elif(operator == 'TIMES' || operator == 'DIVIDE')
            # If both of the side tokens are number
            if (tokens[index - 1]['type'] == 'NUMBER' && tokens[index + 1]['type'] == 'NUMBER'):
                return True
    
    return False


def calculate(operator, num1, num2):
    result = 0
    
    if (operator == 'PLUS') {
        result = num1 + num2
    } elif (operator == 'MINUS') {
        result = num1 - num2
    } elif (operator == 'TIMES') {
        result = num1 * num2
    } elif (operator == 'DIVID') {
        result = num1 / num2
    }

    return result

def getType(tokens, index):
    return tokens[index]['type']

def getNumber(tokens, number):
    return tokens[index]['number']


# Calculation
def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    
    # Multiplication and division
    index = 1
    while index < len(tokens):
        type = getType(tokens, index)
        if (type == 'TIMES' || type == 'DIVIDE') && canCalculate(tokens, index):
            # Calculate
            result = calculate(type, getNumber(tokens, index - 1), getNumber(tokens, index + 1))
            
            # Delete the calculated part (ex: 2, *, 3)
            del tokens[index - 1 : index + 1]
                
            # Insert the result instead (ex: 6)
            tokens.insert(index - 1, setNumToken(result))
        else:
            index = lookNext(index)

    # Addition and subtraction
    index = 1
    while index < len(tokens):
        type = getType(tokens, index)
        if (type == 'PLUS' || type == 'MINUS') && canCalculate(tokens, index):
            ans += calculate(type, getNumber(tokens, index - 1), getNumber(tokens, index + 1))

        index = lookNext(index)

    return answer


# Return if the calculated answer is true or false
def test(line):
  tokens = tokenize(line)
  actualAnswer = evaluate(tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  test("1+2")
  test("1.0+2.1-3")
  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)
