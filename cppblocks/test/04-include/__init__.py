testCases = [
        {
            "description" : "Angle include of header with define",
            "expected" : {
                "input/01-single-angle-include.c" : [ (7,3) ],
                "input/01-single-define.h": []
            },
            "input" : [ "input/01-single-angle-include.c", True, [ 'input' ], [], {} ]
        },
        {
            "description" : "Quote include of header in same directory with define",
            "expected" : {
                "input/02-single-quote-include.c" : [ (7,3) ],
                "input/01-single-define.h": []
            },
            "input" : [ "input/02-single-quote-include.c", True, [], [], {} ]
        }
]
