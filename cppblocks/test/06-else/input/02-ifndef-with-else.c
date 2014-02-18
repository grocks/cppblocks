#ifndef FOOBAR
int a = 1;
#else
int b = 1;
#endif

#define BARFOO

#ifndef BARFOO
int a = 2;
#else
int b = 2;
#endif
