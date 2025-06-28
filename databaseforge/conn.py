from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

# Define the SQLite database
engine = create_engine("sqlite:///store.db", echo=True)

# Base class for models
Base = declarative_base()

# Define Category Table
class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)

    # One-to-many relationship
    products = relationship("Product", back_populates="category")

# Define Product Table
class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'))

    # Relationship back to category
    category = relationship("Category", back_populates="products")

# Create tables in the database
Base.metadata.create_all(engine)

# Populate tables
with Session(engine) as session:
    # Add categories
    electronics = Category(category_name="Electronics")
    groceries = Category(category_name="Groceries")
    fashion = Category(category_name="Fashion")

    session.add_all([electronics, groceries, fashion])
    session.flush()  # To assign IDs before using them below

    # Add products
    products = [
        Product(product_name="Laptop", price=75000, category_id=electronics.category_id),
        Product(product_name="Smartphone", price=30000, category_id=electronics.category_id),
        Product(product_name="Rice", price=1200, category_id=groceries.category_id),
        Product(product_name="T-Shirt", price=499, category_id=fashion.category_id),
    ]
    session.add_all(products)
    session.commit()

# Retrieve and display data
with Session(engine) as session:
    results = session.query(Product).join(Category).all()
    print("\n--- Product List ---")
    for product in results:
        print(f"Product: {product.product_name}, Price: ₹{product.price}, Category: {product.category.category_name}")
