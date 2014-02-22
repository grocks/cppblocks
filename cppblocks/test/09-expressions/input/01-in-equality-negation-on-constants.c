///////////////////////////////////////
// Conditions evaluating to false
///////////////////////////////////////

#if 0 == 1

int a = 1;

int b = 1;

int c = 1;

#elif 1 != 1

int a = 2;

int b = 2;
#elif !1

int b = 3;

int c = 3;

#endif



///////////////////////////////////////
// Conditions evaluating to true
///////////////////////////////////////

#if 42 == 42

int a = 1;

int b = 1;

int c = 1;

#elif 0 != 1

int a = 2;

int b = 2;
#elif !0

int b = 3;

int c = 3;

#endif

#if 0
int a = 3;
#elif 0 != 3
int b = 3;
#endif

#if 0
#elif !0
int a = 4;

int b = 4;

int c = 4;

#endif
