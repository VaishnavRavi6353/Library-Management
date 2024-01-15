import pandas as pd

# Function to register a new user
def register_user(username, password):
    users_df = pd.read_csv("D:\\Projects\\Library Management\\users.csv")
    
    # Check if the username is already taken
    if username in users_df.username.values:  
        print("Username already exists. Please choose another username.")
        return False

    # Get the maximum user_id and increment it for the new user
    new_user_id = users_df['user_id'].max() + 1 if not users_df.empty else 1

    # Add the new user to the DataFrame
    new_user = pd.DataFrame({'user_id': [new_user_id], 'username': [username], 'password': [password]})
    users_df = pd.concat([users_df, new_user], ignore_index=True)

    # Update the csv file
    users_df.to_csv("D:\\Projects\\Library Management\\users.csv", index=False)

    print("Registration successful.")
    return True

# Function to authenticate a user
def login_user(username, password):
    users_df = pd.read_csv("D:\\Projects\\Library Management\\users.csv")

    # Check if the username and password match
    user = users_df[(users_df.username == username) & (users_df.password == int(password))]

    print(user)
    if not user.empty:
        return user.iloc[0].user_id
    
    else:
        return None

# Function for borrowing a book
def borrow_book(user_id, book_id):
    BookData_df = pd.read_csv("D:\\Projects\\Library Management\\BookData.csv")

    # Borrow book if available
    if ((BookData_df.availability > 0) & (BookData_df.unique_id == book_id)).any():  
        BookData_df.loc[BookData_df.unique_id == book_id, 'availability'] -= 1
        price = BookData_df.loc[BookData_df.unique_id == book_id, 'price'].values[0]  
        print(f"Price to pay until the book is returned is ${price}.")
        print("Book is Available & Borrowed successfully...")
    else:
        print("Book is not Available.")
    
    # Update the csv file
    BookData_df.to_csv("D:\\Projects\\Library Management\\BookData.csv", index=False)

# Function to return a book
def return_book(user_id, book_id):
    BookData_df = pd.read_csv("D:\\Projects\\Library Management\\BookData.csv")

    # Collect Book and return money
    try:
        BookData_df.loc[BookData_df.unique_id == book_id, 'availability'] += 1
        price = BookData_df.loc[BookData_df.unique_id == book_id, 'price'].values[0]
        print(f"Collect your money ${price}.")
        print("Book is returned successfully...")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Update the csv file
    BookData_df.to_csv("D:\\Projects\\Library Management\\BookData.csv", index=False)

# Main Program
print("Library Management System")

while True:
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        register_user(username, password)

    elif choice == "2":
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        user_id = login_user(username, password)
        
        if user_id:
            print(f"Login successful! User ID: {user_id}")

            # Library Services
            while True:
                print("1. Borrow a book")
                print("2. Return a book")
                print("3. Logout")
                choice = input("Enter your choice: ")

                if choice == "1":
                    book_id = input("Enter the book ID to borrow: ")
                    borrow_book(user_id, book_id)

                elif choice == "2":
                    book_id = input("Enter the book ID to return: ")
                    return_book(user_id, book_id)

                elif choice == "3":
                    print("Logging out...")
                    break

                else:
                    print("Invalid choice. Try again.")

        else:
            print("Login failed. Invalid credentials.")

    elif choice=='3':
        break
    else:
        print("Invalid choice. Try again.")
