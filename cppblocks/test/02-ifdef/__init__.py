testCases = [
        {
            "description" : "Define and ifdef in same file works",
            "expected" : [
                  {
                      "filepath" : "input/01-true-and-false-ifdef.c",
                      "disabledBlocks" : [ (7,3) ]
                  }
                ],
            "input" : [ "input/01-true-and-false-ifdef.c", False, None, None, {} ]
        },
        {
            "description" : "Define and ifndef in same file works",
            "expected" : [
                  {
                      "filepath" : "input/02-true-and-false-ifndef.c",
                      "disabledBlocks" : [ (3,3) ]
                  }
                ],
            "input" : [ "input/02-true-and-false-ifndef.c", False, None, None, {} ]
        },
        {
            "description" : "Nested ifdefs in same file work",
            "expected" : [
                  {
                      "filepath" : "input/03-nested-ifdefs.c",
                      "disabledBlocks" : [ (1,7), (13,3) ]
                  }
                ],
            "input" : [ "input/03-nested-ifdefs.c", False, None, None, {} ]
        },
        {
            "description" : "Nested ifdefs with predefines work",
            "expected" : [
                  {
                      "filepath" : "input/03-nested-ifdefs.c",
                      "disabledBlocks" : [ (1,7) ]
                  }
                ],
            "input" : [ "input/03-nested-ifdefs.c", False, None, None, { 'BAR' : None } ]
        },
        {
            "description" : "Nested ifdefs with undef works",
            "expected" : [
                  {
                      "filepath" : "input/04-ifdef-with-undef.c",
                      "disabledBlocks" : [ (9,3), (17,3) ]
                  }
                ],
            "input" : [ "input/04-ifdef-with-undef.c", False, None, None, {} ]
        }
]
