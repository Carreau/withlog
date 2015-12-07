from colorama import Fore, Back, Style

colors = True

def bg(message, level=0, fmt=None):
    if colors:
        if not fmt:
            fmt=Fore.WHITE+getattr(Back, l[level])
        return fmt + message + Style.RESET_ALL
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


from contextlib import contextmanager
import builtins

@contextmanager
def print_statement(p):
    """replace built-in print statement"""
    oldprint = builtins.print
    builtins.print = p 
    try:
        yield (p, oldprint)
    except Exception:
        builtins.print = oldprint
        raise

@contextmanager
def input():
    old_input = builtins.input 
    builtins.input = old_input
    def new_input(prompt):
        if gStack:
            return old_input(gStack[-1].format_line(prompt))
        else:
            return old_input(prompt)
    builtins.input = new_input
    try:
        yield 
    except Exception :
        builtins.input = old_input
        raise
    builtins.input = old_input



def glog(message, *args, **kwargs):
    if gStack:
        gStack[-1].log(message % tuple( str(a) for a in args))
    else:
        print('>>', message)

class Message:

    def __init__(self, title, level=0, fmt=None, writer=print):
        self.title = title
        self.level = level
        self.fmt=fmt
        self.writer = writer

    def log(self, message='', *args, **kwargs):
        return self._log(message, *args, **kwargs)

    def format_line(self, message, *args, **kwargs):
        if not message: 
            message = ''
        message = bg(' ', self.level, self.fmt) + ' ' +  message
        if self.sup:
            return self.sup.format_line(message)
        else :
            return message

    def _log(self, message='', *args, **kwargs):
        m = '\n'.join([self.format_line(m) for m in message.split('\n')])
        self.writer(m, *args, **kwargs)

    def __enter__(self):
        if gStack and gStack[-1] is not self:
            self.sup = gStack[-1]
        else:
            self.sup=None
        if self not in gStack:
            gStack.append(self)
        l = '%s' % (80 - len(gStack)*2)
        self.log(bg(('{:^'+l+'}').format(self.title), self.level, self.fmt))
        self.log()
        return self.log

    def __exit__(self, *args):
        self.log(' ')
        if self.sup:
            self.sup=None
        if gStack[-1] is self:
            gStack.pop()

class Info(Message):
    def __init__(self, title):
        super().__init__(title, 0)

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
