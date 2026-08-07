'''
Perform the following operations:
Print the details of every employee.
Print only the names of all employees.
Calculate and print the total salary of all employees.
Find the employee with the highest salary.
Add a new employee named Bilal with:
Salary = 65000
Age = 27
Department = "Marketing"
Update Sara's salary to 58000.
Add a new key "Experience" for every employee and set it to 2 years.
Remove the "Age" key from every employee.
Ask the user to enter an employee's name.
If the employee exists, print all of their details.
Otherwise, print "Employee not found".
Finally, print the updated dictionary.

Bonus Challenge:

Count how many employees belong to each department.
Print the average salary of all employees.

This covers almost every important nested dictionary operation you'll encounter in Python. Try solving it on your own, and I'll review your solution if you get stuck.
'''
niit_emp = {
    "Dawood" : {
        "Salary" : 50000,
        "Age": 20,
        "Department" : "Word press Dev"
    },
    "Abuzar" : {
        "Salary" : 150000,
        "Age": 22,
        "Department" : "Development"
    },
    "Abd" : {
        "Salary" : 55000,
        "Age": 25,
        "Department" : "Word press Dev"
    }
}

#printing name of all employees
#for key in niit_emp:
   # print("Employee Name: ",key)


for key,vss in niit_emp.items():
    print("Employee: ",key)


    if isinstance(vss,dict):
        for ke,vsd in vss.items():
            print(ke," : ",vsd)
    print(" ")






    