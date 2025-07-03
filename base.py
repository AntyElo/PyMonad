class Monad(object):
	def __init__(self, v):
		"`return x` and `pure x` -- identical monad"
		self.v = v
	def pure(self, *a, **kw):
		self.__init__(*a, *kw)
		return self
	def bind(self, f):
		"id's bind. It just apply `f` to theirself value"
		self.v = f(self.v)
		return self
	def __call__(self, *a, **kw):
		"alias for bind"
		return self.bind(*a, **kw)
	def __eq__(self, m):
		if hasattr(m, "v"):
			return self.v==m.v
		return False

class Carring(object):
	def __init__(s, f, hm=1):
		s.f = f
		s.hm = hm
	def __call__(s, a=None, **kw,):
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

def pure(v, example=None):
	"return `v` to `example`'s monad context"
	t = Monad if example==None else example.__class__.__new__()
	return t.pure(t(), v)
