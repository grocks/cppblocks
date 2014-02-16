testCases = [
        {
            "description" : "Angle include of header with define",
            "expected" : [
                  {
                      "filepath" : "input/01-single-angle-include.c",
                      "disabledBlocks" : [ (7,3) ]
                  }
                ],
            "input" : [ "input/01-single-angle-include.c", False, None, None, {} ]
        },
]
