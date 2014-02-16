testCases = [
        {
            "description" : "Test whitespace in front of '#'",
            "expected" : [
                  {
                      "filepath" : "input/01-nested-ifdefs.c",
                      "disabledBlocks" : [ (1,7), (13,3) ]
                  }
                ],
            "input" : [ "input/01-nested-ifdefs.c", False, None, None, {} ]
        }
]
