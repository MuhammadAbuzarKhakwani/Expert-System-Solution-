counter = 0
count = 0
word_list = []

while counter < 7:
    word = input("Enter a Word: ")
    word_list.append(word)
    counter += 1

while count < 7:
    if count % 2 == 0:
        print(word_list[count])

    count += 1