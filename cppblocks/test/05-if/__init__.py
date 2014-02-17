testCases = [
        {
            "description" : "If on constant expressions '0' and '1'",
            "expected" : {
                "input/01-if-on-constant-expressions-0-and-1.c" : [ (5,4) ]
            },
            "input" : [ "input/01-if-on-constant-expressions-0-and-1.c", False, [], [], {} ]
        },
        {
            "description" : "If on symbols with value '0' and '1'",
            "expected" : {
                "input/02-if-on-symbols-defined-to-0-and-1.c" : [ (9,4) ]
            },
            "input" : [ "input/02-if-on-symbols-defined-to-0-and-1.c", False, [], [], {} ]
        },
        {
            "description" : "If on recursive symbols with value '0' and '1'",
            "expected" : {
                "input/03-if-on-recursive-symbols-defined-to-0-and-1.c" : [ (7,3) ]
            },
            "input" : [ "input/03-if-on-recursive-symbols-defined-to-0-and-1.c", False, [], [], {} ]
        }
]
