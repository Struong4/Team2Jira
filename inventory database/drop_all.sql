-- USE Inventory;

-- SET SQL_SAFE_UPDATES = 0;

-- drops all triggers
DROP TRIGGER IF EXISTS before_buy_stock;
DROP TRIGGER IF EXISTS before_buy_student;
DROP TRIGGER IF EXISTS before_buy_item;
DROP TRIGGER IF EXISTS after_buy;

DROP TRIGGER IF EXISTS before_restock_staff;
DROP TRIGGER IF EXISTS before_restock_item;
DROP TRIGGER IF EXISTS after_restock;

DROP TRIGGER IF EXISTS before_update_item;
DROP TRIGGER IF EXISTS before_update_log;
DROP TRIGGER IF EXISTS before_update_staff;

-- drops all tables
DROP TABLE IF EXISTS buys;
DROP TABLE IF EXISTS updates;
DROP TABLE IF EXISTS restock;

DROP TABLE IF EXISTS origin;
DROP TABLE IF EXISTS category;

DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS item;
DROP TABLE IF EXISTS staff;
