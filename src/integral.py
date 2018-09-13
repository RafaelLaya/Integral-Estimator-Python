from py_expression_eval import Parser
import random
import math

"""
 Estimates the integral of function over the interval (a, b) using an specified number of rectangles and Simpson's Method
    Args:
        function: A py_expression expression 
        a: A float number that represents the left bound of integration
        b: A float number that represents the right bound of integration
        rectangles: A positive integer that represents the number of subintervals considered in the estimation of the integral.

    Returns:
        The estimation of the integral
    
    Notes:
        Assumes the function provided is supported and continous in (a, b)
        Simpson's method will return the weighted average that corresponds to simpson's method when rectangles is odd (simpson's method is usually defined for an even number rectangles by the way it is derived)
"""
def simpson(function, a, b, rectangles):

  if a == b:
    return 0

  delta_x = (b - a) / rectangles
  if delta_x < 0:
    return -simpson(function, b, a, rectangles)
  return (2 * midpoint(function, a, b, rectangles) + trapezium(function, a, b, rectangles)) / 3

"""
 Estimates the integral of function over the interval (a, b) using an specified number of rectangles and Left Riemann Sums
    Args:
        function: A py_expression expression 
        a: A float number that represents the left bound of integration
        b: A float number that represents the right bound of integration
        rectangles: A positive integer that represents the number of subintervals considered in the estimation of the integral.

    Returns:
        The estimation of the integral
    Notes:
        Assumes the function provided is supported and continous in (a, b)
"""
def left(function, a, b, rectangles):

  if a == b:
    return 0

  delta_x = (b - a) / rectangles

  if delta_x < 0:
    return -left(function, b, a, rectangles)

  total = 0
  for i in range(0, rectangles):
    total += function.evaluate({'x' : a + i * delta_x})
  total *= delta_x

  return total

"""
 Estimates the integral of function over the interval (a, b) using an specified number of rectangles and Right Riemann Sums
    Args:
        function: A py_expression expression 
        a: A float number that represents the left bound of integration
        b: A float number that represents the right bound of integration
        rectangles: A positive integer that represents the number of subintervals considered in the estimation of the integral.

    Returns:
        The estimation of the integral
    Notes:
        Assumes the function provided is supported and continous in (a, b)
"""
def right(function, a, b, rectangles):
  if a == b:
    return 0
  delta_x = (b - a) / rectangles

  if delta_x < 0:
    return -right(function, b, a, rectangles)

  return left(function, a + delta_x, b + delta_x, rectangles)

"""
 Estimates the integral of function over the interval (a, b) using an specified number of rectangles and the midpoint rule
    Args:
        function: A py_expression expression 
        a: A float number that represents the left bound of integration
        b: A float number that represents the right bound of integration
        rectangles: A positive integer that represents the number of subintervals considered in the estimation of the integral.

    Returns:
        The estimation of the integral
    Notes:
        Assumes the function provided is supported and continous in (a, b)
"""
def midpoint(function, a, b, rectangles):
  if a == b:
    return 0
  
  delta_x = (b - a) / rectangles
  if delta_x < 0:
    return -midpoint(function, b, a, rectangles)
  return left(function, a + (delta_x / 2), b + (delta_x) / 2, rectangles)

"""
 Estimates the integral of function over the interval (a, b) using an specified number of rectangles and the trapezium rule
    Args:
        function: A py_expression expression 
        a: A float number that represents the left bound of integration
        b: A float number that represents the right bound of integration
        rectangles: A positive integer that represents the number of subintervals considered in the estimation of the integral.

    Returns:
        The estimation of the integral
    Notes:
        Assumes the function provided is supported and continous in (a, b)
"""
def trapezium(function, a, b, rectangles):
  if a == b:
    return 0
  
  delta_x = (b - a) / rectangles
  if delta_x < 0:
    return -trapezium(function, b, a, rectangles)
  return (left(function, a, b, rectangles) + right(function, a, b, rectangles)) / 2

"""
 Estimates the integral of function over the interval (a, b) using an specified number of rectangles and left riemann sums, right riemann sums, trapezium rule, simpson's rule and midpoint rule by taking their average
    Args:
        function: A py_expression expression 
        a: A float number that represents the left bound of integration
        b: A float number that represents the right bound of integration
        rectangles: A positive integer that represents the number of subintervals considered in the estimation of the integral.

    Returns:
        The estimation of the integral
    Notes:
        Assumes the function provided is supported and continous in (a, b)
"""
def average(function, a, b, rectangles):
  if a == b:
    return 0
  return (simpson(function, a, b, rectangles) + trapezium(function, a, b, rectangles) + left(function, a, b, rectangles) + right(function, a, b, rectangles) + midpoint(function, a, b, rectangles)) / 5
  
