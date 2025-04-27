import sqlite3
import re
from datetime import datetime
import time
from random import randint
import random
import string

INVENTORY = "inventory.db"
CREATE_SCRIPT = "create_all.sql"
DROP_SCRIPT = "drop_all.sql"

ID_REG_EXP = r"^[A-Z]{2}\d{5}$"
NAME_PATTERN = r"^[A-Z][a-z]+(?:[-' ][A-Z][a-z]+)*$"

def createInventory(create_script):
    runSQLScript(create_script)

def resetInventory(drop_script):
    runSQLScript(drop_script)


# Custom REGEXP function for SQLite
def regexp(expr, item):
    """Apply regular expression matching."""
    if item is None:
        return False
    return re.fullmatch(expr, item) is not None


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


def addNewItem(item_id, item_name, weight_lbs, quantity=0, price=0.00, descript="", quantity_limit=0, origins=[], categories=[], image_str=""):
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
            INSERT INTO item (item_id, item_name, weight_lbs, price, descript, quantity, quantity_limit, image_str) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (item_id, item_name, weight_lbs, price, descript, quantity, quantity_limit, image_str,))

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

    tables = ["item", "origin", "category", "staff", "orders", "updates", "restock"]

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

def buyItem(item_id, order_datetime, order_quantity):
    prompt = ""

    if datetime.strptime(order_datetime, "%Y-%m-%d %H:%M:%S") > datetime.now():
        return f"⚠️ Unable to buy item {item_id}. Invalid datetime of {order_datetime}" 

    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    # Register REGEXP function
    conn.create_function("REGEXP", 2, regexp)

    try:
        # executes the buy command
        cursor.execute("""
            INSERT INTO orders (item_id, order_datetime, order_quantity)
            VALUES (?, ?, ?)
        """, (item_id, order_datetime, order_quantity,))

        conn.commit()

        prompt = f"✅ {order_quantity} Item(s) '{item_id}' have been bought"
    except sqlite3.IntegrityError as e:
        if "CHECK constraint failed" in str(e):
            # no need
            if order_quantity < 1:
                prompt = f"⚠️ Unable to buy item {item_id}. Invalid buy_quantity of {order_quantity}" 
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

