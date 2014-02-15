testCases = [
        {
            "description" : "Define and ifdef in same file works",
            "expected" : [
                  {
                      "filepath" : "input/01-true-and-false-ifdef.c",
                      "disabledBlocks" : [ (7,3) ]
                  }
                ],
            "input" : [ "input/01-true-and-false-ifdef.c", False, None, None, [] ]
        },
        {
            "description" : "Define and ifndef in same file works",
            "expected" : [
                  {
                      "filepath" : "input/02-true-and-false-ifndef.c",
                      "disabledBlocks" : [ (3,3) ]
                  }
                ],
            "input" : [ "input/02-true-and-false-ifndef.c", False, None, None, [] ]
        },
        {
            "description" : "Nested ifdefs in same file work",
            "expected" : [
                  {
                      "filepath" : "input/03-nested-ifdefs.c",
                      "disabledBlocks" : [ (1,7), (13,3) ]
                  }
                ],
            "input" : [ "input/03-nested-ifdefs.c", False, None, None, [] ]
        }
]
