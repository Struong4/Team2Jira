-- uncomment this to make the database
-- CREATE DATABASE Inventory;

-- USE Inventory;

-- SET SQL_SAFE_UPDATES = 0;

-- creates a table for item
CREATE TABLE IF NOT EXISTS item (
	item_id CHAR(10) NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    weight_lbs DOUBLE NOT NULL,
    price FLOAT,
    descript VARCHAR(500),
    quantity INT NOT NULL,
    quantity_limit INT,
    image_str TEXT,
    PRIMARY KEY (item_id),
    CHECK (item_id REGEXP "^\d+$" AND weight_lbs >= 0 AND price >= 0 AND quantity >= 0 AND quantity_limit >= 0)
);

-- creates a table for origin
CREATE TABLE IF NOT EXISTS origin (
	item_id CHAR(10) NOT NULL,
    origin_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (item_id, origin_name),
    FOREIGN KEY (item_id) REFERENCES item(item_id),
    CHECK (item_id REGEXP "^\d+$")
);

-- creates a table for category
CREATE TABLE IF NOT EXISTS category (
	item_id CHAR(10) NOT NULL,
    category_name VARCHAR(100) NOT NULL,
	PRIMARY KEY (item_id, category_name),
    FOREIGN KEY (item_id) REFERENCES item(item_id),
    CHECK (item_id REGEXP "^\d+$")
);

-- creates a table for staff
CREATE TABLE IF NOT EXISTS staff (
	staff_id CHAR(7) NOT NULL,
    staff_first_name VARCHAR(50) NOT NULL,
    staff_last_name VARCHAR(50) NOT NULL,
    staff_username CHAR(7) NOT NULL,
    staff_password VARCHAR(50) NOT NULL,
    PRIMARY KEY (staff_id),
    CHECK (staff_id REGEXP "^[A-Z]{2}\d{5}$" AND staff_first_name REGEXP "^[A-Z][a-z]+(?:[-' ][A-Z][a-z]+)*$" AND 
    staff_last_name REGEXP "^[A-Z][a-z]+(?:[-' ][A-Z][a-z]+)*$" and staff_username REGEXP "^[A-Z]{2}\d{5}$")
);

-- creates a table for orders
CREATE TABLE IF NOT EXISTS orders (
    item_id CHAR(10) NOT NULL,
    order_datetime DATETIME NOT NULL,
    order_quantity INT NOT NULL,
    PRIMARY KEY (item_id, order_datetime),
    FOREIGN KEY (item_id) REFERENCES item(item_id),
    CHECK (item_id REGEXP "^\d+$" AND order_quantity > 0)
);

-- creates a table for updates
CREATE TABLE IF NOT EXISTS updates(
	staff_id CHAR(7) NOT NULL,
    item_id CHAR(10) NOT NULL,
    update_datetime DATETIME NOT NULL,
    PRIMARY KEY (staff_id, item_id, update_datetime),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
    FOREIGN KEY (item_id) REFERENCES item(item_id),
    CHECK (staff_id REGEXP "^[A-Z]{2}\d{5}$" AND item_id REGEXP "^\d+$")
);

-- creates a table for restock
CREATE TABLE IF NOT EXISTS restock (
	staff_id CHAR(7) NOT NULL,
    item_id CHAR(10) NOT NULL,
    restock_datetime DATETIME NOT NULL,
    restock_quantity INT NOT NULL,
    PRIMARY KEY (staff_id, item_id, restock_datetime),
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id),
    FOREIGN KEY (item_id) REFERENCES item(item_id),
    CHECK (staff_id REGEXP "^[A-Z]{2}\d{5}$" AND item_id REGEXP "^\d+$" AND restock_quantity > 0)
);

-- declares a trigger to orders an item
CREATE TRIGGER before_order_stock
BEFORE INSERT ON orders
FOR EACH ROW
WHEN (SELECT quantity FROM item WHERE item_id = NEW.item_id) < NEW.order_quantity
BEGIN
    SELECT RAISE(ABORT, 'Not enough stock available');
END;

-- Prevents purchase if item_id does not exist
CREATE TRIGGER before_order_item
BEFORE INSERT ON orders
FOR EACH ROW
WHEN (SELECT COUNT(*) FROM item WHERE item_id = NEW.item_id) = 0
BEGIN
    SELECT RAISE(ABORT, 'Invalid item ID');
END;

-- declares a trigger after ordering an item
CREATE TRIGGER after_order
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    -- Deduct the purchased quantity from the item inventory
    UPDATE item
    SET quantity = quantity - NEW.order_quantity
    WHERE item_id = NEW.item_id;
END;

-- Prevents restock if item_id does not exist
CREATE TRIGGER before_restock_item
BEFORE INSERT ON restock
FOR EACH ROW
WHEN (SELECT COUNT(*) FROM item WHERE item_id = NEW.item_id) = 0
BEGIN
    SELECT RAISE(ABORT, 'Invalid item ID');
END;

-- Prevents restock if staff_id does not exist
CREATE TRIGGER before_restock_staff
BEFORE INSERT ON restock
FOR EACH ROW
WHEN (SELECT COUNT(*) FROM staff WHERE staff_id = NEW.staff_id) = 0
BEGIN
    SELECT RAISE(ABORT, 'Invalid staff ID');
END;

-- declares a trigger after restocking an item
 CREATE TRIGGER after_restock
 AFTER INSERT ON restock
 FOR EACH ROW
 BEGIN
     -- Deduct the purchased quantity from the item inventory
     UPDATE item
     SET quantity = quantity + NEW.restock_quantity
     WHERE item_id = NEW.item_id;
 END;
 
 -- declares a trigger that checks if an item_id exists before updating
 CREATE TRIGGER before_update_item
 BEFORE UPDATE ON item
 FOR EACH ROW
 BEGIN
     -- Check if the item_id exists in the table
     SELECT 
         CASE
             WHEN (SELECT COUNT(*) FROM item WHERE item_id = OLD.item_id) = 0 THEN
                 RAISE(ABORT, 'Item ID does not exist')
         END;
 END;
 
 -- declares a trigger that checks if an item_id exists before adding to update log
 CREATE TRIGGER before_update_log
 BEFORE INSERT ON updates
 FOR EACH ROW
 WHEN (SELECT COUNT(*) FROM item WHERE item_id = NEW.item_id) = 0
 BEGIN
     SELECT RAISE(ABORT, 'Item ID does not exist');
 END;
 
 -- Prevents update if staff_id does not exist
 CREATE TRIGGER before_update_staff
 BEFORE INSERT ON updates
 FOR EACH ROW
 WHEN (SELECT COUNT(*) FROM staff WHERE staff_id = NEW.staff_id) = 0
 BEGIN
     SELECT RAISE(ABORT, 'Invalid staff ID');
 END;