def receiver():
    while True:
        data = yield
        print("Received:", data)


gen = receiver()

next(gen)

gen.send("Python")
gen.send("Dawood")

    



