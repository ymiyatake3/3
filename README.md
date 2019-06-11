# 3

### How to use

- Please input "calculator.py" in Terminal.
- Tests will be executed first.
- After the tests end, you can input your formula.


### About modularization
- Made some methods like
  - getType(token), getNumber(token)
  - calculate(operator, num1, num2)
  - checkErrorInput(line)
  - checkTokenOrder(tokens)
  - isOperator(token)
  - lookNext(index)
  - makeNumToken(number), makeToken(type)
  etc.
 
- In calculation, I tried to dynamically change the tokens array.
For example, 

  __[1, +, 2, *, 3]__ →
  
  **[1, +, 6]** →
  
  **[7]** 
  
  because it was good to implement multiplication and division.
  
- To implement the dynamic tokens change shown above,
I made some changes to tokens.

  - If the input is only number, change **1** to **1 + 0**
  - If the input is negative number, change **-1** to **0 - 1**
  
  because of them, the number and operator must appear each other,
  that is, every calculation can be done in the manner of **(number) (operator) (number)**.
  And error handling becomes easy.
