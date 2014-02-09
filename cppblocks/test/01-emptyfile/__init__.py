testCases = [
        {
            "description" : "Empty files have no disabled blocks",
            "expected" : [
                  {
                      "filepath" : "input/empty.c",
                      "disabledBlocks" : []
                  }
                ],
            "input" : [ "input/empty.c", False, None, None, [] ]
        }
]
