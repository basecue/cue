# cue

Pythonic implementation of the observer pattern.

Usage:

```python
import cue

class MyClass:
    @cue.publisher
    def my_method(self, x: Any) -> Any:
        ...
      
      
 @cue.subscribe(MyClass.my_method)
 def on_method_call(myclass_instance: MyClass, x: Any) -> None:
     # called after the myclass_instance.my_method is called
     ...
```


```python

import cue

class MyClass:
    my_attribute: Cue[Any] = Cue()
    
@cue.subscribe(MyClass.my_attribute)
def on_method_call(myclass_instance: MyClass, value: Any):
    # called after myclass_instance.my_attribute assignment
    ...
```
