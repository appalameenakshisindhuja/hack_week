# 🛒 SQLAlchemy SQLite3 ORM Demo

This Python project demonstrates the use of **SQLAlchemy** as an Object Relational Mapper (ORM) to interact with a **SQLite3** database. It includes two tables:

- **Category** (`category_id`, `category_name`)
- **Product** (`product_id`, `product_name`, `price`, `category_id`)

The script:
- Creates the database and tables
- Populates them with sample data
- Retrieves and displays products with their prices and categories in the console

---

## 📁 Files

- `main.py` – Python script with the full SQLAlchemy logic
- `store.db` – Auto-generated SQLite3 database file (created after you run the script)

---

## ⚙️ Requirements

- Python 3.6 or higher
- SQLAlchemy

Install dependencies using:
pip install sqlalchemy

## ▶️ How to Run
Clone or download this repository
Run the script:
python conn.py

This will:
Create a local SQLite3 database (store.db)
Populate it with sample data
Print a list of products with their prices and categories



