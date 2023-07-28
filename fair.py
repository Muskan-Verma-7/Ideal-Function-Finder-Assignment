from rough import Testing
from rough2 import Rough
if __name__ == '__main__':
    e = 5
    f = 3
    g = 2
    h = 1
    maths = Testing(e, f, g, h)
    add,sub = maths.calculate()
    output = Rough(add,sub)
    output.print_output()


