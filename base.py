def dot(f, *g):
	if g: return lambda *a, **kw: f(dot(g[0], *g[1:])(*a, **kw))
	else: return lambda *a, **kw: f(*a, **kw)

def passM(attr, *a, **kw):
	"modify attribute of inherit value and pass binding"
	def wrapper(m):
		getattr(m, attr)(*a, **kw)
		return m
	return wrapper

def idf(x):
	"identity function"
	return x

def notf(x):
	return not x

class Applicative(object):
	NAME = "f"

	def __init__(f, v):
		f.v = v

	def fmap(fa, ab, *a, **kw):
		"ab <$> fa"
		fa.v = ab(fa.v, *a, **kw)
		return fa

	def __call__(f, *a, **kw):
		"alias for fmap"
		return f.fmap(*a, **kw)

	def seqapple(fa, fab, *a, **kw):
		"fab <*> fa"
		fb = fab(fa.v, *a, **kw)
		if isinstance(fb, Applicative):
			fa.v == fb.v
		return fa

	def __repr__(f):
		return f"{f.NAME} {f.v}"

	def __eq__(fa, fb):
		return False if not isinstance(fb, Applicative) else fa.v==fb.v

def liftA(f, *a, **kw):
	l = [e.v for e in a if isinstance(e, Applicative)]
	return dot(Pure, f)(*l, **kw)


class Pure(Applicative):
	NAME = "Pure"

	def __init__(s, v, *a, **kw):
		s.v = v
		s.a = a
		s.kw = kw

	def __eq__(pa, pb):
		return False if not isinstance(pb, Pure) else dot(notf, list, filter)(lambda a: getattr(pa, a)!=getattr(pb, a), ["v", "a", "kw"])


class Monad(Applicative):
	"Is Identical monad"
	NAME = "Identical"

	def bind(ma, f):
		"id's `>>=`. It just apply `f` to inherit value"
		mb = f(ma.v)
		if isinstance(mb, Applicative):
			ma.v = m.v # Work fine both with Monad and Pure
		return ma

	def __call__(m, *a, **kw):
		"alias for `bind`"
		return m.bind(*a, **kw)


class Comonad(Applicative):
	NAME = "Comonad"
	def __init__(w, v, f):
		"constructor, uses `.v` for value and `.f` for function"
		w.v = v
		w.f = f

	def duplicate(w):
		f = lambda *a, **kw: w.f(*a, **kw)
		w.f = f
		return w

	def extract(w):
		return w.v

	def extend(w, g):
		w.f = dot(g, w.f)
		return w

	def __call__(w, *a, **kw):
		"alias for `extend`"
		return extend(*a, **kw)

	def __eq__(wa, wb):
		return False if (not hasattr(wb, "v") or not hasattr(wb, "f")) else (wa.v==wb.v)


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
	def __init__(s, f, **kw):
		s.f = f
		s.args = kw.get("args", [])
		s.kw   = kw.get("kw",   {})
		s.name = kw.get("name", "func")
	def __call__(s, *args, **kw):
		s.args += list(args)
		s.kw.update(kw)
		return s
	def __repr__(s):
		return f"{s.name}(*{s.args}, **{s.kw})"
	def lflip(m):
		if len(m.args) < 2: return m
		f, s, *t = m.args
		m.args = [s, f, *t]
		return m
	def rflip(m):
		if len(m.args) < 2: return m
		*t, s, f = m.args
		m.args = [*t, f, s]
		return m
	def run(s):
		return s.f(*s.args, **s.kw)
