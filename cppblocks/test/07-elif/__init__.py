testCases = [
        {
            "description" : "If-elif on constant expressions '0' and '1'",
            "expected" : {
                "input/01-if-elif-on-constant-expressions-0-and-1.c" : [ (1,2), (9,2), (15,2), (19,2), (21,2) ]
            },
            "input" : [ "input/01-if-elif-on-constant-expressions-0-and-1.c", False, [], [], {} ]
        },
        {
            "description" : "If with multiple elifs",
            "expected" : {
                "input/02-if-multiple-elifs.c" : [ (4,3), (7,3), (10,3), (13,3) ]
            },
            "input" : [ "input/02-if-multiple-elifs.c", False, [], [], {} ]
        },
        {
            "description" : "If-elif-else on constant expressions",
            "expected" : {
                "input/03-if-elif-else-with-constant-expressions.c" : [ (4,3), (7,3), (12,2), (16,2) ]
            },
            "input" : [ "input/03-if-elif-else-with-constant-expressions.c", False, [], [], {} ]
        }
]
