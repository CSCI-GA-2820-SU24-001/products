"""
This module contains functions and classes for performing various testings.
It provides functionality for:
- Product model test cases
- model testing functions
"""

import os
import logging
from unittest import TestCase
from decimal import Decimal
from wsgi import app
from service.models import Product, DataValidationError, db
from .factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Product   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
# pylint: disable=duplicate-code
class TestProduct(TestCase):
    """Test Cases for Product Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should create a Product and assert that it exists"""
        product = Product(
            name="Test Product",
            description="A test product",
            price=Decimal("10.00"),
            available=True,
        )

        self.assertIsNone(product.id)
        product.create()
        self.assertIsNotNone(product.id)
        self.assertTrue(product is not None)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "A test product")
        self.assertEqual(product.price, Decimal("10.00"))
        self.assertEqual(product.available, True)

    def test_read_a_product(self):
        """It should read a Product"""
        product = ProductFactory()
        product.create()
        found_product = Product.find(product.id)
        self.assertIsNotNone(found_product)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)
        self.assertEqual(found_product.available, product.available)

    def test_update_a_product(self):
        """It should update a Product"""
        product = ProductFactory()
        product.create()
        self.assertIsNotNone(product.id)
        product.description = "Updated description"
        product.update()
        updated_product = Product.find(product.id)
        self.assertEqual(updated_product.description, "Updated description")

    def test_delete_a_product(self):
        """It should delete a Product"""
        product = ProductFactory()
        product.create()
        self.assertIsNotNone(product.id)
        product.delete()
        found_product = Product.find(product.id)
        self.assertIsNone(found_product)
    
    def test_update_product_with_negative_price(self):
        """It should not update a Product with a negative price"""
        product = ProductFactory()
        product.create()
        self.assertIsNotNone(product.id)
        product.price = Decimal("-10.00")
        with self.assertRaises(DataValidationError):
            product.update()

    def test_serialize_a_product(self):
        """It should serialize a Product"""
        product = ProductFactory()
        data = product.serialize()
        self.assertEqual(data["id"], product.id)
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["description"], product.description)
        self.assertEqual(data["price"], str(product.price))
        self.assertEqual(data["available"], product.available)

    def test_deserialize_a_product(self):
        """It should deserialize a Product"""
        data = {
            "name": "Test Product",
            "description": "A test product",
            "price": "10.00",
            "available": True,
        }
        product = Product()
        product.deserialize(data)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.description, "A test product")
        self.assertEqual(product.price, Decimal("10.00"))
        self.assertEqual(product.available, True)

    def test_deserialize_with_key_error(self):
        """It should not deserialize a Product with a KeyError"""
        data = {"name": "Test Product", "price": "10.00"}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_with_type_error(self):
        """It should not deserialize a Product with a TypeError"""
        data = "this is not a dictionary"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_update_invalid_id(self):
        """It should not update a Product with an invalid ID"""
        product = ProductFactory()
        product.id = None
        product.description = "New description"
        self.assertRaises(DataValidationError, product.update)

    def test_delete_invalid_product(self):
        """It should not delete a Product that does not exist"""
        product = ProductFactory()
        self.assertRaises(DataValidationError, product.delete)

    def test_deserialize_empty_data(self):
        """It should not deserialize a Product with empty data"""
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, {})

    def test_find_all_products(self):
        """It should return all products"""
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()
        all_products = Product.all()
        self.assertEqual(len(all_products), 3)

    def test_find_by_name(self):
        """It should find a product by name"""
        product = ProductFactory()
        product.create()
        found_products = Product.find_by_name(product.name)
        self.assertEqual(found_products.first().id, product.id)
        self.assertEqual(found_products.first().name, product.name)

    def test_find_by_id_not_found(self):
        """It should not find a Product with a non-existing ID"""
        product = ProductFactory()
        product.create()
        found_product = Product.find(0)  # Assuming 0 is not a valid ID
        self.assertIsNone(found_product)

    def test_datavalidationerror_exception(self):
        """It should raise a DataValidationError"""
        with self.assertRaises(DataValidationError):
            raise DataValidationError("This is a test error")

    def test_create_with_missing_data(self):
        """It should not create a Product with missing data"""
        product = Product(
            name=None, description="A test product", price=Decimal("10.00")
        )
        with self.assertRaises(DataValidationError):
            product.create()

    def test_serialize_with_special_characters(self):
        """It should serialize a Product with special characters"""
        product = Product(
            name="Special!@#$%^&*()_+-=~`[]{}|;:'\",<.>/?",
            description="Description with special characters !@#$%^&*()",
            price=Decimal("10.00"),
            available=True,
        )
        data = product.serialize()
        self.assertEqual(data["name"], "Special!@#$%^&*()_+-=~`[]{}|;:'\",<.>/?")
        self.assertEqual(
            data["description"], "Description with special characters !@#$%^&*()"
        )

    def test_all_method_with_no_products(self):
        """It should return an empty list when no products are present"""
        all_products = Product.all()
        self.assertEqual(len(all_products), 0)

    def test_find_by_name_no_match(self):
        """It should return an empty list when no products match the name"""
        found_products = Product.find_by_name("Non-existent name")
        self.assertEqual(found_products.count(), 0)

    def test_find_with_invalid_id_type(self):
        """It should not find a Product with an invalid ID type"""
        with self.assertRaises(DataValidationError):
            Product.find("invalid_id")

    def test_find_by_description(self):
        """It should Find a Product by Description"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        description = products[0].description
        count = len(
            [product for product in products if description in product.description]
        )
        found = Product.find_by_description(description)
        self.assertEqual(len(found), count)
        for product in found:
            self.assertIn(description, product.description)

    def test_find_by_price(self):
        """It should Find a Product by Price"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        price = products[0].price
        count = len([product for product in products if product.price == price])
        found = Product.find_by_price(price)
        self.assertEqual(len(found), count)
        for product in found:
            self.assertEqual(product.price, price)

    def test_find_by_availability(self):
        """It should Find Products by Availability"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        available = products[0].available
        count = len([product for product in products if product.available == available])
        found = Product.find_by_availability(available)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.available, available)

    def test_deserialize_bad_available(self):
        """It should not deserialize a bad available attribute"""
        test_product = ProductFactory()
        data = test_product.serialize()
        data["available"] = "true"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)
