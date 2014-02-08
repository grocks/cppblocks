'''
General API functions used to implement the tests in this test suite.
'''
testCases = [
        {
            "description" : "Empty files have no disabled blocks",
            "expected" : [],
            "input" : [ "input/empty.c", False, None, None, None ]
        }
]
