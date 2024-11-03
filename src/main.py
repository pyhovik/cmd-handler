# import tty, termios, sys, os
# fd = sys.stdin.fileno()

# def getchar():
#    #Returns a single character from standard input
#    old_settings = termios.tcgetattr(fd)
#    try:
#       tty.setraw(sys.stdin.fileno())
#       ch = sys.stdin.read(1)
#    finally:
#       termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#    return ch
   
# while 1:
#     ch = getchar()
#     os.write(sys.stdin.fileno(), ch.encode())
#     if ch == 'q': 
#        break
#     elif ch == '?':
#         os.write(sys.stdin.fileno(), b'\nyes\n')

import tty, termios, sys, os
fin = sys.stdin.fileno()
fout = sys.stdout.fileno()
prompt = ' # '

def wrapper():
    data = b''
    old_settings = termios.tcgetattr(fin)
    try:
        tty.setraw(sys.stdin.fileno())
        while 1:
            ch = sys.stdin.read(1)
            if ch == '?':
                os.write(fout, b'\r\n')
                os.write(sys.stdin.fileno(), b'yes')
                os.write(fout, b'\r\n')
                os.write(fout, prompt.encode())
                os.write(fout, data)
            else: 
                os.write(fout, ch.encode())
                data = data + ch.encode()
            if ord(ch) in [13]: # 13 - '\r'
                break
    finally:
        termios.tcsetattr(fin, termios.TCSADRAIN, old_settings)
    return data

while 1:
    os.write(fout, b' # ')
    data = wrapper().decode()
    if 'dima' in data:
        os.write(fout, b'\nopopopopo')
    if 'exit' in data:
        break
    os.write(fout, b'\n')
