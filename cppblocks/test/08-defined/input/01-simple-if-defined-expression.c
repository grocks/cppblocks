#if defined FOOBAR
int a = 1;

int b = 2;

int c = 3;
#endif

#define FOOBAR

#if defined FOOBAR

int main();

int a = 2;

int b = 3;

int c = 4;
#endif

#if 0

int a = 3;

#elif defined FOOBAR

int b = 3;

#elif defined BAR

int c = 4



#endif
