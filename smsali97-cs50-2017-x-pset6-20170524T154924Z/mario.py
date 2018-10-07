import cs50

def main():
    while True:
        print("height: ", end="")
        h = cs50.get_int()
        if h >= 0 and h <= 23:
            break
    for i in range(2,2 + h):
        k = h - i
        while k >= 0:
            print(" ",end="")
            k -= 1 
        for j in range (0,i):
            print("#",end = "")
        print()
            
if __name__ == "__main__":
    main()
    
    
    
    
