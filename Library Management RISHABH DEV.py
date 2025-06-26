#SOURCE CODE

# MySql Connectivity
import mysql.connector

mydb = mysql.connector.connect(host='localhost', user='root', passwd='98766')
mycursor = mydb.cursor()

# Welcome Screen

print('''
-----------------------------------------------------------------
           WELCOME TO LIBRARY MANAGEMENT SYSTEM
-----------------------------------------------------------------
''')

# Creating Database

mycursor.execute("create database if not exists library_2")
mycursor.execute("use library_2")
mycursor.execute("create table if not exists available_books(id int, name varchar(25), subject varchar(25), quantity int)")
mycursor.execute("create table if not exists issued(id int, name varchar(25), subject varchar(25), s_name varchar(25), s_class varchar(25))")
mydb.commit()


# Functions

# Main Menu
def display_menu():
    print("""
-----------------------------------------------------------------
    1. Add New Books
    2. Remove Books (Complete Set)
    3. Remove N Books (Reduce Quantity by N)
    4. Add N Books (Increase Quantity by N)
    5. Issue Book To Student
    6. Return Book
    7. View Available Books
    8. View Issued Books
    9. Find Book with Maximum Quantity
    10. Find Book with Minimum Quantity
    11. Exit
-----------------------------------------------------------------    
    """)


# 1. Add A Set Of Book

def add_new_book():
    loop1 = 'y'
    while loop1 == 'y':
        print('All information is mandatory to be filled')
        idd = int(input('Enter Book ID (Numeric Value): '))
        name = input('Enter Book Name: ')
        subject = input('Enter Subject: ')
        quan = int(input('Enter Quantity: '))
        mycursor.execute(f"insert into available_books values({idd}, '{name}', '{subject}', {quan})")
        mydb.commit()
        print("""
>>>>>>>>>>>> Data Inserted Successfully....""")
        loop1 = input('Do You Want To Add Another Book? (y/n) ').lower()


# 2. Remove A Set Of Book

def remove_book():
    idd = int(input('Enter ID To Remove Book (Numeric Value): '))
    mycursor.execute(f"delete from available_books where id={idd}")
    mydb.commit()
    print("""
>>>>>>>>>>>> Data Successfully Deleted....""")


# 3. Remove n No Of Books

def remove_n_books():
    idd = int(input('Enter Book ID (Numeric Value): '))
    n = int(input('Enter the number of books to remove: '))
    mycursor.execute(f"update available_books set quantity=quantity-{n} where id={idd} and quantity >= {n}")
    mydb.commit()
    print(f"""
>>>>>>>>>>>> {n} books Successfully Removed....""")


# 4. Add n books

def add_n_books():
    idd = int(input('Enter Book ID (Numeric Value): '))
    n = int(input('Enter the number of books to add: '))
    mycursor.execute(f"update available_books set quantity=quantity+{n} where id={idd}")
    mydb.commit()

    print(f"""
>>>>>>>>>>>> {n} books Successfully Added....""")


# 5. Issue Book To A Student

def issue_book():
    loop1 = 'y'
    while loop1 == "y":
        print('All information is mandatory to be filled')
        idd = int(input('Enter Book ID (Numeric Value): '))
        s_name = input('Enter Student Name: ')
        s_class = input('Enter Student Class: ')
        mycursor.execute(f"select * from available_books where id={idd}")
        result = mycursor.fetchone()

        if result:
            t_id_available, t_name, t_subject, t_quan = result

            if t_quan > 0:
                mycursor.execute(f"insert into issued values({idd}, '{t_name}', '{t_subject}', '{s_name}', '{s_class}')")
                mycursor.execute(f"update available_books set quantity=quantity-1 where id={idd}")
                mydb.commit()
                print("""
>>>>>>>>>>>> Book Successfully Issued.....""")
            else:
                print("""
>>>>>>>>>>>> Book Not Available (Quantity is 0)....""")
        else:
            print("""
>>>>>>>>>>>> No Book Is Available With Input Book ID....""")
        loop1 = input('Do You Want To Issue More Books? (y/n) ').lower()


# 6. Return Book

def return_book():
    loop1='y'
    while loop1=='y':
        idd = int(input('Enter Book ID (Numeric Value): '))
        s_name = input('Enter Student Name: ')
        s_class = input('Enter Student Class: ')
        mycursor.execute(f"select * from issued where id={idd} and s_name='{s_name}' and s_class='{s_class}'")
        result = mycursor.fetchone()

        if result:
            mycursor.execute(f"select * from available_books where id={idd}")
            result_available = mycursor.fetchone()

            if result_available:
                t_id,t_name,t_subject,t_quan=result_available
                quan=t_quan+1
                mycursor.execute(f"delete from issued where id={idd} and s_name='{s_name}' and s_class='{s_class}'")
                mycursor.execute(f"update available_books set quantity={quan} where id={idd}")
                mydb.commit()
                print("""
>>>>>>>>>>>> Book Successfully Returned....""")
            else:
                print("""
>>>>>>>>>>>> Error: No Book Found in Available Books....""")
        else:
            print("""
>>>>>>>>>>>> Book Not Issued....""")
        loop1=input('Do You Wnat To Return More Book? (y/n) ').lower()


# 7. Show Available Books

def show_available_books():
    mycursor.execute("select * from available_books")
    print("ID | NAME | SUBJECT | QUANTITY")

    for i in mycursor:
        a,b,c,d=i
        print(f"{a} | {b} | {c} | {d}")


# 8. Show Issued Books

def show_issued_books():
    mycursor.execute("select * from issued")
    print("ID | NAME | SUBJECT | S_NAME | S_CLASS")

    for i in mycursor:
        a2,b2,c2,d2,e2=i
        print(f"{a2} | {b2} | {c2} | {d2} | {e2}")


# 9. Function to find the book with maximum quantity

def find_max_quantity_book():
    mycursor.execute("SELECT * FROM available_books ORDER BY quantity DESC LIMIT 1")
    result = mycursor.fetchone()
    if result:
        book_id, book_name, book_subject, book_quantity = result
        print(f"The book with the maximum quantity is:")
        print(f"ID: {book_id}, Name: {book_name}, Subject: {book_subject}, Quantity: {book_quantity}")
    else:
        print("No books available.")


# 10. Function to find the book with minimum quantity

def find_min_quantity_book():
    mycursor.execute("SELECT * FROM available_books ORDER BY quantity ASC LIMIT 1")
    result = mycursor.fetchone()
    if result:
        book_id, book_name, book_subject, book_quantity = result
        print(f"The book with the minimum quantity is:")
        print(f"ID: {book_id}, Name: {book_name}, Subject: {book_subject}, Quantity: {book_quantity}")
    else:
        print("No books available.")


# 11. Exit Function

def exit_program():
    global mydb
    mydb.close()
    print("Exiting the program.")
    exit()


# Main

while True:
    display_menu()
    ch = int(input("Enter your choice: "))

    if ch == 1:
        add_new_book()
    
    elif ch == 2:
        remove_book()
    
    elif ch == 3:
        remove_n_books()
    
    elif ch == 4:
        add_n_books()
    
    elif ch == 5:
        issue_book()
    
    elif ch == 6:
        return_book()
    
    elif ch == 7:
        show_available_books()
    
    elif ch == 8:
        show_issued_books()
    
    elif ch == 9:
        find_max_quantity_book()
    
    elif ch == 10:
        find_min_quantity_book()
  
    elif ch == 11:
        exit_program()