def updateItem(staff_id, item_id, update_datetime, item_name, weight_lbs, quantity=0, price=0.00, descript="", quantity_limit=0, origins=[], categories=[], image_str=""):
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
                    quantity_limit = ?,
                    image_str = ?
            WHERE item_id = ?
        """, (item_name, weight_lbs, price, descript, quantity, quantity_limit, image_str, item_id,))

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

def showInventory(origins=[], categories=[]):
    # declares and initializes variables
    inventory = {}

    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    # query for filtering out items of specific origins and categories
    query = """
        SELECT i.item_id, i.item_name, i.weight_lbs, i.price, i.descript,
               i.quantity, i.quantity_limit
        FROM item i
        LEFT JOIN origin o ON i.item_id = o.item_id
        LEFT JOIN category c ON i.item_id = c.item_id
    """
    conditions = []
    params = []

    # add filters if provided
    if origins:
        placeholders = ",".join("?" for _ in origins)
        conditions.append(f"o.origin_name IN ({placeholders})")
        params.extend(origins)

    if categories:
        placeholders = ",".join("?" for _ in categories)
        conditions.append(f"c.category_name IN ({placeholders})")
        params.extend(categories)

    # append WHERE clause if needed
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    for row in rows:
        item_id, item_name, weight_lbs, price, descript, quantity, quantity_limit = row
        inventory[item_id] = {
            "Item name": item_name,
            "Weight": weight_lbs,
            "Price": price,
            "Description": descript,
            "Quantity": quantity,
            "Quantity Limit": quantity_limit
        }

    cursor.close()
    conn.close()

    return inventory

def showHistory():
    # declares and initializes variables
    transactions = []

    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    #tables = ["buys", "restock", "updates"]
    tables = {"orders": "ORDER", "restock": "RESTOCK", "updates": "UPDATE"}

    for table in tables:
    # gets all buy transactions
        cursor.execute(f"SELECT * FROM {table}")
        rows = cursor.fetchall()

        for row in rows:

            if table == "orders":

                transaction = {
                    'Transaction Type': tables[table],
                    'Item ID': row[0],
                    'Datetime': row[1],
                    'Quantity': row[2]
                }
            elif table == "updates":
                
                transaction = {
                    'Transaction Type': tables[table],
                    'Staff ID': row[0],
                    'Item ID': row[1],
                    'Datetime': row[2]
                }
            elif table == "restock":

                transaction = {
                    'Transaction Type': tables[table],
                    'Staff ID': row[0],
                    'Item ID': row[1],
                    'Datetime': row[2],
                    'Quantity': row[3]
                }

            transactions.append(transaction)

    cursor.close()
    conn.close()

    return transactions

def addNewStaff(staff_id, staff_first_name, staff_last_name, staff_username, staff_password):
    prompt = ""

    # checks for check constraints
    if not re.fullmatch(ID_REG_EXP, staff_id):
        return f"❌ Invalid staff ID '{staff_id}'. Must match format: 2 uppercase letters followed by 5 digits."
    elif not re.fullmatch(ID_REG_EXP, staff_username):
        return f"❌ Invalid staff username '{staff_username}'. Must match format: 2 uppercase letters followed by 5 digits."
    elif not re.fullmatch(NAME_PATTERN, staff_first_name):
        return f"❌ Invalid staff first name '{staff_first_name}'."
    elif not re.fullmatch(NAME_PATTERN, staff_last_name):
        return f"❌ Invalid staff last name '{staff_last_name}'."

    # establishes a connection with the sql database
    conn = sqlite3.connect(INVENTORY)

    # gets the sql cursor
    cursor = conn.cursor()

    # Register REGEXP function
    conn.create_function("REGEXP", 2, regexp)

    try:
        # executes the add staff command
        #print(f"about to add staff {staff_id}")
        cursor.execute("""
            INSERT INTO staff (staff_id, staff_first_name, staff_last_name, staff_username, staff_password)
            VALUES (?, ?, ?, ?, ?)
        """, (staff_id, staff_first_name, staff_last_name, staff_username, staff_password))

        conn.commit()

        #print("added a staff")

        prompt = f"✅ Staff '{staff_id}' successfully added!"

    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            prompt = f"⚠️ Unable to add staff {staff_id}. Staff ID '{staff_id}' already exists in the database!"
        else:
            prompt = f"⚠️ Unable to add staff {staff_id}. {e}"
    
    finally:
        # closes the cursor and connection
        cursor.close()
        conn.close()

    return prompt

def simulateAddingRandomItems(num_items=50):
    item_names = ["Milk", "Orange", "Apple", "Banana", "Chicken", "Rice", "Beef", "Yogurt", "Cereal", "Pork", "Bread", "Cheese", "Butter", "Fish", "Tomato", "Lettuce", "Spinach", "Grapes", "Watermelon", "Strawberry"]
    origins_list = ["Walmart", "Target", "H Mart", "Aldi", "Costco", "Trader Joe's", "Whole Foods", "Safeway", "Kroger"]
    categories_list = ["Dairy", "Fruit", "Meat", "Vegetable", "Grain", "Beverage", "Snack", "Frozen", "Condiment", "Seafood"]

    for _ in range(num_items):
        # Create a random 10-digit item ID
        item_id = "".join(random.choices(string.digits, k=10))

        # Randomly choose an item name or create a new random one
        item_name = random.choice(item_names) + ''.join(random.choices(string.ascii_lowercase, k=3))

        # Generate random weight between 0.5 and 20 lbs
        weight = round(random.uniform(0.5, 20.0), 2)

        # Generate random quantity between 1 and 100
        quantity = random.randint(1, 100)

        # Generate random price between 1 and 100 dollars
        price = round(random.uniform(1.0, 100.0), 2)

        # Randomly select origins (1 to 3 random ones)
        origins = random.sample(origins_list, random.randint(1, 3))

        # Randomly select categories (1 to 2 random ones)
        categories = random.sample(categories_list, random.randint(1, 2))

        # Small description
        description = f"A random {item_name.lower()}."

        # Random quantity limit
        quantity_limit = random.randint(0, 50)

        # Optional: dummy image string
        image_str = ""

        result = addNewItem(item_id, item_name, weight, quantity, price, description, quantity_limit, origins, categories, image_str)
        print(result)



# where we'll test the code to make sure it works
if __name__ == "__main__":

    # creates tables using the create_all.sql script
    resetInventory(DROP_SCRIPT)
    createInventory(CREATE_SCRIPT)

    print("BEFORE TESTING ADD NEW ITEMS")
    displayAllTables()

    simulateAddingRandomItems(100)
    #showInventory()

    print("INVENTORY")
    inventory = showInventory()

    for item in inventory:
        print(item, inventory[item])

    # print("TESTING ADD STAFF")
    # # testing normal case for add staff
    # print(addNewStaff("GB70937", "Gia", "Santos", "GB70937", "password"))
    # print(addNewStaff("AB12345", "Olive", "Santos", "AB12345", "123pass"))
    # print(addNewStaff("CD67890", "Manuel", "Santos", "CD67890", "pass1234"))

    # # error case duplicate staff ID
    # print(addNewStaff("GB70937", "John", "Doe", "GB70937", "password"))

    # # error case invalid staff ID
    # print(addNewStaff("12ABCDE", "John", "Doe", "GB70937", "password"))

    # # error case invalid staff username
    # print(addNewStaff("GB70937", "John", "Doe", "12ABCDE", "password"))

    # # error case invalid staff first name
    # print(addNewStaff("GB70937", "1234princess", "Doe", "GB70937", "password"))

    # # error case invalid staff last name
    # print(addNewStaff("GB70937", "John", "1234princess", "GB70937", "password"))

    # displayAllTables()

    # normal test cases for adding items
    # print(addNewItem("1111111111", "milk", 5.0, 10, 10, "a carton of milk", 0, ["walmart", "target", "h mart"], ["dairy", "white"]))
    # print(addNewItem("2222222222", "orange", 1.0, 10, 10, "an orange", 0, ["walmart", "aldis"], ["fruit"]))
    # print(addNewItem("3333333333", "apple", 1.0, 10, 10, "an apple", 0, ["walmart"], ["fruit", "red"]))

    # # edge cases for adding items
    # print(addNewItem("4444444444", "banana", 1.0, 10, 10, "an banana"))
    # print(addNewItem(5555555555, "chicken", 1.0, 1, 0, "an chicken"))
    # print(addNewItem(6666666666, "pork", 1.0, 1, 0, "an pork"))

    # # error cases for adding items
    # # unique constraints
    # print(addNewItem("4444444444", "cereal", 1.0, 1, 0, "an cereal"))

    # # check contraints
    # print(addNewItem("7777777777", "yogurt", -1.0, 1, 0, "an yogurt"))
    # print(addNewItem("8888888888", "sugar", 1.0, -1, 0, "an sugar"))
    # print(addNewItem("9999a99999", "salt", 1.0, 1, 0, "an salt"))
    # print(addNewItem("9999999999", "sugar", 1.0, -1, 0, "an sugar"))
    # print(addNewItem("9999999999", "sugar", 1.0, 1, -5, "an sugar"))

    # # data constraints
    # print(addNewItem("000000000", "rice", 1.0, 1, 0, "a rice"))
    # print(addNewItem("1111122222", "eggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg", 1, 1.0, "an sugar", 5))
    # print(addNewItem("4444455555", "meat", 1, 1.0, 10, 10))
    # print(addNewItem("5555566666", "beef", 1, 1.0, 10, "an beef", 5, "hello", []))
    # print(addNewItem("6666677777", "blueberry", 1, 1.0, 10, "an blueberry", 5, [], "hi"))

    # print("AFTER TESTING ADD NEW ITEMS")
    # displayAllTables()

    # print("INVENTORY")
    # inventory = showInventory()

    # for item in inventory:
    #     print(item, inventory[item])
    # print("TESTING SHOW HISTORY")
    # addNewStaff("AB12345", "Your", "Mom")

    # print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "almond milk", 6.0, 5, 5, "a carton of almond milk", 3, ["walmart", "target", "h mart"], ["dairy", "white"]))
    # time.sleep(randint(1,5))
    # print(restockItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))
    # time.sleep(randint(1,5))
    # print(buyItem("1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))
    # time.sleep(randint(1,5))
    # print(updateItem("AB12345", "2222222222", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "tangerine", 1.5, 20, 10, "a tangerine", 20, ["walmart", "aldis"], ["fruit"]))
    # time.sleep(randint(1,5))
    # print(updateItem("AB12345", "3333333333", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "cherry", 0.5, 20, 0.5, "a cherry", 10, ["walmart"], ["fruit", "red"]))
    # time.sleep(randint(1,5))
    # print(buyItem("2222222222", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 5))
    # time.sleep(randint(1,5))
    # print(updateItem("AB12345", '4444444444', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'banana', 1.0, 50, 10.0, 'a banana', 10, ['h mart', 'lotte mart'], ["yellow", "tropical"]))
    # time.sleep(randint(1,5))
    # print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "almond milk", 6.0, 5, 5, "a carton of almond milk", 3, ["aldis", "giant"], ["dairy", "white"]))
    # time.sleep(randint(1,5))
    # print(restockItem("AB12345", "2222222222", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))
    # time.sleep(randint(1,5))
    # print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "almond milk", 6.0, 5, 5, "a carton of almond milk", 3, ["aldis", "giant"], ["cow"]))
    # time.sleep(randint(1,5))
    # print(restockItem("AB12345", "3333333333", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 20))
    # time.sleep(randint(1,5))
    # print(updateItem("AB12345", "1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "almond milk", 6.0, 5, 5, "a carton of almond milk", 3))
    # time.sleep(randint(1,5))
    # print(buyItem("3333333333", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 10))

    # print("HISTORY")
    # transactions = showHistory()
    # for transaction in transactions:
    #     print(transaction)

    # print("INVENTORY")
    # inventory = showInventory()

    # for item in inventory:
    #     print(item, inventory[item])
    

    # print("TESTING UPDATE ITMES")
    # addNewStaff("AB12345", "Your", "Mom", "AB12345", "password")

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

    # displayAllTables()

    # print("ENTIRE INVENTORY")
    # inventory = showInventory()

    # for item in inventory:
    #     print(item, inventory[item])

    # print("FILTER ALDIS AND WALMART")
    # inventory = showInventory(origins=['aldis', 'walmart'])
    # for item in inventory:
    #     print(item, inventory[item])

    # print("FILTER FRUIT AND TROPICAL")
    # inventory = showInventory(categories=['fruit', 'tropical'])
    # for item in inventory:
    #     print(item, inventory[item])

    # print("FILTER FRUIT AND HMART")
    # inventory = showInventory(origins=['h mart'], categories=['fruit'])
    # for item in inventory:
    #     print(item, inventory[item])

    # print("NONEXISTING ORIGINS AND CATEGORIES")
    # inventory = showInventory(origins=['weis'], categories=['meat'])
    # for item in inventory:
    #     print(item, inventory[item])



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

    # # normal case for buying items
    # print(buyItem("1111111111", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))
    # print(buyItem("2222222222", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 5))
    # print(buyItem("3333333333", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 10))

    # # edge case: no more stock
    # print(buyItem("3333333333", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))

    # # edge case: buying 0 items
    # print(buyItem("5555555555", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0))

    # # error case: invalid student id
    # print(buyItem("4444444444", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))

    # # error case: nonexistent student id
    # print(buyItem("4444444444", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))

    # # error case: invalid item id
    # print(buyItem("444444444", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))

    # # error case: invalid item id
    # print(buyItem("8888888888", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1))

    # # error case: invalid item id
    # print(buyItem("4444444444", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), -5))

    # # edge case: buying item at a past datetime
    # print(buyItem("4444444444", "2001-04-03  12:00:00", 1))

    # # error case: buying items at a future datetime than now
    # print(buyItem("5555555555", "2030-04-03  12:00:00", 1))





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