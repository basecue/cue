# cue

Pythonic implementation of the observer pattern.

Usage:

```python
import cue

class MyClass:
    @cue.publisher
    def my_method(self, x: str) -> str:
        ...
      
      
 @cue.subscribe(MyClass.my_method)
 def on_method_call(myclass_instance: MyClass, x: str) -> None:
     # called after the myclass_instance.my_method is called
     ...
```


```python

import dataclasses
import cue

@dataclasses.dataclass
@cue.publisher
class MyClass:
    my_attribute: str
    
@cue.subscribe(MyClass.my_attribute)
def on_method_call(myclass_instance: MyClass, value: str):
    # called after myclass_instance.my_attribute assignment
    ...
```


Development:
```
python setup.py bdist_wheel
python -m twine upload dist/cuelib-X.Y.Z-py3-none-any.whl
```