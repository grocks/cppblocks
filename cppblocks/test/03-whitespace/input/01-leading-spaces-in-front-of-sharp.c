  #ifdef FOO
int a = 1;
 #ifdef BAR
int b = 1;
#endif
int c = 1;
             #endif

	#define FOO

 #ifdef FOO
int a = 2;
#ifdef BAR
int b = 2;
  #endif
int c = 2;
#endif

#define BAR

		#ifdef FOO
int a = 3;
 #ifdef BAR
int b = 3;
#endif
int c = 3;
  #endif

