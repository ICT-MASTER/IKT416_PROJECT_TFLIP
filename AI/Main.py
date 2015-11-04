import Student_Create
import Student_Clean



ans=True
while ans:
    print ("""1. Generate Students
2. Clean Students
3. Check API Connectivity
4. Exit/Quit
""")
    ans=input("What would you like to do? ")
    if ans=="1":
        print("\n Students Created")
    elif ans=="2":

        print("\n Students directory cleaned!")
    elif ans=="3":
        print("\n API Status: ")
    elif ans=="4":
        print("\n Goodbye")
        exit(1)
    elif ans !="":
        print("\n Not Valid Choice Try again")