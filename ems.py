import mysql.connector

# Database connection
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nikita@123",  # replace 'your_password' with your MySQL root password
    database="emp"
)

#Check Employee Function

def check_employee(employee_id):
    # Query to select all rows from the employees table where id matches
    sql = 'SELECT * FROM employees WHERE id=%s'

    # Making cursor buffered to make rowcount method work properly
    cursor = con.cursor(buffered=True)
    cursor.execute(sql, (employee_id,))
    return cursor.rowcount == 1

# Add Employee Function
def add_employee():
    Id = input("Enter Employee Id: ")
    if check_employee(Id):
        print("Employee already exists. Please try again.")
        return
    
    Name = input("Enter your Name: ")
    Post = input("Enter your Post: ")
    Salary = input("Enter Employee Salary: ")


    sql = 'INSERT INTO employees (id, name, position, salary) VALUES (%s, %s, %s, %s)'
    data = (Id, Name, Post, Salary)
    cursor = con.cursor()
    try:
        cursor.execute(sql,data)
        con.commit()
        print("Employee Added Successfully")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        con.rollback()

    finally:
        cursor.close()


#REMOVE EMPLOYEE FUNCTION
def remove_employee():
    Id = input("Enter Employee Id: ")

    # Checking if Employee with given Id exists
    if not check_employee(Id):
        print("Employee does not exist. Please try again.")
        return
    
    else:
        # Query to delete employee from the employees table
        sql = 'DELETE FROM employees WHERE id=%s'
        data = (Id,)
        cursor = con.cursor()

        try:
            # Executing the SQL Query
            cursor.execute(sql, data)

            # Committing the transaction
            con.commit()
            print("Employee Removed Successfully")
        
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            con.rollback()
        
        finally:
            # Closing the cursor
            cursor.close()


# PROMOTR EMPLOYEE FUNCTION
def promote_employee():
    Id = input("Enter Employee's Id: ")

    # Checking if Employee with given Id exists
    if not check_employee(Id):
        print("Employee does not exist. Please try again.")
        return
    
    else:
        try:
            Amount = float(input("Enter increase in Salary: "))

            # Query to Fetch Salary of Employee with given Id
            sql_select = 'SELECT salary FROM employees WHERE id=%s'
            data = (Id,)
            cursor = con.cursor()

            # Executing the SQL Query
            cursor.execute(sql_select, data)

            # Fetching Salary of Employee with given Id
            current_salary = cursor.fetchone()[0]
            new_salary = current_salary + Amount

            # Query to Update Salary of Employee with given Id
            sql_update = 'UPDATE employees SET salary=%s WHERE id=%s'
            data_update = (new_salary, Id)

            # Executing the SQL Query to update salary
            cursor.execute(sql_update, data_update)

            # Committing the transaction
            con.commit()
            print("Employee Promoted Successfully")

        except (ValueError, mysql.connector.Error) as e:
            print(f"Error: {e}")
            con.rollback()

        finally:
            # Closing the cursor
            cursor.close()


#DISPLAY EMPLOYEES FUNCTION
def display_employees():
    try:
        # Query to select all rows from the employees table
        sql = 'SELECT * FROM employees'
        cursor = con.cursor()

        # Executing the SQL Query
        cursor.execute(sql)

        # Fetching all details of all the Employees
        employees = cursor.fetchall()
        for employee in employees:
            print("Employee Id : ", employee[0])
            print("Employee Name : ", employee[1])
            print("Employee Post : ", employee[2])
            print("Employee Salary : ", employee[3])
            print("------------------------------------")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Closing the cursor
        cursor.close()


#MENU FUNCTION
def menu():
    while True:
        print("\nWelcome to Employee Management Record")
        print("Press:")
        print("1 to Add Employee")
        print("2 to Remove Employee")
        print("3 to Promote Employee")
        print("4 to Display Employees")
        print("5 to Exit")
        
        # Taking choice from user
        ch = input("Enter your Choice: ")

        if ch == '1':
            add_employee()
        elif ch == '2':
            remove_employee()
        elif ch == '3':
            promote_employee()
        elif ch == '4':
            display_employees()
        elif ch == '5':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid Choice! Please try again.")

if __name__ == "__main__":
    menu()