def carr(f, *a, **kw):
	"carry funcion: \\x->(f x) z"
	return lambda x: f(x, *a, **kw)

def carl(f, *a, **kw):
	"carry funcion: \\x->(f z) x"
	return lambda x: f(*a, x, **kw)

class Monad(object):
	def __init__(self, v):
		"`return x` and `pure x`"
		self.v = v
	def re(self, *a, **kw):
		self.__init__(*a, *kw)
		return self

def bind(m, *fs):
	for f in fs:
		m = m.__bind__(f)
	return m

def bbind(m, *fs):
	for f in fs:
		m = m.__bind__(f, True)
	return m
