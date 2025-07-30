from .base import Monad, isMonad

class Dict(Monad):

	def __init__(s, fst=None, **v):
		s.v = v
		s.v["v"] = v.get("v", fst)

	def bind(s, f, *bindto):
		if not bindto: bindto = ["v"]
		m = f(*[s.v[e] for e in bindto])
		if not isMonad(m):
			return s
		for k, w in m.v.items():
			s.v[k] = w
		return s

	def __repr__(s):
		"Show only main inherit value"
		return f"Dict {s.v['v']}"
