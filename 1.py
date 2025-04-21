import psycopg2
import csv

# --- PhoneBook System ---

def create_phonebook_table():
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="0419",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            phone_number VARCHAR(15) UNIQUE
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_contact():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone_number = input("Enter phone number: ")

    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="0419",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s)", 
                (first_name, last_name, phone_number))
    conn.commit()
    cur.close()
    conn.close()    

def update_contact():
    phone_number = input("Enter the phone number to update: ")
    new_first_name = input("Enter new first name: ")
    new_phone_number = input("Enter new phone number: ")

    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="0419",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("UPDATE phonebook SET first_name = %s, phone_number = %s WHERE phone_number = %s", 
                (new_first_name, new_phone_number, phone_number))
    conn.commit()
    cur.close()
    conn.close()

def search_contacts():
    search_term = input("Enter search term (first name, last name, phone number): ")

    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="0419",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE first_name LIKE %s OR last_name LIKE %s OR phone_number LIKE %s",
                ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close() 
    conn.close()

def delete_contact():
    phone_number = input("Enter the phone number to delete: ")

    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="0419",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE phone_number = %s", (phone_number,))
    conn.commit()
    cur.close()
    conn.close()

# --- CSV Data Upload to Database ---

def load_data_from_csv(csv_file):
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="0419",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Open the CSV file and read it
    with open(csv_file, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header row if it exists

        for row in csv_reader:
            first_name, last_name, phone_number = row
            # Insert data into the phonebook table
            cur.execute("INSERT INTO phonebook (first_name, last_name, phone_number) VALUES (%s, %s, %s)",
                        (first_name, last_name, phone_number))

    conn.commit()
    cur.close()
    conn.close()

# --- View All Records from PhoneBook Table ---

def view_all_contacts():
    conn = psycopg2.connect(
        database="postgres",
        user="postgres",
        password="0419",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    if rows:
        print("PhoneBook Records:")
        for row in rows:
            print(f"ID: {row[0]}, First Name: {row[1]}, Last Name: {row[2]}, Phone Number: {row[3]}")
    else:
        print("No records found.")
    cur.close()
    conn.close()    

# --- Main Program Flow ---

def main():
    create_phonebook_table()

    while True:
        print("\nPhoneBook System:")
        print("1. Add Contact")
        print("2. Update Contact")
        print("3. Search Contacts")
        print("4. Delete Contact")
        print("5. Load Data from CSV")
        print("6. View All Contacts")
        print("7. Exit PhoneBook System")
        choice = input("Choose an option: ")

        if choice == '1':
            add_contact()
        elif choice == '2':
            update_contact()
        elif choice == '3':
            search_contacts()
        elif choice == '4':
            delete_contact()
        elif choice == '5':
            csv_file = input("Enter the path to the CSV file: ")
            load_data_from_csv(csv_file)
        elif choice == '6':
            view_all_contacts()
        elif choice == '7':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
