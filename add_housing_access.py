from app import db, User

if __name__ == '__main__':
    email = input("Enter the email to add: ")
    username = input("Enter the username to add: ")
    password = input("Enter your password: ")
    pass_confirm = input("Please re-input your password for confirmation: ")
    while pass_confirm != password:
        password = input("Passwords did not match. Try again or exit to restart: ")
        pass_confirm = input("Confirm your password: ")
    user = User(email, username, password)
    db.session.add(user)
    db.session.commit()

