-- uncomment this to make the database
-- CREATE DATABASE Inventory;

-- USE Inventory;

-- SET SQL_SAFE_UPDATES = 0;

-- creates a table for student
CREATE TABLE IF NOT EXISTS student (
	student_id CHAR(7) NOT NULL,
    student_first_name VARCHAR(50) NOT NULL,
    student_last_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (student_id),
    CHECK (student_id REGEXP "^[A-Z]{2}\d{5}$" AND student_first_name REGEXP "^[A-Z][a-z]+(?:[-' ][A-Z][a-z]+)*$" AND 
    student_last_name REGEXP "^[A-Z][a-z]+(?:[-' ][A-Z][a-z]+)*$")
);

-- creates a table for item
CREATE TABLE IF NOT EXISTS item (
	item_id CHAR(10) NOT NULL,
    item_name VARCHAR(100) NOT NULL,
    weight_lbs DOUBLE NOT NULL,
    price FLOAT,
    descript VARCHAR(500),
    quantity INT NOT NULL,
    quantity_limit INT,
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
    PRIMARY KEY (staff_id),
    CHECK (staff_id REGEXP "^[A-Z]{2}\d{5}$" AND staff_first_name REGEXP "^[A-Z][a-z]+(?:[-' ][A-Z][a-z]+)*$" AND 
    staff_last_name REGEXP "^[A-Z][a-z]+(?:[-' ][A-Z][a-z]+)*$")
);

-- creates a table for buys
CREATE TABLE IF NOT EXISTS buys (
	student_id CHAR(7) NOT NULL,
    item_id CHAR(10) NOT NULL,
    buy_datetime DATETIME NOT NULL,
    buy_quantity INT NOT NULL,
    PRIMARY KEY (student_id, item_id, buy_datetime),
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (item_id) REFERENCES item(item_id),
    CHECK (student_id REGEXP "^[A-Z]{2}\d{5}$" AND item_id REGEXP "^\d+$" AND buy_quantity > 0)
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
