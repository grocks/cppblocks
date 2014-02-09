testCases = [
        {
            "description" : "Define and ifdef in same file works",
            "expected" : [
                  {
                      "filepath" : "input/main.c",
                      "disabledBlocks" : [ (7,3) ]
                  }
                ],
            "input" : [ "input/main.c", False, None, None, [] ]
        }
]
