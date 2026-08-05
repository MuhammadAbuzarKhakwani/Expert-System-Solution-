cinema = [
    [11,12,13,14,15],
    [21,22,23,24,25],
    [31,32,33,34,35],
    [41,42,43,44,45],
    [51,52,53,54,55]
]

while True:

    print(".........................................................................")
    print("......................Hello! Welcome to David Cinema.....................")
    print()

    for row in cinema:
        print("                       ", row)

    print()

    print("Enter seat number (Example: 23)")
    print("Enter 0 to Exit")

    s_no = input("Enter here: ")

    # Exit
    if s_no == "0":
        print("Thank you for visiting David Cinema!")
        break

    
    if len(s_no) != 2 or not s_no.isdigit():
        print("Invalid seat number!\n")
        continue

    row = int(s_no[0]) - 1
    col = int(s_no[1]) - 1

    
    if row < 0 or row > 4 or col < 0 or col > 4:
        print("Seat does not exist!\n")
        continue

    if cinema[row][col] != "X":
        cinema[row][col] = "X"
        print("Seat booked successfully!\n")
    else:
        print("Seat already booked!\n")