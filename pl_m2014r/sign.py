#
# Protocol reference:
#
# https://wls.wwco.com/ledsigns/prolite/ProliteProtocol.html
#

import time
from serial import Serial


class NoResponse(Exception):
    pass


class InvalidCommand(Exception):
    pass


def _fmt_id(id):
    return f'<ID{id:02x}>'


def _read_response(serial, timeout=0):
    start = time.time()
    response = bytes()
    while True:
        ch = serial.read()
        if ch:
            response += ch
            if ch[0] == 0x11:
                assert response[0:4] == b'\x13<ID'
                response_id = int(response[4:5].decode('utf-8'), 16)
                response_code = response[7:8].decode('utf-8')
                return response_code
        elapsed = time.time() - start
        if timeout > 0 and elapsed > timeout:
            raise NoResponse(response)


def _validate_id(id):
    assert id >= 0 and id <= 255


def _validate_page(page):
    assert page >= 'A' and page <= 'Z'


class Sign:
    def __init__(self, device, baud=9600, id=1):
        _validate_id(id)
        self.device = device
        self.baud = baud
        self.sign_id = id

    def _send_data(self, serial, data_bytes, response_timeout):
        serial.write(data_bytes)
        serial.flush()
        if self.sign_id != 0:
            response_code = _read_response(
                serial,
                timeout=response_timeout,
            )
            if response_code != 'S':
                raise InvalidCommand(response_code)

    def send_command(self, cmd, response_timeout=1, retries=0):
        data_bytes = (cmd + '\r\n').encode('utf-8')
        with Serial(
            self.device,
            self.baud,
            timeout=1,
        ) as serial:
            start = time.time()
            for n in range(retries+1):
                try:
                    return self._send_data(serial, data_bytes, response_timeout)
                except NoResponse:
                    pass
            raise NoResponse()

    def set_message(self, message, page='A'):
        _validate_page(page)
        self.send_command(f'{_fmt_id(self.sign_id)}<P{page.upper()}>{message}')

    def run_page(self, page):
        _validate_page(page)
        self.send_command(f'{_fmt_id(self.sign_id)}<RP{page.upper()}>')

    def wakeup(self):
        self.send_command(_fmt_id(self.sign_id))
