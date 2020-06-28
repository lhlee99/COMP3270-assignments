class Test():
    def __init__(self, a):
        self.n = a

if __name__ == "__main__":
    t = Test(1)
    l = [t]
    t = Test(2)
    l.append(t)
    print(min(1,2,3,4,5))