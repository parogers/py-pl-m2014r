# py-pl-m2014r

Python library for the PL-M2014R LED display sign by Pro-Lite.

## Usage

```python
from pl_m2014r import Sign

sign = Sign('/dev/ttyUSB0', id=1)
sign.wakeup()
sign.set_message('<FC>Hello, sign!')
sign.run_page('A')
```
