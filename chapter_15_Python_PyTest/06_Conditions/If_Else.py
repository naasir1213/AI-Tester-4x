age=int(input("Enter your age:"))

if age>=21:
    print("You can go the club")
else:
    print("Not Allowed")

#Find the positive number is even or odd
#Strip remove the extra spaces
num=int(input("enter a number").strip())

if num>=0:
   print("Positive")
   if num%2==0:
      print("Even")
   else:
      print("odd")
else:
    print("Negative")