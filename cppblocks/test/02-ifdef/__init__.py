testCases = [
        {
            "description" : "Define and ifdef in same file works",
            "expected" : {
                "input/01-true-and-false-ifdef.c" : [ (7,3) ]
            },
            "input" : [ "input/01-true-and-false-ifdef.c", False, [], [], {} ]
        },
        {
            "description" : "Define and ifndef in same file works",
            "expected" : {
                "input/02-true-and-false-ifndef.c" : [ (3,3) ]
            },
            "input" : [ "input/02-true-and-false-ifndef.c", False, [], [], {} ]
        },
        {
            "description" : "Nested ifdefs in same file work",
            "expected" : {
                "input/03-nested-ifdefs.c" : [ (1,7), (13,3) ]
            },
            "input" : [ "input/03-nested-ifdefs.c", False, [], [], {} ]
        },
        {
            "description" : "Nested ifdefs with predefines work",
            "expected" : {
                "input/03-nested-ifdefs.c" : [ (1,7) ]
            },
            "input" : [ "input/03-nested-ifdefs.c", False, [], [], { 'BAR' : None } ]
        },
        {
            "description" : "Nested ifdefs with undef works",
            "expected" : {
                "input/04-ifdef-with-undef.c" : [ (9,3), (17,3) ]
            },
            "input" : [ "input/04-ifdef-with-undef.c", False, [], [], {} ]
        }
]
