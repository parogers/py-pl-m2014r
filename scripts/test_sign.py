#!/usr/bin/env python3

from serial import Serial
import time

import site
site.addsitedir('.')
from pl_m2014r import Sign

s = Sign('/dev/ttyUSB0', id=1)
count = 1
s.wakeup()
s.run_page('A')
while True:
    s.set_message(f' {count} ')
    count += 1
    time.sleep(0.5)
