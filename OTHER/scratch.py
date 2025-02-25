from collections import deque
import sys

class Person:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
    
    def __str__(self):
        parent_str = f'My parent is {self.parent.name}' if self.parent else ''
        return f'My name is {self.name} {parent_str}'
    
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, Person):
            return self.name == other.name
        return False

if len(sys.argv) > 2:
    print(f'Usage: python3 {sys.argv[0]} <output_pickle_file>')
    exit(0)
output_file = sys.argv[1]
print(output_file)

mk = Person('Maksim', None)
lk = Person('Luke', mk)
baby = Person('Isaac', mk)
print(mk)
print(lk)
print(baby)

asdf = {mk: 48, lk: 12}
asdf[baby] = 9
for item in asdf:
    print(asdf[item])

queue = deque([1])
queue.append(2)
queue.append(3)
print(queue)

class A:
    def __init__(self, a, b):
        self.a = a 
        self.b = b

    def __str__(self):
        return str(self.a)+'-'+str(self.b)

a = A(1,2)
b = A(100,400)
print(a)
print(b)

dct = { a: 'maksim', b: 'marsha'}
print(dct)
print(dct.get(a))