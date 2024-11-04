import tty, termios, sys, os, string
from commands import *

# получить номера дескрипторов потоков
fin = sys.stdin.fileno()
fout = sys.stdout.fileno()
PROMPT = ' # '
TIP_TEXT = 'tip text'

def input_wrapper(prompt, tip_text) -> str:
    buffer = b''
    # сохранить предыдущие настройки терминала
    old_settings = termios.tcgetattr(fin)
    try:
        # перевести терминал в raw mode
        tty.setraw(sys.stdin.fileno())
        # пока осуществляется ввод...
        while 1:
            # читать по одному символу из stdin
            ch = sys.stdin.read(1)
            if ch == '?':
                os.write(fout, b'\r\n')
                os.write(sys.stdin.fileno(), tip_text.encode())
                os.write(fout, b'\r\n')
                os.write(fout, prompt.encode())
                os.write(fout, buffer)
            # завершить цикл при нажатии ENTER
            elif ch == '\r': # enter button
                break
            # записать в буфер все видимые символы
            elif ch in string.printable: 
                os.write(fout, ch.encode())
                buffer = buffer + ch.encode()
    finally:
        termios.tcsetattr(fin, termios.TCSADRAIN, old_settings)
    return buffer.decode()

while 1:
    os.write(fout, PROMPT.encode())
    data = input_wrapper(PROMPT, TIP_TEXT)
    if 'exit' == data:
        os.write(fout, b'\n')
        break
    try:
        os.write(fout, command_map[data].encode())
    except KeyError:
        pass
    os.write(fout, b'\n')
