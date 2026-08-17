'''
  Task
Given an integer, , perform the following conditional actions:

If  is odd, print Weird
If  is even and in the inclusive range of 2-5 to , print Not Weird
If  is even and in the inclusive range of 6-20 to , print Weird
If  is even and greater than , print Not Weird
Input Format

A single line containing a positive integer, .

Constraints

Output Format

Print Weird if the number is weird. Otherwise, print Not Weird'''

num = int(input())

if num > 0:
    if num%2 == 0:
        if 2<= num <= 5:
            print("Not Weird")
        elif 6<= num <= 20:
            print("Weird")
        else:
            print("Not Weird")
    else:
        print("Weird")
else:
    print("Please enter a positive number")