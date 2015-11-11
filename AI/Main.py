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
        Student_Create.generate()
        print("\nStudents Created")
    elif ans=="2":
        Student_Clean.clean()
        print("\nStudents directory cleaned!")
    elif ans=="3":
        print("\nAPI Status: ")
    elif ans=="4":
        print("\nGoodbye")
        exit(1)
    elif ans !="":
        print("\nNot Valid Choice Try again")