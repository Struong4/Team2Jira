import sqlite3
import re
from datetime import datetime
import time
from random import randint

INVENTORY = "inventory.db"
CREATE_SCRIPT = "create_all.sql"
DROP_SCRIPT = "drop_all.sql"

ID_REG_EXP = "^[A-Z]{2}\d{5}$"

def createInventory():
    runSQLScript(CREATE_SCRIPT)

def resetInventory():
    runSQLScript(DROP_SCRIPT)


# Custom REGEXP function for SQLite
def regexp(expr, item):
    """Apply regular expression matching."""
    if item is None:
        return False
    reg = re.compile(expr)
    return reg.search(item) is not None

def runSQLScript(sql_file):

    # opens the sql script to be read
    with open(sql_file, "r") as f:
        sql_script = f.read()

    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # Register REGEXP function
    conn.create_function("REGEXP", 2, regexp)

    cursor = conn.cursor()

    # Use executescript to handle multi-line SQL statements properly
    cursor.executescript(sql_script)

    conn.commit()
    conn.close()
    print(f"Executed {sql_file} on {INVENTORY}")


def addNewItem(item_id, item_name, weight_lbs, quantity=0, price=0.00, descript="", quantity_limit=0, origins=[], categories=[]):
    prompt = ""

    item_id = str(item_id)

    # checks if the origins is a list 
    if not isinstance(origins, list):
        return f"⚠️ Unable to add {item_name}. Origins must be a list of origin names"
    if not isinstance(categories, list):
        return f"⚠️ Unable to add {item_name}. Categories must be a list of category names"
    if len(item_id) != 10:
        return f"⚠️ Unable to add {item_name}. Item id must be 10-digits"
    if not isinstance(descript, str):
        return f"⚠️ Unable to add {item_name}. Description must be a string of at most 500 characters"

    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    # Register REGEXP function
    conn.create_function("REGEXP", 2, regexp)

    try:
        # adds the item
        cursor.execute("""
            INSERT INTO item (item_id, item_name, weight_lbs, price, descript, quantity, quantity_limit) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (item_id, item_name, weight_lbs, price, descript, quantity, quantity_limit))

        # iterates through all places of origin
        for origin in origins:

            # adds the origin associated with the item
            cursor.execute("""
                INSERT INTO origin (item_id, origin_name) 
                VALUES (?, ?)
            """, (item_id, origin))

        # iterates through all places of categories
        for category in categories:

            # adds the category associated with the item
            cursor.execute("""
                INSERT INTO category (item_id, category_name) 
                VALUES (?, ?)
            """, (item_id, category))

        conn.commit()
        prompt = f"✅ Item '{item_name}' added successfully!"

    except sqlite3.IntegrityError as e:
        #print(f"❌ Error: {e}")
        if "UNIQUE constraint failed" in str(e):
            prompt = f"⚠️ Unable to add {item_name}. Item ID '{item_id}' already exists in the database!"
        elif "CHECK constraint failed" in str(e):

            # checks the different check contraints
            if not item_id.isdigit():
                prompt = f"⚠️ Unable to add {item_name}. Item ID must be a unique 10-digit code"
            elif weight_lbs < 0:
                prompt = f"⚠️ Unable to add {item_name}. Weight must be greater than 0"
            elif quantity < 0:
                prompt = f"⚠️ Unable to add {item_name}. Quantity must be greater than 0"
            elif quantity_limit < 0:
                prompt = f"⚠️ Unable to add {item_name}. Quantity limit must be greater than 0"
            elif price < 0:
                prompt = f"⚠️ Unable to update {item_name}. Price must be greater than 0"

    finally:
        cursor.close()
        conn.close()
    return prompt

def removeItem(item_id):
    item_id = str(item_id)
    if len(item_id) != 10:
        return f"⚠️ Unable to remove item {item_id}. Item ID must be a unique 10-digit code"
    if not item_id.isdigit():
        return f"⚠️ Unable to remove item {item_id}. Item ID must be a unique 10-digit code"

    prompt = ""
    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    # checks if the item still exists
    query = f"SELECT COUNT(*) FROM item WHERE item_id = ?"
    cursor.execute(query, (item_id,))
    count = cursor.fetchone()[0]

    if count == 1:

        # removes the item
        cursor.execute("""
            DELETE FROM item WHERE item_id = ?
        """, (item_id,))

        # removes category associated with the item
        cursor.execute("""
            DELETE FROM category WHERE item_id = ?
        """, (item_id,))

        # removes origin associated with the item
        cursor.execute("""
            DELETE FROM origin WHERE item_id = ?
        """, (item_id,))

        prompt = f"✅ Item '{item_id}' successfully removed!"
    else:
        # displays if item has already been removed
        prompt = f"⚠️ Unable to remove item {item_id}. Item ID {item_id} doesn't exist"

    conn.commit()

    # closes the cursor
    cursor.close()

    # closes the connection
    conn.close()

    return prompt

def displayAllTables():
    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    print("DISPLAYING ALL TABLES")

    tables = ["student", "item", "origin", "category", "staff", "buys", "updates", "restock"]

    for table in tables:
        print(f"TABLE: {table.upper()}")
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()
        
        if rows:
            for row in rows:
                print(row)
        else:
            print("No records found.")
        
        print("\n" + "-" * 40 + "\n")

    # closes the cursor and connection
    cursor.close()
    conn.close()

def buyItem(student_id, item_id, buy_datetime, buy_quantity):
    prompt = ""

    if datetime.strptime(buy_datetime, "%Y-%m-%d %H:%M:%S") > datetime.now():
        return f"⚠️ Unable to buy item {item_id}. Invalid datetime of {buy_datetime}" 

    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    # Register REGEXP function
    conn.create_function("REGEXP", 2, regexp)

    try:
        # executes the buy command
        cursor.execute("""
            INSERT INTO buys (student_id, item_id, buy_datetime, buy_quantity)
            VALUES (?, ?, ?, ?)
        """, (student_id, item_id, buy_datetime, buy_quantity,))
    
        conn.commit()

        prompt = f"✅ Item '{item_id}' bought by student {student_id}. Bought {buy_quantity} items!"
    except sqlite3.IntegrityError as e:
        if "CHECK constraint failed" in str(e):
            # no need
            if buy_quantity < 1:
                prompt = f"⚠️ Unable to buy item {item_id}. Invalid buy_quantity of {buy_quantity}" 
        else:
            prompt = f"⚠️ Unable to buy item {item_id}. {e}" 
    finally:
        # closes the cursor and connection
        cursor.close()
        conn.close()

    return prompt

def restockItem(staff_id, item_id, restock_datetime, restock_quantity):
    prompt = ""

    if datetime.strptime(restock_datetime, "%Y-%m-%d %H:%M:%S") > datetime.now():
        return f"⚠️ Unable to restock item {item_id}. Invalid datetime of {restock_datetime}" 


    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    # Register REGEXP function
    conn.create_function("REGEXP", 2, regexp)

    try:
        # executes the buy command
        cursor.execute("""
            INSERT INTO restock (staff_id, item_id, restock_datetime, restock_quantity)
            VALUES (?, ?, ?, ?)
        """, (staff_id, item_id, restock_datetime, restock_quantity,))
    
        conn.commit()

        prompt = f"✅ Item '{item_id}' restocked by staff {staff_id}. Restocked {restock_quantity} items!"
    except sqlite3.IntegrityError as e:
        if "CHECK constraint failed" in str(e):
            if restock_quantity < 1:
                prompt = f"⚠️ Unable to restock item {item_id}. Invalid restock_quantity of {restock_quantity}" 
        else:
            prompt = f"⚠️ Unable to restock item {item_id}. {e}" 
    finally:
        # closes the cursor and connection
        cursor.close()
        conn.close()

    return prompt

def updateItem(staff_id, item_id, update_datetime, item_name, weight_lbs, quantity=0, price=0.00, descript="", quantity_limit=0, origins=[], categories=[]):
    prompt = ""

    item_id = str(item_id)

    # checks for valid datetime
    if datetime.strptime(update_datetime, "%Y-%m-%d %H:%M:%S") > datetime.now():
        return f"⚠️ Unable to update item {item_name}. Invalid datetime of {update_datetime}"

    # checks if the origins is a list 
    if not isinstance(origins, list):
        return f"⚠️ Unable to update {item_name}. Origins must be a list of origin names"
    if not isinstance(categories, list):
        return f"⚠️ Unable to update {item_name}. Categories must be a list of category names"
    if len(item_id) != 10:
        return f"⚠️ Unable to update {item_name}. Item id must be 10-digits"
    if not isinstance(descript, str):
        return f"⚠️ Unable to update {item_name}. Description must be a string of at most 500 characters"

    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    # Register REGEXP function
    conn.create_function("REGEXP", 2, regexp)

    try:
        # updates the item
        # adds the item
        cursor.execute("""
            UPDATE item
            SET 
                       item_name = ?,
                       weight_lbs = ?,
                       price = ?,
                       descript = ?,
                       quantity = ?,
                       quantity_limit = ?
            WHERE item_id = ?
        """, (item_name, weight_lbs, price, descript, quantity, quantity_limit, item_id,))

        # adds item to update log
        cursor.execute("""
            INSERT INTO updates (staff_id, item_id, update_datetime) 
            VALUES (?, ?, ?)
        """, (staff_id, item_id, update_datetime))

        # removes all the origins connected to item id before
        cursor.execute("""
            DELETE FROM origin WHERE item_id = ?
        """, (item_id,))

        # iterates through all places of origin
        for origin in origins:

            # adds the origin associated with the item
            cursor.execute("""
                INSERT INTO origin (item_id, origin_name) 
                VALUES (?, ?)
            """, (item_id, origin))

        # removes all the categories connected to item id before
        cursor.execute("""
            DELETE FROM category WHERE item_id = ?
        """, (item_id,))

        # iterates through all places of categories
        for category in categories:

            # adds the category associated with the item
            cursor.execute("""
                INSERT INTO category (item_id, category_name) 
                VALUES (?, ?)
            """, (item_id, category))

        conn.commit()
        prompt = f"✅ Item '{item_name}' successfully! updated"

    except sqlite3.IntegrityError as e:
        #print(f"❌ Error: {e}")
        if "UNIQUE constraint failed" in str(e):
            prompt = f"⚠️ Unable to update {item_name}. Item ID '{item_id}' already exists in the database!"
        elif "CHECK constraint failed" in str(e):

            # checks the different check contraints
            if not item_id.isdigit():
                prompt = f"⚠️ Unable to update {item_name}. Item ID must be a unique 10-digit code"
            elif weight_lbs < 0:
                prompt = f"⚠️ Unable to update {item_name}. Weight must be greater than 0"
            elif quantity < 0:
                prompt = f"⚠️ Unable to update {item_name}. Quantity must be greater than 0"
            elif quantity_limit < 0:
                prompt = f"⚠️ Unable to update {item_name}. Quantity limit must be greater than 0"
            elif price < 0:
                prompt = f"⚠️ Unable to update {item_name}. Price must be greater than 0"
        else:
            prompt = f"⚠️ Unable to update item {item_name}. {e}"

    finally:
        cursor.close()
        conn.close()
    return prompt

def showInventory():
    # declares and initializes variables
    inventory = {}

    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    # gets all the items in the inventory
    cursor.execute(f"SELECT * FROM item")
    rows = cursor.fetchall()

    # iterates through all the items and stores them in a dictionary
    for row in rows:
        item_id = row[0]
        item_name = row[1]
        weight_lbs = row[2]
        price = row[3]
        descript = row[4]
        quantity = row[5]
        quantity_limit = row[6]

        inventory[item_id] = {"Item name": item_name, "Weight": weight_lbs, "Price": price, "Description": descript, "Quantity": quantity, "Quantity Limit": quantity_limit}

    cursor.close()
    conn.close()

    # inventory is in dictionary format
    return inventory

def showHistory():
    # declares and initializes variables
    transactions = []

    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    #tables = ["buys", "restock", "updates"]
    tables = {"buys": "BUY", "restock": "RESTOCK", "updates": "UPDATE"}

    for table in tables:
    # gets all buy transactions
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        for row in rows:
            transaction = {
                'Transaction Type': tables[table],
                'Person ID': row[0],
                'Item ID': row[1],
                'Datetime': row[2]
            }

            if table == "buys" or table == "restock":
                transaction["Quantity"] = row[3]
            transactions.append(transaction)

    cursor.close()
    conn.close()

    return transactions
    
def addNewStudent(student_id, student_first_name, student_last_name):

    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    # Register REGEXP function
    conn.create_function("REGEXP", 2, regexp)

    # executes the buy command
    cursor.execute("""
        INSERT INTO student (student_id, student_first_name, student_last_name)
        VALUES (?, ?, ?)
    """, (student_id, student_first_name, student_last_name,))

    conn.commit()

    # closes the cursor and connection
    cursor.close()
    conn.close()

def addNewStaff(staff_id, staff_first_name, staff_last_name):

    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    # Register REGEXP function
    conn.create_function("REGEXP", 2, regexp)

    # executes the buy command
    cursor.execute("""
        INSERT INTO staff (staff_id, staff_first_name, staff_last_name)
        VALUES (?, ?, ?)
    """, (staff_id, staff_first_name, staff_last_name,))

    conn.commit()

    # closes the cursor and connection
    cursor.close()
    conn.close()
    

# where we'll test the code to make sure it works
if __name__ == "__main__":

    # creates tables using the create_all.sql script
    resetInventory()
    createInventory()

    print("BEFORE TESTING ADD NEW ITEMS")
    displayAllTables()

    # normal test cases for adding items
    print(addNewItem("1111111111", "milk", 5.0, 10, 10, "a carton of milk", 0, ["walmart", "target", "h mart"], ["dairy", "white"]))
    print(addNewItem("2222222222", "orange", 1.0, 10, 10, "an orange", 0, ["walmart", "aldis"], ["fruit"]))
    print(addNewItem("3333333333", "apple", 1.0, 10, 10, "an apple", 0, ["walmart"], ["fruit", "red"]))

    # edge cases for adding items
    print(addNewItem("4444444444", "banana", 1.0, 10, 10, "an banana"))
    print(addNewItem(5555555555, "chicken", 1.0, 1, 0, "an chicken"))
    print(addNewItem(6666666666, "pork", 1.0, 1, 0, "an pork"))

    # error cases for adding items
    # unique constraints
    print(addNewItem("4444444444", "cereal", 1.0, 1, 0, "an cereal"))

    # check contraints
    print(addNewItem("7777777777", "yogurt", -1.0, 1, 0, "an yogurt"))
    print(addNewItem("8888888888", "sugar", 1.0, -1, 0, "an sugar"))
    print(addNewItem("9999a99999", "salt", 1.0, 1, 0, "an salt"))
    print(addNewItem("9999999999", "sugar", 1.0, -1, 0, "an sugar"))
    print(addNewItem("9999999999", "sugar", 1.0, 1, -5, "an sugar"))

    # data constraints
    print(addNewItem("000000000", "rice", 1.0, 1, 0, "a rice"))
    print(addNewItem("1111122222", "eggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg", 1, 1.0, "an sugar", 5))
    print(addNewItem("4444455555", "meat", 1, 1.0, 10, 10))
    print(addNewItem("5555566666", "beef", 1, 1.0, 10, "an beef", 5, "hello", []))
    print(addNewItem("6666677777", "blueberry", 1, 1.0, 10, "an blueberry", 5, [], "hi"))

    print("AFTER TESTING ADD NEW ITEMS")
    displayAllTables()

    print("TESTING SHOW HISTORY")
    addNewStaff("AB12345", "Your", "Mom")
    addNewStudent("GB70937", "Gia", "Santos")

    print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "almond milk", 6.0, 5, 5, "a carton of almond milk", 3, ["walmart", "target", "h mart"], ["dairy", "white"]))
    time.sleep(randint(1,5))
    print(restockItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))
    time.sleep(randint(1,5))
    print(buyItem("GB70937", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))
    time.sleep(randint(1,5))
    print(updateItem("AB12345", "2222222222", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "tangerine", 1.5, 20, 10, "a tangerine", 20, ["walmart", "aldis"], ["fruit"]))
    time.sleep(randint(1,5))
    print(updateItem("AB12345", "3333333333", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "cherry", 0.5, 20, 0.5, "a cherry", 10, ["walmart"], ["fruit", "red"]))
    time.sleep(randint(1,5))
    print(buyItem("GB70937", "2222222222", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 5))
    time.sleep(randint(1,5))
    print(updateItem("AB12345", '4444444444', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'banana', 1.0, 50, 10.0, 'a banana', 10, ['h mart', 'lotte mart'], ["yellow", "tropical"]))
    time.sleep(randint(1,5))
    print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "almond milk", 6.0, 5, 5, "a carton of almond milk", 3, ["aldis", "giant"], ["dairy", "white"]))
    time.sleep(randint(1,5))
    print(restockItem("AB12345", "2222222222", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))
    time.sleep(randint(1,5))
    print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "almond milk", 6.0, 5, 5, "a carton of almond milk", 3, ["aldis", "giant"], ["cow"]))
    time.sleep(randint(1,5))
    print(restockItem("AB12345", "3333333333", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))
    time.sleep(randint(1,5))
    print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "almond milk", 6.0, 5, 5, "a carton of almond milk", 3))
    time.sleep(randint(1,5))
    print(buyItem("GB70937", "3333333333", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 10))

    print("HISTORY")
    transactions = showHistory()
    for transaction in transactions:
        print(transaction)

    # print("INVENTORY")
    # inventory = showInventory()

    # for item in inventory:
    #     print(item, inventory[item])
    

    # print("TESTING UPDATE ITMES")
    # addNewStaff("AB12345", "Your", "Mom")

    # # normal case
    # print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "almond milk", 6.0, 5, 5, "a carton of almond milk", 3, ["walmart", "target", "h mart"], ["dairy", "white"]))
    # print(updateItem("AB12345", "2222222222", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "tangerine", 1.5, 1, 10, "a tangerine", 4, ["walmart", "aldis"], ["fruit"]))
    # print(updateItem("AB12345", "3333333333", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "cherry", 0.5, 20, 0.5, "a cherry", 10, ["walmart"], ["fruit", "red"]))

    # # edge case: add origins and categories
    # print(updateItem("AB12345", '4444444444', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'banana', 1.0, 50, 10.0, 'a banana', 10, ['h mart', 'lotte mart'], ["yellow", "tropical"]))
    # displayAllTables()

    # time.sleep(5)
    # # edge case: change origins
    # print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "almond milk", 6.0, 5, 5, "a carton of almond milk", 3, ["aldis", "giant"], ["dairy", "white"]))
    # displayAllTables()

    # time.sleep(5)
    # # edge case: change categories
    # print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "almond milk", 6.0, 5, 5, "a carton of almond milk", 3, ["aldis", "giant"], ["cow"]))
    # displayAllTables()

    # time.sleep(5)
    # # edge case: no origins and categories
    # print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "almond milk", 6.0, 5, 5, "a carton of almond milk", 3))
    # displayAllTables()

    # time.sleep(5)
    # # error case: invalid item ID format
    # print(updateItem("AB12345", "11111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "whole milk", 6.0, 5, 5, "a carton of whole milk", 3))
    # print(updateItem("AB12345", "11aa1a1a11", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "whole milk", 6.0, 5, 5, "a carton of whole milk", 3))

    # # error case: nonexisting item ID
    # print(updateItem("AB12345", "9999999999", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "whole milk", 6.0, 5, 5, "a carton of whole milk", 3))

    # # error case: invalid quantity
    # print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "whole milk", 6.0, -5, 5, "a carton of whole milk", 3))

    # # error case: invalid price
    # print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "whole milk", 6.0, 5, -5, "a carton of whole milk", 3))

    # # error case: datetime > now
    # print(updateItem("AB12345", "1111111111", "2030-04-03  12:00:00", "whole milk", 6.0, 5, 5, "a carton of whole milk", 3))

    # # error case invalid weight
    # print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "whole milk", -6.0, 5, 5, "a carton of whole milk", 3))

    # # error case: invalid quantity limit
    # print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "whole milk", 6.0, 5, 5, "a carton of whole milk", -3))

    # # error case: nonexistent staff ID
    # print(updateItem("GB70937", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "whole milk", 6.0, 5, 5, "a carton of whole milk", 3))


    # # error case: incorrect staff ID format
    # print(updateItem("12ABCDE", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "whole milk", 6.0, 5, 5, "a carton of whole milk", 3))



    # print("TESTING RESTOCK ITMES")
    # addNewStaff("AB12345", "Your", "Mom")

    # # normal test cases for restocking items
    # print(restockItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))
    # print(restockItem("AB12345", "2222222222", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))
    # print(restockItem("AB12345", "3333333333", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))

    # # edge case: restocking 0 items
    # print(restockItem("AB12345", "4444444444", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0))

    # # error case: invalid staff id
    # print(restockItem("12ABCD", "4444444444", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))

    # # error case: nonexistent staff id
    # print(restockItem("CD12345", "4444444444", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))

    # # error case: invalid item id
    # print(restockItem("AB12345", "aaaaaaaaaa", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))
    # print(restockItem("AB12345", "22222222", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))

    # # error case: nonexistent item id
    # print(restockItem("AB12345", "9999999999", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))

    # # error case: invalid restock quantity
    # print(restockItem("AB12345", "4444444444", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), -10))

    # # edge case: restocking datetime before now
    # print(restockItem("AB12345", "4444444444", "2001-04-03  12:00:00", 10))

    # # edge case: restocking datetime before now
    # print(restockItem("AB12345", "5555555555", "2030-04-03  12:00:00", 10))

    # # edge case: restocking same item from same staff
    # print(restockItem("AB12345", "1111111111", "2001-04-03  12:00:00", 10))






    # print("TESTING BUY ITEMS")
    # addNewStudent("GB70937", "Gia", "Santos")

    # # normal case for buying items
    # print(buyItem("GB70937", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))
    # print(buyItem("GB70937", "2222222222", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 5))
    # print(buyItem("GB70937", "3333333333", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 10))

    # # edge case: no more stock
    # print(buyItem("GB70937", "3333333333", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))

    # # edge case: buying 0 items
    # print(buyItem("GB70937", "5555555555", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0))

    # # error case: invalid student id
    # print(buyItem("12ABCDE", "4444444444", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))

    # # error case: nonexistent student id
    # print(buyItem("AB12345", "4444444444", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))

    # # error case: invalid item id
    # print(buyItem("GB70937", "444444444", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))

    # # error case: invalid item id
    # print(buyItem("GB70937", "8888888888", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))

    # # error case: invalid item id
    # print(buyItem("GB70937", "4444444444", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), -5))

    # # edge case: buying item at a past datetime
    # print(buyItem("GB70937", "4444444444", "2001-04-03  12:00:00", 1))

    # # error case: buying items at a future datetime than now
    # print(buyItem("GB70937", "5555555555", "2030-04-03  12:00:00", 1))
    




    # normal testing cases for removing an item
    # print(removeItem("1111111111"))
    # print(removeItem("2222222222"))
    # print(removeItem("3333333333"))

    # # edge testing cases for removing an item
    # print(removeItem(4444444444))
    # print(removeItem(5555555555))

    # # error cases for removing an item
    # print(removeItem("1111111111"))
    # print(removeItem("9898989898"))
    # print(removeItem("111111111"))
    # print(removeItem("11111111111"))
    # print(removeItem("11111111a1"))
    
    # print("AFTER TESTING REMOVE ITEMS")

    #displayAllTables()

    



    #runSQLScript(DROP_SCRIPT)
    
