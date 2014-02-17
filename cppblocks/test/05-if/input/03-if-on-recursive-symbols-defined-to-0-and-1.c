#define FOO 0

#define BAR 1

#define FOOFOO FOO

#if FOOFOO
int a = 3;
#endif

#define BARBAR BAR

#if BARBAR
int b = 4;
int c = 4;
#endif
