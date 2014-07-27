# CppBlocks

CppBlocks evaluates C/C++ preprocessor directives to find #if, #ifdef, #ifndef, #elif and #else blocks that are currently excluded from the compilation.

For example, in the following C code listing the line 18 is not compiled:

```
#include <stdio.h>

#define ENTER_IF 1

int main()
{

#ifdef ENTER_IF
    printf("Hello GitHub!\n");
#else
    printf("Hello world!\n");
#endif

    return 0;
}
```

CppBlocks finds such blocks. CppBlocks is split into two parts: a Python library and a Vim plugin.

The Python library implements the C/C++ preprocessor and returns a list of all such inactive blocks.

The CppBlocks library can be used in plug-ins for your favorite text editor/IDE to see all inactive blocks in your source code.

At the moment the CppBlocks project includes a Vim plugin that demonstrates the capabilities of CppBlocks.
