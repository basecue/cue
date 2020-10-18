# cue

Pythonic implementation of the observer pattern.

Usage:

```python
import cue

class MyClass:
  @cue.publisher
  def method(self, x):
      return x
      
      
 @cue.subscribe
 def on_method_call(myclass_instance, x):
     print(x)
```
