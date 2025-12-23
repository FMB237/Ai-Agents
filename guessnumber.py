#This is a small python code for a guessnumber games

import random

secret_number=random.randint(1,10)
attemps=4

print("I'm thinking of a number between 1 and 10")

while attemps > 0:
    guest = int(input("Take a Guest :"))
    if(guest==secret_number):
        print("Congratulation you have guess the number")
        break 
    elif guest < attemps :
        print(' Too low, Try again')
    else:
        print("Too high,Try again")
        attemps -=1 #Increamenting down
if attemps == 0:
    print("You have run all attemps",secret_number)   
        
     