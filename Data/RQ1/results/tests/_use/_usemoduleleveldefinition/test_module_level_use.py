class Base:
    ...

class Inherit(Base):
    ...

def func1():
    print(Base)
    return 0
x = []

y: int = 1

t1, t2 = 1, 2

(t3 := 1)
for a, b in x:
    print(a)
    print(b)

print(Base)
print(Inherit)
print(func1)
print(x)
print(y)

print(t1)

print(t2)

print(t3)