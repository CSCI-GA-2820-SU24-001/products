"""
Test cases for Pet Model
"""

import os
import logging
from unittest import TestCase
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

    def test_create_a_resource(self):
        """It should create a Product"""
        resource = ProductFactory()
        resource.create()
        self.assertIsNotNone(resource.id)
        found = Product.all()
        self.assertEqual(len(found), 1)
        data = Product.find(resource.id)
        self.assertEqual(data.name, resource.name)

    def test_create_a_resource_with_missing_name(self):
        """It should not create a Product with missing name"""
        resource = ProductFactory()
        resource.name = None
        with self.assertRaises(DataValidationError):
            resource.create()

    def test_read_a_resource(self):
        """It should read a Product by ID"""
        resource = ProductFactory()
        resource.create()
        data = Product.find(resource.id)
        self.assertIsNotNone(data)
        self.assertEqual(data.id, resource.id)
        self.assertEqual(data.name, resource.name)

    def test_read_a_non_existent_resource(self):
        """It should not read a non-existent Product"""
        data = Product.find(0)
        self.assertIsNone(data)

    def test_update_a_resource(self):
        """It should update a Product"""
        resource = ProductFactory()
        resource.create()
        original_id = resource.id
        resource.name = "Updated Name"
        resource.update()
        updated = Product.find(original_id)
        self.assertEqual(updated.name, "Updated Name")

    def test_update_a_resource_with_invalid_data(self):
        """It should not update a Product with invalid data"""
        resource = ProductFactory()
        resource.create()
        resource.name = None
        with self.assertRaises(DataValidationError):
            resource.update()

    def test_delete_a_resource(self):
        """It should delete a Product"""
        resource = ProductFactory()
        resource.create()
        resource.delete()
        data = Product.find(resource.id)
        self.assertIsNone(data)

    def test_delete_a_non_existent_resource(self):
        """It should not delete a non-existent Product"""
        resource = ProductFactory()
        resource.id = 0
        with self.assertRaises(DataValidationError):
            resource.delete()

    def test_list_all_resources(self):
        """It should list all Products"""
        resources = [ProductFactory() for _ in range(5)]
        for resource in resources:
            resource.create()
        found = Product.all()
        self.assertEqual(len(found), 5)
