#!/usr/bin/env python3

import logging
import time

logging.basicConfig(level=logging.DEBUG)

import site
site.addsitedir('.')
from plm2014r import Sign

s = Sign('/dev/ttyUSB0', id=1, retries=20)
count = 1
s.wakeup()
s.run_page('A')
while True:
    s.set_message(f' {count} ')
    count += 1
    time.sleep(0.5)
