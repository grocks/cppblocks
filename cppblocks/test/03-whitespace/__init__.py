testCases = [
        {
            "description" : "Test whitespace in front of '#'",
            "expected" : [
                  {
                      "filepath" : "input/01-leading-spaces-in-front-of-sharp.c",
                      "disabledBlocks" : [ (1,7), (13,3) ]
                  }
                ],
            "input" : [ "input/01-leading-spaces-in-front-of-sharp.c", False, None, None, {} ]
        },
        {
            "description" : "Test whitespace in after '#'",
            "expected" : [
                  {
                      "filepath" : "input/02-leading-spaces-after-sharp.c",
                      "disabledBlocks" : [ (1,7), (13,3) ]
                  }
                ],
            "input" : [ "input/02-leading-spaces-after-sharp.c", False, None, None, {} ]
        }
]
