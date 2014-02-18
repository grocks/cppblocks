#if 0
    int a = 1;

    #if 0
        int b = 1;
    #else
        int c = 1;
    #endif

    int d = 1;
#else
    int a = 2;

    #if 0
        int b = 2;
    #else
        int c = 2;
    #endif

    int d = 2;
#endif

#if 0
    int a = 3;

    #if 1
        int b = 3;
    #else
        int c = 3;
    #endif

    int d = 3;
#else
    int a = 4;

    #if 1
        int b = 4;
    #else
        int c = 4;
    #endif

    int d = 4;
#endif

#if 1
    int a = 5;

    #if 0
        int b = 5;
    #else
        int c = 5;
    #endif

    int d = 5;
#else
    int a = 6;

    #if 0
        int b = 6;
    #else
        int c = 6;
    #endif

    int d = 6;
#endif

#if 1
    int a = 7;

    #if 1
        int b = 7;
    #else
        int c = 7;
    #endif

    int d = 7;
#else
    int a = 8;

    #if 1
        int b = 8;
    #else
        int c = 8;
    #endif

    int d = 8;
#endif
