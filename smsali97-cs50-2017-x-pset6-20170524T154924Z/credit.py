import cs50

# take the number and store it
l = cs50.get_int()
x = l
ctr = 0
sum1 = 0
while x > 0:
    # do it in alternate numbers
    if ctr % 2 == 1:
        # take the last digit out
        n = 2*(x % 10)
        if n >= 10:
            while n > 0:
                sum1 += n%10
                n = n//10
        else: 
            sum1 += n%10
    x = x//10
    ctr += 1
ctr = 0
while l > 0:
    if ctr % 2 == 0:
        sum1 += l%10
    ctr += 1
    l = l//10

if sum1 % 10 == 0:
    print("AMEX")
else:
    print("INVALID")