import tty, termios, sys, os, string

# получить номера дескрипторов потоков
fin = sys.stdin.fileno()
fout = sys.stdout.fileno()
PROMPT_UNPRIVILEGED = 'CMD_HANDLER# '
PROMPT_PRIVILEGED = 'CMD_HANDLER(config)# '
SNMP_TRAPS_TIP = """  config           Enable SNMP config traps\r
  entity           Enable SNMP entity traps\r
  flash            Enable SNMP FLASH traps\r
  snmp             Enable SNMP traps\r
  syslog           Enable SNMP syslog traps\r
  <cr>\r

"""

def input_wrapper(prompt, tip_text) -> str:
    """
    Функция-обертка, которая посимвольно обрабатывает пользовательский ввод в поисках символа-подсказки ("?") и управляющих символов.
    При нахождении символа в stdout выводится заранее определенная строка.
    """
    buffer = b''
    # сохранить предыдущие настройки терминала
    old_settings = termios.tcgetattr(fin)
    try:
        # перевести терминал в raw mode
        tty.setraw(fin)
        # пока осуществляется ввод...
        while 1:
            # читать по одному символу из stdin
            ch = sys.stdin.read(1)
            if ch == '?':
                os.write(fout, b'\r\n')
                os.write(fout, tip_text.encode())
                os.write(fout, b'\r\n')
                os.write(fout, prompt.encode())
                os.write(fout, buffer)
            # завершить цикл при нажатии ENTER или CTRL+C
            elif ch in ['\r', '\u0003', '\n']: # enter button
                break
            # записать в буфер все видимые символы
            elif ch in string.printable: 
                os.write(fout, ch.encode())
                buffer = buffer + ch.encode()
    # вернуть настройки терминала после окончания ввода
    finally:
        termios.tcsetattr(fin, termios.TCSADRAIN, old_settings)
    return buffer.decode()

def init_aliases():
    """
    Функция для определения скриптов-алиасов.
    Возвращает карту алиас-скрипт, которая получена путем сканирования файла aliases.sh.
    """
    module_name = __file__.rsplit('/')[-1]
    aliases_file_path = __file__.replace(module_name, 'aliases.sh')
    aliases_map = dict()
    with open(aliases_file_path) as aliases_file:
        for line in aliases_file:
            # получаем список в формате [alias, script_path]
            alias_to_script_list = line.rstrip().replace('alias ', ''). replace("'", '').split('=')
            # если есть алиас...
            if alias_to_script_list[0]:
                # то добавляем его в карту
                aliases_map[alias_to_script_list[0]] = alias_to_script_list[1]
    return aliases_map

def handler_loop():
    # получить список алиасов
    try:
        alias_map = init_aliases()
    except:
        alias_map = dict()
    prompt = PROMPT_UNPRIVILEGED
    while 1:
        os.write(fout, prompt.encode())
        data = input_wrapper(prompt, SNMP_TRAPS_TIP)
        if data == 'exit':
            os.write(fout, b'\n')
            break
        # смена промпта на привилегированный
        elif data == 'configure':
            prompt = PROMPT_PRIVILEGED
            os.write(fout, b'\n')
        # смена промпта на непривилегированный
        elif data == 'end':
            prompt = PROMPT_UNPRIVILEGED
            os.write(fout, b'\n')
        # если прислали какую-то строку, то пытаемся обработать
        elif data:
            try:
                # разбить строку на слова
                command_words = data.split()
                # если первое слово есть в списки алиасов...
                if command_words[0] in alias_map.keys():
                    # список с результатами обработки слов
                    result_command_words = []
                    # то в цикле заменяем эти слова на алиасы из aliases.sh
                    for word in command_words:
                        result_command_words.append(alias_map[word] if word in alias_map.keys() else word)
                    # склеиваем список из обработанных слов в строку
                    result_command = " ".join(result_command_words)
                    os.write(fout, b'\n')
                    # и пытаемся выполнить команду
                    os.system(f"sh {result_command}")
                # если первого слова нет в списке алиасов, то просто напечатать символ \n
                else:
                    os.write(fout, b'\n')
            # на исключения внимания не обращаем
            except:
                continue
        # если нет совпадений ни по одному условию - печатать символ \n
        else:
            os.write(fout, b'\n')

if __name__ == '__main__':
    handler_loop()