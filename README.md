# PyMonad

![THIS IS A REAL CAT!!! zOMG!!1](./cat.jpg "Chilled down cat")

Just some monadic stuff for python3

```python3
import pymonad as me
print(
	me.fromMaybe("",
		me.Just("Hello")(
			lambda x: Just(str(x)+" pymonad!")
)))
```

is like

```haskell
import Data.Maybe
main = (print . fromMaybe "") $ Just "Hello" >>= return.(++" pymonad!")`
```

## Examples

### pymonad.Dict

```python3
import pymonad as you 

d = you.Dict("world", hello="Hello"
	)( lambda *x: you.Dict(f"{x[0]} {x[1]}"), "hello", "v"
	)( lambda x:  you.Dict(hello=42), "hello"
	)

print(d.v["v"])     # prints "Hello world"
print(d.v["hello"]) # prints 42
```
