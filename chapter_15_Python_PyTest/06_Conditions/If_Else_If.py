#Problem Find the max between 3 numbers
#User Inputs- num1,num2,num3 ->int
#O/P:int or String with max number

num1=int(input("Enter the num1\n"))  #5  #10
num2=int(input("Enter the num2\n"))  #3  #12
num3=int(input("Enter the num3\n"))  #2  #11

# result=max(num1,num2,num3)
# print(result)

if num1>=num2 and num1>=3:
    print(num1)
elif num2>=3 and num2>=1:
    print(num2)
else:
   print(num3)

#Calculate the letter grade based on a numeric score:A:90-100,B:80-89,C:70-79,D:60-69,F:below

num=85

if num<0 or num>100 