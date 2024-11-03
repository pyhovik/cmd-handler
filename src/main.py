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
os.write(fout, b' # ')
data = b''
while 1:
    old_settings = termios.tcgetattr(fin)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        os.write(fout, ch.encode())
        data = data + ch.encode()
        if ch == '?':
            os.write(sys.stdin.fileno(), b'\n\ryes\n')
            os.write(fout, data)
        if ord(ch) in [13]: # 13 - '\r'
            break
    finally:
        termios.tcsetattr(fin, termios.TCSADRAIN, old_settings)
os.write(fout, b'\n')
if b'dima' in data:
    os.write(fout, b'\nopopopopo\n')
os.write(fout, data)
os.write(fout, b'\n')
os.write(fout, b' # \n')