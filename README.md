# PyMonad

Just some monadic stuff for python3

``` python3
import pymonad as me
print(
	me.bind(me.Just("Hello"), lambda x: Just(str(x)+" pymonad!"))
)
```

is like

``` haskell
main = print $ Just "Hello" >>= return.(++" pymonad!")`
```