testCases = [
        {
            "description" : "Test whitespace in front of '#'",
            "expected" : {
                "input/01-leading-spaces-in-front-of-sharp.c" : [ (1,7), (13,3) ]
            },
            "input" : [ "input/01-leading-spaces-in-front-of-sharp.c", False, [], [], {} ]
        },
        {
            "description" : "Test whitespace in after '#'",
            "expected" : {
                "input/02-leading-spaces-after-sharp.c" : [ (1,7), (13,3) ]
            },
            "input" : [ "input/02-leading-spaces-after-sharp.c", False, [], [], {} ]
        }
]
