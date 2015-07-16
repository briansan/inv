"""
  @file   inv/view/cli/common.py
  @author Brian Kim
  @brief  a script containing the methods necessary
          to design a robust command-line interface
"""

import sys
import signal

def read_int(prompt):
  try:
    y_str=raw_input(prompt)
    y=int(y_str)
  except KeyboardInterrupt:
    y=None
  except:
    print "invalid input, expecting integer value"
    y=read_int(prompt)
  return y

def read_float(prompt):
  try:
    y_str=raw_input(prompt)
    y=float(y_str)
  except KeyboardInterrupt:
    y=None
  except:
    print "invalid input, expecting floating-point value"
    y=read_float(prompt)
  return y

def read_bool(prompt):
  try:
    y_str=raw_input(prompt)
    if y_str in 'yY':
      y=True
    elif y_str in 'nN':
      y=False
    else:
      raise Exception()
  except KeyboardInterrupt:
    y=None
  except:
    print "invalid input, expecting boolean value (y/n)"
    y=read_bool(prompt)
  return y

def read_str(prompt):
  try:
    y=raw_input(prompt)
  except KeyboardInterrupt:
    y=None
  except:
    print "invalid input"
    y=read_str(prompt)
  return y

def read_date(prompt):
  try:
    y=raw_input(prompt)
    if y=='':
      return None
    from dateutil import parser
    y=parser.parse(y)
  except KeyboardInterrupt:
    y=None
  except:
    print "invalid input (MM/DD/YYYY)"
    y=read_date(prompt)
  return y  

def select_obj_from_list( x ):
  """
  displays a list of objects 'x' and prompts the user for an
  index to select an object, returning that object 
  """
  # check list length
  n = len(x)

  # check for empty list
  if n == 0:
    print ""
    print "No Results Found..."
    return None
  
  # check for 1 obj list
  if n == 1:
    print ""
    print "1 Result: " + str(x[0])
    return x[0]

  # otherwise do the normal thing
  for i in range(n):
    obj = x[i]
    print str(i+1)+". "+str(obj)

  # prompt for index
  opt = -1
  while opt == -1:
    print "" # item is a more user-friendly term than object
    opt = read_int('Select an item: ')
    # cancel if ctrl+c
    if not opt:
      return None
    if opt < 1 or opt > n: # if opt falls outside the proper range,
      opt = -1             # try again

  # get that object
  y = x[opt-1]
  return y

