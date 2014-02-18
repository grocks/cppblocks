#ifdef FOOBAR
int a = 1;
#else

 #ifdef BARFOO
int b = 1;
 #endif

#endif

#define BAZ

#ifdef BAZ
int a = 2;

 #ifdef BAZBAR
int b = 2;
 #endif

#else
int c = 2;
#endif
