n  = int(input("Enter any number: "))

l = []

for i in range(n):
    if n >= 1 and n <= 150:
        l.append(n)
        n = n - 1

new_l  = l[::-1]

for i in new_l:
    print(i,end = "")


#goal if n is 3 than print 1235
