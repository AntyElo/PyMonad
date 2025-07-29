from .base import Monad

class Logger(Monad):

	def __init__(self, optional, msg=None):
		"Is `Logger x ss`"
		self.v = optional
		if msg==None: msg = f"return {self.v}"
		self.log = [msg]

	def bind(self, f):
		"`m >>= f`"
		m = f(self.v)
		assert isinstance(m, Logger)
		self.log += m.log
		self.v    = m.v
		return self

	def __repr__(self):
		return "\n".join(map(
			(lambda E: f"[{E[0]:0>4}] {E[1]}")
			, list(enumerate(self.log))
		)) + f"\n[expv] {self.v}"

def add5_wlog(v):
	return Logger(v+5, f"Add 5 to {v}")


if __name__ == "__main__":

	print(f'''\
Logger of 13 binded to add5: [18 + logs]:
{ Logger(13)(add5_wlog) }
''')
