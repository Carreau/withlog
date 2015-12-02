
"""
a simple package
"""


__version__ = '0.0.1'


from colorama import Fore, Back, Style

colors = True

def bg(message, level=0):
    if colors:
        return Fore.WHITE+getattr(Back, l[level]) + message + Style.RESET_ALL
    else:
        return nc[level]+message
def fg(message, level=0):
    return getattr(Fore, l[level]) + message + Style.RESET_ALL

gStack = []

l = {
    0: 'BLUE',
    1: 'GREEN',
    2: 'YELLOW',
    3: 'RED'
   }

nc = {
        0: '\u2503',
        1: '\u2503',
        2: '\u2503',
        3: '\u2503',
}
    


def glog(message):
    if gStack:
        gStack[-1].log('global message')
    else:
        print('>>', message)

class Message:

    def __init__(self, title, level=0):
        self.title = title
        self.level = level

    def log(self, message=''):
        return self._log(message)

    def _log(self, message=''):
        m = '\n'.join([bg(' ', self.level) + ' ' +  m for m in message.split('\n')])
        if self.sup:
            self.sup.log(m)
        else:
            print(m)

    def __enter__(self):
        if gStack:
            self.sup = gStack[-1]
            self.sup.log(' ')
        else:
            self.sup=None
        gStack.append(self)
        l = '%s' % (80 - len(gStack)*2)
        self.log(bg(('{:^'+l+'}').format(self.title), self.level))
        self.log()
        return self.log

    def __exit__(self, *args):
        self.log(' ')
        if self.sup:
            self.sup.log(' ')
            self.sup=None
        gStack.pop()
        pass

class OK(Message):
    def __init__(self, title):
        super().__init__(title,1)
    
class Warning(Message):
    def __init__(self, title):
        super().__init__(title,2)


class Critical(Message):
    def __init__(self, title):
        super().__init__(title,3)
    


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--nocolors', action='store_false')
    args = parser.parse_args()
    global color
    colors=args.nocolors
    with Message('Hello there') as log:
        log('This is a Logging message context manager')
        log('it support nesting and will render in a User friendly way')
        log('I need to fix multi \nline \nstring')
        with Warning('Nested it does support') as log1:
            log1('like Yoda speach order ')
            log1('of words are')

        with Critical('Come to the dark side') as log2:
            log2('we have cookies')

            with OK("Paternity test") as log3:
                log3('I am your father')

        log('So ?')


if __name__ == '__main__':
     main()

