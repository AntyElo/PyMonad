# PyMonad

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