"""
 Estimates the integral of function over the interval (a, b) using a tolerance number and the left and right riemann sums
    Args:
        function: A py_expression expression 
        lower_bound: A float number that represents the left bound of integration
        higher_bound: A float number that represents the right bound of integration
        tolerance: A float small positive number that represents the maximum desired difference between the left and right riemann sums
    Returns:
        The estimation of the integral
    Notes:
        Assumes the function provided is supported, continous and of monotone behaviour in (lower_bound, higher_bound)
        The algorithm works fine for any function but the tolerance being guaranteed by a theorem requires the function be monotone
"""
def left_right_tolerance(function, lower_bound, higher_bound, initial,epsilon):
  if lower_bound == higher_bound:
    return 0
  rectangles = initial
  right_appr = right(function, lower_bound, higher_bound, rectangles)
  left_appr = left(function, lower_bound, higher_bound, rectangles)

  while math.fabs(right_appr - left_appr) > epsilon:
    print("\nRectangles:", rectangles)
    print("Left:", left_appr)
    print("Right:", right_appr)
    print("Difference:", math.fabs(right_appr - left_appr))
    print("Average:", (right_appr + left_appr) / 2)
    print("We have not guaranteed your initial tolerance.")
    
    while True:
      try:
        answer = input("How much would you like to jump? (type 'q' for quit)> ").lower()
        
        if 'q' in answer:
          return (right_appr + left_appr) / 2
        else:
          answer = int(answer)
          if answer < 1:
             print("\nYour input should be either 'q' or a positive integer. Try again. ")
             continue
          else:
            rectangles = rectangles + int(answer)
            break
      except:
        print("\nYour input should be either 'q' or a positive integer. Try again. ")
        continue

    right_appr = right(function, lower_bound, higher_bound, rectangles)
    left_appr = left(function, lower_bound, higher_bound, rectangles)
    print()

  return (right_appr + left_appr) / 2

"""
 Estimates the integral of function over the interval (a, b) using an specified number of rectangles and a random method out of Simpson's method, Trapezium Rule, Left Riemann Sums, Right Riemann Sums, Midpoint RUle and Averaging all of these
    Args:
        function: A py_expression expression 
        a: A float number that represents the left bound of integration
        b: A float number that represents the right bound of integration
        rectangles: A positive integer that represents the number of subintervals considered in the estimation of the integral.

    Returns:
        The estimation of the integral
    Notes:
        Assumes the function provided is supported and continous in (a, b)
"""
def surprise(function, a, b, rectangles):
  method = ["Simpson's Method", "Trapezium Rule", "Left Riemann Sums", "Right Riemann Sums", "Midpoint Rule", "Averaging Simpson's, Trapezium, Left Riemann Sums, Right Riemann Sums and Midpoint Rule"]
  
  random_num = random.randint(1, 6)
  
  print("\n", method[random_num - 1] + "... ", end="")
  approx_integral(random_num, function, lower_bound, higher_bound, rectangles)

"""
 Explains the user how to input expressions into the program.
"""
def instructions():
  print(20 * "\n")
  print("This is an integral estimator program")
  print("The user can provide a function of the single variable 'x' as well as an interval of integration and the program will compute its result using the method of choosing.\n")
  print("The home menu will show a list of options from which you can choose.\n")
  print("\tAll your functions should depend only on the variable 'x'\n")
  print("\tThis program assumes your function is continous over the specified interval. Only definite proper integrals are supported. If the function does not meet one of these requirements the program will encounter either a zero division error or an unexpected result or a math domain error or infinity or similars.\n")
  print("\tCosine, Sine and Tangent functions are supported and written as cos(x), sin(x) and tan(x)\n")
  print("\tThe functions inverse tangent, inverse sine and inverse cosine are supported and can be written as arctan(x), arcsin(x) and arccos(x) or atan(x), asin(x) and acos(x).\n")
  print("\tThe function natural log is supported and can be used as ln(x) or log(x) which are equivalent\n")
  print("\tAbsolute Value is supported and written as abs(x)\n")
  print("\tThe functions ceil and floor are supported as ceil(x) and floor(x)\n")
  print("\tThe exponential function can be used as e^x, E^x or exp(x). The usage exp(x) is slightly more exact than e^x and E^x after the fourteenth decimal digit\n")
  print("\tThe numbers pi and euler's number can be written as PI, pi, E or e\n")
  print("\tThe supported operations are multiplication (*), addition (+), division (/), correct usage of parentheses (()), exponentiation (^), modulo (%), substraction (-)\n")
  print("\tThe square root function is supported as sqrt(x) or x^(1/2). Use exponents for all other roots.\n")
  print("\tFor example the integral of (five times the square of x) plus (pi times the exponential function in composition with the square root of x) can be entered as 5*x^2+pi*exp(sqrt(x)) or as 5x^2+piexp(x^(1/2)).\n")
  print("\tLazy typing (omitting the multiplication sign) is supported for all numbers, e, pi, and the functions described here. However it is my personal preference and advice for the user to write correctly\n")
  print("\tA funny little feature: x^3 can be entered as xxx, x^2 as xx and similar for other integer exponents\n")
  print("\tHave fun!\n")
  print("\tIf some input does not work correctly please email me the steps on what you did exactly to produce the output, send me screenshots and be sure that I can read the computer representation of the function that is displayed everytime you input a new function into the program")
  print("\tHave fun!")

  input("Press enter to continue.")

