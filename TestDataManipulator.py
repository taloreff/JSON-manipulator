import unittest
import json
from pathlib import Path
from DataManipulator import DataManipulator


class TestDataManipulator(unittest.TestCase):
    
    test_dict ={
        "value1": "1999/10/10 10:15:15",
	    "value2": '''abcd sklakf    qwerty  
        blablabla       sss''',
	    "value3": [
		"bar", "baz", "foo", "bar", "baz", 5
	    ],
	    "value4": "1997/10/10 10:15:15z",
     	"value5": "1999-10-10 12:15:15",
        "value6": "10/10/1997 10:15:15",
        "value7": 10
    }
    
    expected_data = {
            "value1": "2021/10/10 10:15:15",
            "value2": "sssalbalbalbytrewqfkalksdcba",
            "value3": ["bar","baz","foo",5],
            "value4": "2021/10/10 10:15:15+0000"
        }
    
    test_file = Path("test.json")
    with test_file.open("w") as file:
        json.dump(test_dict, file, indent=2)
    
    def test_manipulate(self):
        dm = DataManipulator(self.test_file)
        dm.manipulate()
        self.assertEqual(dm.data, self.expected_data)
        
    def test_save(self):
        dm = DataManipulator(self.test_file)
        dm.manipulate()
        dm.save(Path("test_output.json"))
        with open(Path("test_output.json")) as file:
            output_data = json.load(file)
        self.assertEqual(output_data, self.expected_data)
    
    def test_e2e(self):
        dm = DataManipulator(self.test_file)
        dm.manipulate()
        dm.save(Path("test_output.json"))
        with open(Path("test_output.json")) as file:
            output_data = json.load(file)
        self.assertEqual(output_data, self.expected_data)
        
    def test_input(self):
        bad_input_file = Path("bad_input.json")
        with bad_input_file.open("w") as file:
            file.write('{"key1": "value1","key2": }')
        dm = DataManipulator(bad_input_file)
        