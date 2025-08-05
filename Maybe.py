from .base import Monad, Applicative

class Maybe(Monad):

	def __init__(self, x, isnothing=False):
		"Is `Just x` | `Nothing`, defaults to Just"
		self.n = True if isnothing else False
		self.v = x

	def bind(self, f, blind=False):
		"`>>=` if not blind, else `>>`"
		if self.n: return self
		if not blind: f = f(self.v)
		if isinstance(f, Maybe):       self.n = f.n
		if isinstance(f, Applicative): self.v = f.v
		return self

	def __repr__(self):
		"Fixed None === Nothing"
		return f"Just {self.v}" if not self.n else ("Nothing" if self.v==None else f"Fixed {self.v}")

	def __eq__(self, m):
		if isinstance(m, Maybe):
			if self.n: return m.n
		if isinstance(m, Applicative):
			return self.v==m.v
		return False

def Just(x):
	return Maybe(x, False)

def Fixed(x):
	"Extented Maybe: Nothing is just Fixed None"
	return Maybe(x, True)

Nothing = Fixed(None)

def isNothing(m):
	return m==Nothing

def isJust(m):
	return not m.n

def isFixed(m):
	return (m.n and m.v)

def maybe(c, f, m):
	return f(m) if isJust(m) else c

def fromMaybe(c, m):
	if isNothing(m): return c
	else: return m.v

def fromJust(m):
	"Extraxt value from `Just x` or `Fixed x`"
	if isNothing(m): raise ValueError("got Nothing")
	else: return m.v

def catMaybes(*a):
	"Filter Justes and append their values to List"
	v = []
	for i in a:
		if not isNothing(i): v.append(fromJust(i))
	from List import List
	return List(*v)

def testMaybe():
	"Unit test"
	from .base import Carring, Pure

	def divMaybe(a, b):
		"Example of funcion a -> a -> Maybe b"
		if not b: return Nothing
		return Just(a/b)

	def divMaybeFixed(a, b):
		"Example of funcion a -> a -> MaybeFixed b"
		if not b: return Fixed(a)
		return Just(a/b)

	print(f'''\
test "Just 5 >>= f  0 >>= \\x-> f  x 2": {
	Just(5)( Carring(divMaybe, 1)(0, i=True) )( Carring(divMaybe, 1)(2) ) 
} [Nothing]

test "Just 5 >>= f' 0 >>= \\x-> f' x 2": {
	Just(5)( Carring(divMaybeFixed, 1)(0, i=True) )( Carring(divMaybeFixed, 1)(2) ) 
} [Fixed 5]

test Pure: {
	Maybe(1, False)(Pure(5), 1)( lambda x: Fixed(x-2) )( lambda x: Fixed(x-2) )
} [Fixed 3]
''')