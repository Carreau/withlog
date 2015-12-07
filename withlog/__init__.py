"""
A context manager to deal with logging level as context manager. 

"""


__version__ = '0.0.3'

from .withlog import main, print_statement, input, \
                    Message, Info, Warning, Critical, \
                    glog, gStack

if __name__ == '__main__':
     main()

