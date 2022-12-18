// Axel '0vercl0k' Souchet - December 17 2022
#include <cstdio>

struct Tracer_t {
  Tracer_t() noexcept { printf("Tracer_t() default ctor\n"); }
  ~Tracer_t() noexcept { printf("~Tracer_t() dtor\n"); }
  Tracer_t(const Tracer_t &) noexcept {
    printf("Tracer_t(const Tracer_t &) copy ctor\n");
  }
  Tracer_t &operator=(const Tracer_t &Other) noexcept {
    if (&Other == this) {
      printf("self assignment! ");
    }
    printf("operator=(const Tracer_t &Other) copy assignment operator\n");
    return *this;
  }

  Tracer_t(Tracer_t &&) noexcept {
    printf("Tracer_t(Tracer_t &&) move ctor\n");
  }
  Tracer_t &operator=(Tracer_t &&) noexcept {
    printf("operator=(Tracer_t &&) move assignment operator\n");
    return *this;
  }
};