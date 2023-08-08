import unittest
import json
import os
from schema_builder.schema_builder import SchemaBuilder
class TestData(unittest.TestCase):
    """ Test the schema extraction """
    
    def setUp(self) -> None:
        return super().setUp()
    
    def test_data(self):
        """ Test that the schema is valid """
        
        data_file = 'tests/data/data_1.json'
        test_schema_file = 'tests/schema/schema_1.json'
        new_schema_file =  SchemaBuilder().extract(data_file)
        test_schema = {}
        new_schema = {}
        with open(test_schema_file, 'r') as f1, \
            open(new_schema_file, 'r') as f2:
            test_schema = json.load(f1)
            new_schema = json.load(f2)
        self.assertEqual(new_schema, test_schema)