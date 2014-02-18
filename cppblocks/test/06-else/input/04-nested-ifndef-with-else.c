#define FOOBAR

#ifndef FOOBAR

int a = 1;

#else

 #ifndef BARFOO
int b = 1;
 #endif

#endif

#define BAZBAR

#ifndef BAZ
int a = 2;

 #ifndef BAZBAR
int b = 2;
 #endif

#else

int c = 2;

#endif
