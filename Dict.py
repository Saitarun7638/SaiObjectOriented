fruits = {"Apple": 80, "Banana": 40, "Peach": 30, "Pineapple": 99, "Guava": 55}
name = input("Enter the name of fruit: ")
if name in fruits:
    print(fruits.get(name))
else:
    print('Product not found!')
