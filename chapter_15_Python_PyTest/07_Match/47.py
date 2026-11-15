#In python we dont have the switch keyword.We have match keyword.We dont have the default .we have _

day=int(input("Enter a day from 1 to 7:"))

match day:
      case 1:
        print("Monday")
      case 2:
        print("Tuesday")
      case 3:
        print("Wednesday")
      case 4:
        print("Thursday")
      case 5:
       print("Friday")
      case 6 | 7:
       print("Weekend")
      case _:
       print("Invalid day")