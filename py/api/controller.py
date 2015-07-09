"""
  @file   inv/api/controller.py
  @author Brian Kim
  @brief  this module defines the functionality of 
          the methods described by inv/api/methods.py
"""

import auth


def login(uname,pw):
  # ZZ: alot more involved in authenticating here...
  return auth.auth_inv(uname,pw)
