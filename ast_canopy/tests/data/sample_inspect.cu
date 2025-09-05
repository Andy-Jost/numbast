struct Empty {};
struct A { int a; void f();};
struct B { int a; float b; };

struct Methods {
  void a();
  int b(float, float b);
  // float c(int, ...); // ellipsis not supported

  template<typename T> void ta();
  template<typename T> T tb(T a, int b, float);
  template<typename T> T tc(T a);
  template<typename T, typename U> void td(T a, U b);
  template<int I> void te();
};

template<typename T>
struct TMethods {
  void a();
  void b(T);

  template<typename U> void ta(T, U);
};
