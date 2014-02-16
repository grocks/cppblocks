#define FOO

#ifdef FOO
int i = 3;
#endif

#undef FOO

#ifdef FOO
int j = 3;
#endif

#ifndef BAR

#define BAR

#ifndef BAR
int a = 1;
#endif

#undef BAR

#ifndef BAR
int b = 1;
#endif

#endif
