import threading
import time

value1 = 0
value2 = 0
test_vec = [1, 2, 3]


def func1(event1, val1):
    flag1 = event1.wait(timeout=0)
    time.sleep(1)
    if flag1:
        print("Func 1: ", val1)
        event1.clear()
    else:
        print("Flag 1 is False")
        event1.clear()


def func2(event2, val2):
    flag2 = event2.wait(timeout=0)
    time.sleep(1)
    if flag2:
        print("Func 2: ", val2)
        event2.clear()
    else:
        print("Flag 2 is False")
        event2.clear()


def main():

    global value1
    global value2

    event1 = threading.Event()
    event2 = threading.Event()

    global test_vec

    thread1 = threading.Thread(target=func1, args=(event1, value1))
    thread2 = threading.Thread(target=func2, args=(event2, value2))

    while test_vec:

        if not thread1.is_alive() and test_vec:
            value1 = test_vec[0]
            test_vec.pop(0)
            thread1 = threading.Thread(target=func1, args=(event1, value1))
            event1.set()
            thread1.start()
            time.sleep(1)

        if not thread2.is_alive() and test_vec:
            value2 = test_vec[0]
            test_vec.pop(0)
            thread2 = threading.Thread(target=func2, args=(event2, value2))
            event2.set()
            thread2.start()
            time.sleep(1)

    thread1.join()
    thread2.join()
    print("End of execution")


if __name__ == '__main__':
    main()
