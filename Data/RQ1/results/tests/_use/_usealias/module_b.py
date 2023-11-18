from module_a import func as f, x as x_b, ClassA as c
import module_a as a

print(f, x_b, c, a)

def foo():
    print(f, x_b, c, a)

class ClassB:
    print(f, x_b, c, a)