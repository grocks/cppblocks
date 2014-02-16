testCases = [
        {
            "description" : "Empty files have no disabled blocks",
            "expected" : {
                "input/empty.c" : []
            },
            "input" : [ "input/empty.c", False, [], [], {} ]
        }
]
