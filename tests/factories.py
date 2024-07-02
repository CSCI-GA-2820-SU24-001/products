"""
Test Factory to make fake objects for testing
"""

import factory
from factory.fuzzy import FuzzyDecimal
from service.models import Product


class ProductFactory(factory.Factory):
    """Creates fake products for testing"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("word")
    description = factory.Faker("sentence", nb_words=6)
    price = FuzzyDecimal(1.0, 100.0)
