"""
  @file   inv/view/cli/common.py
  @author Brian Kim
  @brief  a script containing the methods necessary
          to design a robust command-line interface
"""

import sys

def read_int(prompt):
  try:
    y_str=raw_input(prompt)
    y=int(y_str)
  except:
    print "invalid input, expecting integer value"
    y=read_int(prompt)
  return y

def read_float(prompt):
  try:
    y_str=raw_input(prompt)
    y=float(y_str)
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
  except:
    print "invalid input, expecting boolean value (y/n)"
    y=read_bool(prompt)
  return y

def read_str(prompt):
  try:
    y=raw_input(prompt)
  except:
    print "invalid input"
    y=read_str(prompt)
  return y
