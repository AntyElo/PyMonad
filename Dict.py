from .base import Monad, isMonad

class Dict(Monad):

	def __init__(s, fst=None, **v):
		s.v = v
		s.v["__main__"] = v.get("__main__", fst)

	def bind(s, f, bindto="__main__", simpler=False):
		m = f(s.v[bindto])
		if not isMonad(m):
			return s
		if simpler:
			s.v[bindto] = m.v["__main__"]
		else:
			for k, w in m.v.items():
				s.v[k] = w
		return s

	def __repr__(s):
		return f"Dict {s.v['__main__']}"
