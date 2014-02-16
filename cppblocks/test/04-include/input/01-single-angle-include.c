#include <01-single-define.h>

#ifdef FOO
int i = 1;
#endif

#ifndef FOO
int j = 1;
#endif
