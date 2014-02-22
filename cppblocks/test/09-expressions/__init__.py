testCases = [
        {
            "description" : "Equality/inequality/negation on constants",
            "expected" : {
                "input/01-in-equality-negation-on-constants.c" : [ (5,8), (13,5), (18,6), (40,5), (45,6), (53,2), (59,1) ]
            },
            "input" : [ "input/01-in-equality-negation-on-constants.c", False, [], [], {} ]
        },
        {
            "description" : "Parenthesized basic expressions work",
            "expected" : {
                "input/02-parenthesized-expressions.c" : [ (9,5), (19,3), (22,3), (25,2), (35,4), (39,4) ]
            },
            "input" : [ "input/02-parenthesized-expressions.c", False, [], [], {} ]
        }
]
