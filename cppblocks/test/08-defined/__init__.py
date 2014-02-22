testCases = [
        {
            "description" : "Simple if-defined SYMBOL works in true/false case",
            "expected" : {
                "input/01-simple-if-defined-expression.c" : [ (1,7), (22,4), (30,6) ]
            },
            "input" : [ "input/01-simple-if-defined-expression.c", False, [], [], {} ]
        }
]
