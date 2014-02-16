testCases = [
        {
            "description" : "Angle include of header with define",
            "expected" : {
                "input/01-single-angle-include.c" : [ (7,3) ]
            },
            "input" : [ "input/01-single-angle-include.c", False, [ 'input' ], [], {} ]
        },
        {
            "description" : "Quote include of header in same directory with define",
            "expected" : {
                "input/02-single-quote-include.c" : [ (7,3) ]
            },
            "input" : [ "input/02-single-quote-include.c", False, [], [], {} ]
        }
]
