def dot(f, g):
	return lambda *a, **kw: f(g(*a, **kw))

def isMonad(m):
	return hasattr(m, "MONAD")

def isComonad(m):
	return hasattr(m, "COMONAD")

def passM(attr, *a, **kw):
	"modify attribute of inherit value and pass binding"
	def wrapper(m):
		getattr(m, attr)(*a, **kw)
		return m
	return wrapper

class Monad(object):
	MONAD = True

	def __init__(self, v):
		"`pure` of Identical monad"
		self.v = v

	def pure(self, *a, **kw):
		"Make `pure` great again."
		self.__init__(*a, *kw)
		return self

	def bind(self, f):
		"id's `>>=`. It just apply `f` to inherit value"
		self.v = f(self.v)
		return self

	def __call__(self, *a, **kw):
		"alias for `bind`"
		return self.bind(*a, **kw)

	def __eq__(self, m):
		if isMonad(m):
			return self.v==m.v
		return False


class Comonad:
	COMONAD = True

	def __init__(s, v, f):
		"constructor, uses `.v` for value and `.f` for function"
		s.v = v
		s.f = f

	def duplicate(s):
		f = lambda *a, **kw: s.f(*a, **kw)
		s.f = f
		return s

	def extract(s):
		return s.v

	def extend(s, g):
		"alias for `extend`"
		"`extend` (alias)"
		s.f = dot(g, s.f)
		return s

	def __call__(s, *a, **kw):
		"alias for `extend`"
		return extend(*a, **kw)


class Carring(object):

	def __init__(s, f, hm=1):
		s.f = f
		s.hm = hm

	def __call__(s, a=None, **kw):
		s.hm =  kw.get("c", s.hm) # carrings
		s.hm += kw.get("ci", 0) # increment to
		if kw.get("dry", False): return s
		if s.hm <= 0: return s.f(a)
		s.hm-=1
		if kw.get("i", False): # inversed appling
			s.f = (lambda *x, f=s.f, a=a: f(*x, a))
		else:
			s.f = (lambda *x, f=s.f, a=a: f(a, *x))
		return s


class LazyCarring(object):
	def __init__(s, f, hm=1):
		s.f = f
		s.args = []
		s.kw = {}
	def __call__(s, *args, **kw):
		s.args += list(args)
		s.kw.update(kw)
		return s
	def flip(s):
		f, s, *t = s.args
		s.args = [s, f, *t]
		return s
	def run(s):
		return s.f(*s.args, **s.kw)


def pure(v, example=None):
	"return `v` to `example`'s monad context"
	t = Monad if example==None else example.__class__
	return t.pure(t(), v)


if __name__ == "__main__":

	print(f'''\
test Carring [13]:
	{ Carring(lambda *x: sum(x), 3)(2)(3)(6)(2) }
''')
