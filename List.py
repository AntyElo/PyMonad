from base import Monad

class List(Monad):
	def __int__(s, *v):
		s.v=v
	def __bind__(s, f, blind=False):
		v = []
		if blind: 
			for w in s.v: v+=f().v
		else:
			for w in s.v: v+=f(w).v
		s.v=v
		return s
	def __repr__(s):
		return f"{s.v}"
	def __eq__(s, m):
		return s.v==m.v