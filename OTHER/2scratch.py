import time, collections as coll, time
from my_modules import misc_tools as bm

loop_count = 1
with bm.DelayedKeyboardInterrupt() as blah:
    while not blah.get_outta_here:
        for n in range(50):
            print(f'{loop_count} - {n}')
            time.sleep(0.05)
        loop_count += 1

queue = coll.deque([123]) # just testing calling an imported module that was imported as a list
print(queue)
