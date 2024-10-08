"""
Models for Product

All of the models are stored in this module
"""

import logging
from decimal import Decimal
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


class Product(db.Model):
    """
    Class that represents a Product
    """

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Numeric(scale=2), nullable=False)
    available = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Product to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logger.error("Error creating record: %s", self)
            raise DataValidationError(
                "Product with the same name already exists"
            ) from e

    def update(self):
        """
        Updates a Product in the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("ID field cannot be empty")
        # if not self.name:
        #     raise DataValidationError("Name field cannot be empty")
        if self.price is None or self.price < Decimal("0.00"):
            raise DataValidationError("Price must be a positive number")
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error updating record: %s", self)
            raise DataValidationError(e) from e

    def delete(self):
        """Removes a Product from the data store"""
        logger.info("Deleting %s", self.name)
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.error("Error deleting record: %s", self)
            raise DataValidationError(e) from e

    def serialize(self) -> dict:
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "available": self.available,
        }

    def deserialize(self, data: dict):
        """
        Deserializes a Product from a dictionary
        Args:
            data (dict): A dictionary containing the Product data
        """
        try:
            self.name = data["name"]
            self.description = data["description"]
            self.price = round(Decimal(data["price"]), 2)
            if isinstance(data["available"], bool):
                self.available = data["available"]
            else:
                raise DataValidationError(
                    "Invalid type for boolean [available]: "
                    + str(type(data["available"]))
                )
        except AttributeError as error:
            raise DataValidationError(
                "Error: Invalid attribute " + error.args[0]
            ) from error
        except KeyError as error:
            raise DataValidationError("Error: Missing " + error.args[0]) from error
        except TypeError as error:
            raise DataValidationError(
                "Error: Missing or invalid data" + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def all(cls):
        """Returns all of the Products in the database"""
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a Product by its ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        try:
            by_id = int(by_id)
        except ValueError as exc:
            raise DataValidationError(
                "Invalid ID type. ID must be an integer."
            ) from exc
        return cls.query.session.get(cls, by_id)

    @classmethod
    def find_by_name(cls, name: str) -> list:
        """Returns all Products with the given name

        Args:
            name (string): the name of the Products you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_description(cls, description: str) -> list:
        """Returns all Products with the given description

        Args:
            description (string): the description of the Products you want to match
        """
        logger.info("Processing description query for %s ...", description)
        return cls.query.filter(cls.description.ilike(f"%{description}%")).all()

    @classmethod
    def find_by_price(cls, price: Decimal) -> list:
        """Returns all Products with the given price

        Args:
            price (Decimal): the price of the Products you want to match
        """
        logger.info("Processing price query for %s ...", price)
        return cls.query.filter(cls.price == price).all()

    @classmethod
    def find_by_availability(cls, available: bool = True) -> list:
        """Returns all Products by their availability

        :param available: True for products that are available
        :type available: str

        :return: a collection of Products that are available
        :rtype: list

        """
        # if not isinstance(available, bool):
        #     raise TypeError("Invalid availability, must be of type boolean")
        logger.info("Processing available query for %s ...", available)
        return cls.query.filter(cls.available == available)
