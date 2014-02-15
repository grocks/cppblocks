#ifdef FOO
int a = 2;
#ifdef BAR
int i = 3;
#endif
int j = 1;
#endif

#define FOO

#ifdef FOO
int a = 2;
#ifdef BAR
int i = 3;
#endif
int j = 1;
#endif

#define BAR

#ifdef FOO
int a = 2;
#ifdef BAR
int i = 3;
#endif
int j = 1;
#endif