"""
  Very brief summary of the interpretation of an integral and suggested resources for further learning.
"""
def educate():
  print(10 * "\n")
  print("This section assumes the user is comfortable with single variable real valued functions. This program only supports proper integrals which means these functions have to be continous on the given interval\n")
  print("Suppose we have such a function called f(x).\n")
  print("Suppose also that this function is non-negative in the interval (a, b)\n")
  print("The integral from x=a to x=b of the function f(x) with respect to x is the area enclosed by the graph of the curve y=f(x) in the plane xy and between the horizontal line y=0 (the x-axis) within this interval (a, b)\n")
  print("Another interpretation is that if the integral of the velocity v(x) of a particle is the displacement of the particle from timex x=a to x=b, here x represents the time\n")
  print("Now consider the case where f(x) is negative in (a, b), then the integral is the negative of the area enclosed by the graph of the function and the x-axis.")
  print("If the function alternates sign then the function is split in intervals where it does not change sign and the integral is the sum of all these pieces\n\n")

  print("For example: The integral from x = -5 to x = 5 of f(x)=x is the integral of the same function from x=-5 to x=0 added to the integral from x=0 to x=5. The first integral is the negative of the area of the triangle of base and height five, and the second integral is the area of the same triangle with positive sign. The total integral is the addition of these numbers which have the same absolute value but different sign, therefore the integral is zero (try!).\n\n")

  print("This program is aimed to estimate integrals of continous functions using the standard numerical methods that students are usually taught in a regular calculus II class\n\n")

  print("Recommended online resources are: Khan Academy, Coursera, Edx and MIT OpenCourseWare\n")
  print("Suggested textbooks can be found in any bookstore from the authors: James Stewart, Louis Leithold, Edwards and Penney, Thomas, Apostol, Spivak")

  input("Press enter to continue")
  return

"""
 Obtains a function from the user
    Returns:
        A py_expression expression
    Notes:
        Some features were added to the original parser in this function
"""
def get_function():
  parser = Parser()

  while True:
    keywords = ["sin", "cos", "tan", "asin", "acos", "atan", "x", "log", "exp", "ceil", "floor", "abs"]
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "E", "PI", "x"]
    try:
      function = input("\nPlease, enter an expression in terms of the variable 'x' alone > ").replace(" ","").replace("arcsin", "asin").replace("arccos", "acos").replace("arctan", "atan").replace("ln", "log").replace("pi", "PI").replace("e", "E").replace("cEil", "ceil").replace("Exp", "exp").replace("xx", "x*x")

      for keyword in keywords:
        for number in numbers:
          function = function.replace(number + keyword, number + "*" + keyword)
          function = function.replace(number + '(', number + "*" + '(')

      function = parser.parse(function).simplify({})

      print("This is the computer representation of your function:", function.toString())

      if function.variables() != ['x'] and function.variables() != []:
        print("Your expression should only contain 'x' as a variable!")
        print("Your function has the following variables: ")
        for variable in function.variables():
          print(variable)
        continue
    except:
      print("\n Try again: ")
      continue

    return function.simplify({})

"""
 Obtains the integration bounds from the user
    Returns:
        Two numbers that represent the bounds of the integral
"""
def get_bounds():

  while True:
    try:
      print("\nPlease enter the bounds of the integral: ")
      a = float(input("First (Usually lower) bound a > "))
      b = float(input("Second (Usually higher) bound b > "))
      if abs(a) == float('inf') or abs(b) == float('inf'):
        print("The program does not support improper integrals yet!")
        continue
      break
    except:
      print("\n Your input should be a number. Try again")
      continue
  return a, b

