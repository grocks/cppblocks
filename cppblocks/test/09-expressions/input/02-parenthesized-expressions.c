/////////////////////////////
// Parenthesized constants
/////////////////////////////
#if (1)
int a = 1;

int b = 1;

#elif (0)

int a = 2;

int b = 2;
#endif

/////////////////////////////
// Parenthesized defined
/////////////////////////////
#if defined (FOO)
int a = 3;

#elif defined( FOO )

int b = 3;
#elif defined(FOO)
int c = 3;
#endif

////////////////////////////////////
// Parenthesized basic expressions
////////////////////////////////////

#if ((FOO) == (BAR))
int a = 4;
#elif ( ( FOO ) != (BAR)    )
int b = 4;


#elif (! (! (FOO) )	)

int c = 4;

#endif
