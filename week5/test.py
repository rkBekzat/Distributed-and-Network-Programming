

for n in range(1, 25):
     for a in range(1, 25):
          h = (2**n)
          print(n, a, (a**h)%(h*4))