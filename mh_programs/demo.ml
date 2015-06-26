fib = 0
next = 1
index = 30

while index {
    temp = fib + next
    fib = next
    next = temp
    index = index - 1
}

fib