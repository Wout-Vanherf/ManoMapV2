test = [1,2,3,4,5,6,7,8,9,10,11]

def remove_all(inp):
    for val in inp:
        inp.remove(val)

print(test)
remove_all(test)
print(test)
