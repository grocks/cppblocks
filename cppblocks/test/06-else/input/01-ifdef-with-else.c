#ifdef FOOBAR
int a = 1;
#else
int b = 1;
#endif

#define BARFOO

#ifdef BARFOO
int a = 2;
#else
int b = 2;
#endif
