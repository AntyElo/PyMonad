from .base import Monad

class List(Monad):

	def __init__(s, *v):
		s.v = v

	def bind(s, f, blind=False):
		v = []
		if blind:
			for e in s.v: v += f().v
		else:
			for e in s.v: v += f(e).v
		s.v = v
		return s

	def __repr__(s):
		return f"List {s.v}"
