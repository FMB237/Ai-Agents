#This is a file used to recall basics concepts of the python programming lanaguage
print("Hello world")
#These are mainly numrical values
a= 15 
b = 12
c =  23
d = 15
is_Student=True #This is an exemple of a boolean variable
print(is_Student)

sum=a+b
differcent= a- b
product = a*b
quotient = a-b

print(sum)
print(product)

name=input("What is your name ? :")
age=input("What is your age ? :")
status=input("What are a Student ? :")
os=input('What Os do you use ?:')

print(f'my name is {name} i am {age} years old i am also a {status} and i use {os} as Daily operating system' )

          
'''if(a<b):
    print(f"{b} is greater than {a}")
else:
    print(f'{a} is greater than {b}')
    
print(c // d)   
#Let do some switch case '''   

count=0
while(count <= 5):
    print("Good bro")
    count=count +1


#Let do some arrays

Fruits=["banana","Apple","Pinapple"]
print(Fruits)
print(Fruits[0])
Fruits.append('Mangoes')
print(Fruits)

#Let go and look at the used of functions in python

def hello():
    print("Using a Hello World funtion")
 
hello()    


#Let do same for our arithmetic functions
def Quotient(a,b,c): #Passing paramters to the Functions for division
    return a/b/c

result=Quotient(5,50,0.05)
print(result)