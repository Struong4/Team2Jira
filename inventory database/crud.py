import sqlite3
import re

INVENTORY = "inventory.db"
CREATE_SCRIPT = "create_all.sql"
DROP_SCRIPT = "drop_all.sql"


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
        #print(f"✅ Item '{item_name}' added successfully!")
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


# where we'll test the code to make sure it works
if __name__ == "__main__":

    # creates tables using the create_all.sql script
    runSQLScript(CREATE_SCRIPT)

    print("BEFORE TESTING ADD NEW ITEMS")
    displayAllTables()

    # normal test cases for adding items
    print(addNewItem("1111111111", "milk", 5.0, 5, 0, "a carton of milk", 0, ["walmart", "target", "h mart"], ["dairy", "white"]))
    print(addNewItem("2222222222", "orange", 1.0, 1, 0, "an orange", 0, ["walmart", "aldis"], ["fruit"]))
    print(addNewItem("3333333333", "apple", 1.0, 1, 0, "an apple", 0, ["walmart"], ["fruit", "red"]))

    # edge cases for adding items
    print(addNewItem("4444444444", "banana", 1.0, 1, 0, "an banana"))
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

    # data constraints
    print(addNewItem("000000000", "rice", 1.0, 1, 0, "a rice"))
    print(addNewItem("1111122222", "eggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg", 1, 1.0, "an sugar", 5))
    print(addNewItem("4444455555", "meat", 1, 1.0, 10, 10))
    print(addNewItem("5555566666", "beef", 1, 1.0, 10, "an beef", 5, "hello", []))
    print(addNewItem("6666677777", "blueberry", 1, 1.0, 10, "an blueberry", 5, [], "hi"))

    print("AFTER TESTING ADD NEW ITEMS")
    displayAllTables()

    # normal testing cases for removing an item
    print(removeItem("1111111111"))
    print(removeItem("2222222222"))
    print(removeItem("3333333333"))

    # edge testing cases for removing an item
    print(removeItem(4444444444))
    print(removeItem(5555555555))

    # error cases for removing an item
    print(removeItem("1111111111"))
    print(removeItem("9898989898"))
    print(removeItem("111111111"))
    print(removeItem("11111111111"))
    print(removeItem("11111111a1"))
    
    print("AFTER TESTING REMOVE ITEMS")
    displayAllTables()



    runSQLScript(DROP_SCRIPT)
    pass
