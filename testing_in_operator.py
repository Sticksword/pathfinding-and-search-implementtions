class A(object):
  def __hash__(self):
    print '__hash__'
    return 42

  # def __cmp__(self): Deprecated in Python 3
  #   print '__cmp__'
  #   return object.__cmp__(self)

  def __eq__(self, rhs):
    print '__eq__'
    return True

a1 = A()
a2 = A()
print a1 in set([a1])
print a1 in set([a2])

print a1 in [a1]
print a1 in [a2]

'''
'in' operator calls __contains__

For a set:
  'Match' if hash(A) == hash(B) and (A is B or A == B) # identity check, then equality check

For a list:
  'Match' if A is B or A == B # same thing but checking against all items in the list
'''