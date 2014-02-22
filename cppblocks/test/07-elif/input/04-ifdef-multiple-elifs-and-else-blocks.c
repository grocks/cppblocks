#define ENTER_IFDEF

#ifdef ENTER_IFDEF
int a = 1;
void some_function(int, float);

#elif ENTER_ELIF1

int b = 1;

void another_function(const char *argv[]);

#elif ENTER_ELIF2

int c = 1;


int * process_something(const char **argv (*function_ptr)(float, float *));

#else

float d = 1;
int main();

#endif


///////////////////////////////////
// Test entering of elif 1
///////////////////////////////////

#undef ENTER_IFDEF
#define ENTER_ELIF1 1

#ifdef ENTER_IFDEF
int a = 2;
void some_function(int, float);

#elif ENTER_ELIF1

int b = 2;

void another_function(const char *argv[]);

#elif ENTER_ELIF2

int c = 2;


int * process_something(const char **argv (*function_ptr)(float, float *));

#else

float d = 2;
int main();

#endif

///////////////////////////////////
// Test entering of elif 2
///////////////////////////////////

#undef ENTER_ELIF1
#define ENTER_ELIF2 1

#ifdef ENTER_IFDEF
int a = 3;
void some_function(int, float);

#elif ENTER_ELIF1

int b = 3;

void another_function(const char *argv[]);

#elif ENTER_ELIF2

int c = 3;


int * process_something(const char **argv (*function_ptr)(float, float *));

#else

float d = 3;
int main();

#endif

///////////////////////////////////
// Test entering of else
///////////////////////////////////

#undef ENTER_ELIF2

#ifdef ENTER_IFDEF
int a = 3;
void some_function(int, float);

#elif ENTER_ELIF1

int b = 3;

void another_function(const char *argv[]);

#elif ENTER_ELIF2

int c = 3;


int * process_something(const char **argv (*function_ptr)(float, float *));

#else

float d = 3;
int main();

#endif

