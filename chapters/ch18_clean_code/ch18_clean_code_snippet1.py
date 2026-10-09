"""Code from "18.2 PEP 8: the shared style" that is shown in the book but not run on its own:
it needs your own data, a server or extra setup, or it is one step of an example
that the book builds up gradually. See the book for details."""

import os,sys
def Shipping_Cost( Weight,express ):
  if express==True : return Weight*2.5+10
  else : return Weight*2.5
