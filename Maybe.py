from base import Monad, Carring

class Maybe(Monad):
	def __init__(self, v, isnothing=False):
		"Is `Just x` | `Nothing`"
		self.n = True if isnothing else False
		self.v = v
	def pure(self, v):
		self.__init__(v, False)
		return self
	def bind(self, f, blind=False):
		"`m >>= f` if not blind, else `m >> f`"
		if self.n: return self
		return f() if blind else f(self.v)
	def __repr__(self):
		if self.n: 
			if self.v!=None:
				return f"Fixed {self.v}" #if is not `()`
			return "Nothing"
		return f"Just {self.v}"
	def __eq__(self, m):
		if hasattr(m, "n"):
			if self.n: return m.n
		if hasattr(m, "v"):
			return self.v==m.v
		return False

def Just(x):
	return Maybe(x, False)

def Fixed(x):
	"Extention of Maybe by PyMonad"
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
	if isNothing(m): raise ValueError("got Nothing")
	else: return m.v

def catMaybes(*a):
	"Filter Justes and append their values to List"
	v = []
	for i in a:
		if not isNothing(i): v.append(fromJust(i))
	from List import List
	return List(*v)

# Some extra:

def divMaybe(a, b):
	"Example of funcion a -> a -> Maybe b"
	if not b: return Nothing
	return Just(a/b)

def divMaybeFixed(a, b):
	"Example of funcion a -> a -> MaybeFixed b"
	if not b: return Fixed(a)
	return Just(a/b)

if __name__ == "__main__":

	print(f'''\
test Carring:
	{ Carring(lambda *x: sum(x), 3)(2)(3)(6)(2) }

test "Just 5 >>= f 0 >>= \\x-> f x 2" (Should be Nothing):
	{ Just(5)( Carring(divMaybe, 1)(0, i=True) )( Carring(divMaybe, 1)(2) ) }

test pure (Should be Fixed 3):
	{ Maybe(1, False).pure(5)( lambda x: Fixed(x-2) )( lambda x: Fixed(x-2) ) }
''')
