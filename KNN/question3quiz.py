def counter(x):
    count = x
    def increment():
        nonlocal count
        count+=1
        return count
    return increment

myFunction = counter(5)
print(myFunction())
print(myFunction())