testCases = [
        {
            "description" : "Else on ifdef works",
            "expected" : {
                "input/01-ifdef-with-else.c" : [ (1,2), (11,2) ]
            },
            "input" : [ "input/01-ifdef-with-else.c", False, [], [], {} ]
        },
        {
            "description" : "Else on ifndef works",
            "expected" : {
                "input/02-ifndef-with-else.c" : [ (3,2), (9,2) ]
            },
            "input" : [ "input/02-ifndef-with-else.c", False, [], [], {} ]
        },
        {
            "description" : "Nested ifdef with else works",
            "expected" : {
                "input/03-nested-ifdef-with-else.c" : [ (1,2), (5,3), (20,2), (16,3)  ]
            },
            "input" : [ "input/03-nested-ifdef-with-else.c", False, [], [], {} ]
        },
        {
            "description" : "Nested ifndef with else works",
            "expected" : {
                "input/04-nested-ifndef-with-else.c" : [ (3,4), (24,4), (20,3)  ]
            },
            "input" : [ "input/04-nested-ifndef-with-else.c", False, [], [], {} ]
        },
        {
            "description" : "Nested if-else constructs work",
            "expected" : {
                "input/05-nested-if-else-constructs.c" : [ (1,10), (14,2), (23,10), (38,2), (55,10), (48,2), (77,10), (72,2)  ]
            },
            "input" : [ "input/05-nested-if-else-constructs.c", False, [], [], {} ]
        }
]
