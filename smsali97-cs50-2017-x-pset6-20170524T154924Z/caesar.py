import cs50

def main():
    n = cs50.get_int()
    text = input("Your text: ")
    
    for i in range(0,len(text)):
        if text.isalpha(): 
            c = text[i]
            if ( c.isupper() ):
                letter = ord(c) - ord('A')
            else:
                letter = ord(c) - ord('a')
            result = (letter + n) % 26
            
            if (c.isupper()):
                print((chr)(result+ ord('A')),end="")
            else:
                print((chr)(result+ ord('a')) ,end="")
        else:
            c = text[i]
            print(c,end="")
    print()
    
if __name__ == "__main__":
    main()
    
        
    

    