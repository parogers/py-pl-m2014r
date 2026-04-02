# PL-M2014R Protocol Library

Python library for the PL-M2014R LED display sign by Pro-Lite. It's a scrolling marquee type of sign that were often found in store front windows. They use a relatively simple text protocol over serial with escape codes for changing font, color, messages, displaying simple dot matrix graphics etc.

## Protocol documentation

There's an [excellent reference](https://wls.wwco.com/ledsigns/prolite/ProliteProtocol.html) for this particular model of sign.

## Usage

```python
from plm2014r import Sign

sign = Sign('/dev/ttyUSB0', id=1)
sign.wakeup()
sign.set_message('<FC>Hello, sign!')
sign.run_page('A')
```
