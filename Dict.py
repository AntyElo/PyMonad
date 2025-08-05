from .base import Monad, Applicative

class Dict(Monad):

	def __init__(s, fst=None, **v):
		s.v = v
		s.v["v"] = v.get("v", fst)

	def __getitem__(s, *a, **kw):
		return s.v.__getitem__(*a, **kw)

	def __setitem__(s, *a, **kw):
		return s.v.__setitem__(*a, **kw)

	def bind(s, f, *bindto):
		"""
		Update inherit values using f(<args>) values.
		<args> is inherit values named as in bindto
		"""

		if not bindto: bindto = ["v"]
		m = f(*[s.v[e] for e in bindto])
		if isinstance(m, Applicative): # (Dict | Pure)
			for k, w in m.v.items():
				s.v[k] = w
		return s

	def embed(s, k, f, *bindto):
		"""
		Update inherit value with `k` name using f(<args>) value.
		<args> is inherit values named as in bindto
		"""

		if not bindto: bindto = ["v"]
		s.v[k] = f(*[s.v[e] for e in bindto])
		return s

	def __repr__(s):
		"Show only main inherit value"
		return f"Dict {s.v['v']}"
