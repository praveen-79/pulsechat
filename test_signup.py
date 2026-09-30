from database import signup

username = input("Enter username: ")
password = input("Enter password: ")

if signup(username, password):
    print("Signup successful!")
else:
    print("Username already exists!")