"""
 Friendly goodbye to the user 
"""
def print_goodbye():
  print("Thanks for using My Integral Estimator!")
  print("See you soon for your integration needs!")

"""
 Obtains the number of rectangles by the user
    Returns:
        A positive integer that represents the number of sub-intervals that the user will want to use for the calculation of the integral
"""
def get_rectangles():
  while True:
    try:
      rectangles = int(input("\nNumber of Rectangles > "))
      
      if rectangles < 1:
        print("\nYour input should be a positive integer. Try again.")
        continue
      else:
        break

    except:
      print("\nYour input should be a positive integer. Try again.")
      continue
  return rectangles

"""
 Handles integral approximation using other functions
    Args:
        function: A py_expression expression 
        lower_bound: A float number that represents the left bound of integration
        higher_bound: A float number that represents the right bound of integration
        rectangles: A positive integer that represents the number of subintervals considered in the estimation of the integral.
    Notes:
        Assumes the function provided is supported and continous in (lower_bound, higher_bound)
        Prints the results to the screen
"""
def approx_integral(selection, function, lower_bound, higher_bound, rectangles):
  if selection == 1:
    print("\nThe result is: ", simpson(function, lower_bound, higher_bound, rectangles), "\n")
    input("Press enter to continue > ")

  elif selection == 2:
    print("\nThe result is: ", trapezium(function, lower_bound, higher_bound, rectangles), "\n")
    input("Press enter to continue > ")

  elif selection == 3:
    print("\nThe result is: ", left(function, lower_bound, higher_bound, rectangles), "\n")
    input("Press enter to continue > ")

  elif selection == 4:
    print("\nThe result is: ", right(function, lower_bound, higher_bound, rectangles), "\n")
    input("Press enter to continue > ")

  elif selection == 5:
    print("\nThe result is: ", midpoint(function, lower_bound, higher_bound, rectangles), "\n")
    input("Press enter to continue > ")

  elif selection == 6:
    print("\nThe result is: ", average(function, lower_bound, higher_bound, rectangles), "\n")
    input("Press enter to continue > ")

  elif selection == 7:
    while True:
      try:
        tolerance = float(input("What is the tolerance of this approximation? > "))
        
        if tolerance <= 0:
          print("\nYour input should be a real positive number. Try again")
        else:
          break
      except:
        print("\nYour input should be a real positive number. Try again")
        continue

    print("\nThe result is: ", left_right_tolerance(function, lower_bound, higher_bound, rectangles, tolerance), "\n")
    input("Press any key to continue > ")

########################################################################
################ ---------------- main ---------------- ################
########################################################################
print("----- Welcome to My Integral Estimator -----".center(80))

first_time = True
function = None
lower_bound = 0
higher_bound = 0

while True:
  print("\nChoose a technique for the estimation of your integral: ")

  print("1. Simpson's Rule")
  print("2. Trapezium Rule")
  print("3. Left Riemann Sums")
  print("4. Right Riemann Sums")
  print("5. Midpoint Rule")
  print("6. Average 1-5")
  print("7. Left and Right Riemann Sums with Tolerance (Works well for any function but in order to guarantee tolerance the function provided must have monotone behaviour)")
  print("8. Surprise me!")
  print("9. Instructions and Examples")
  print("10. Educate me")
  print("11. Another Function")
  print("12. New Bounds")
  print("13. Change Number of Rectangles to use")
  print("14. Quit")

  print()

  try:
    selection = int(input("Selection > "))
  except:
    continue

  if selection == 9:
    instructions()
    continue
  elif selection == 10:
    educate()
    continue

  if first_time:
    first_time = False
    if selection == 14:
      print_goodbye()
      break
    function = get_function()
    lower_bound, higher_bound = get_bounds()
    rectangles = get_rectangles() 
    if selection == 11 or selection == 12 or selection == 13:
      continue

  if selection in [1, 2, 3, 4, 5, 6, 7]:
    approx_integral(selection, function, lower_bound, higher_bound, rectangles)

  elif selection == 8:
    surprise(function, lower_bound, higher_bound, rectangles)

  elif selection == 9:
    instructions()

  elif selection == 10:
    educate()

  elif selection == 11:
    function = get_function()

  elif selection == 12:
    lower_bound, higher_bound = get_bounds()

  elif selection == 13:
    rectangles = get_rectangles()

  elif selection == 14:
    print_goodbye()
    break