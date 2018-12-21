/*
#
#    bind_vs_lambda.cc - Toy program to study how std::bind compare to lambda.
#    Copyright (C) 2017 Axel "0vercl0k" Souchet - http://www.twitter.com/0vercl0k
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
*/

#include <functional>
#include <memory>

struct Foo {
    uintptr_t f;
    Foo(uintptr_t f)
    : f(f) {}
};

size_t read_from_blah(Foo *obj, uintptr_t idx, uintptr_t a, uintptr_t b) {
    printf("read_from_blah: %zd, %zd, %zd, %zd.\n", obj->f, idx, a, b);
    return b;
}

__declspec(noinline) void test_lambda() {
    std::shared_ptr<Foo> obj = std::make_shared<Foo>(1337);
    uintptr_t idx = 1338;
    auto Read = [&, obj, idx](uintptr_t a, uintptr_t b) {
        return read_from_blah(obj.get(), idx, a, b);
    };
    printf("%zd\n", Read(1, 2));
}

__declspec(noinline) void test_bind() {
    std::shared_ptr<Foo> obj = std::make_shared<Foo>(1337);
    uintptr_t idx = 1338;
    auto Read = std::bind(
        read_from_blah, obj.get(), idx,
        std::placeholders::_1, std::placeholders::_2
    );
    printf("%zd\n", Read(1, 2));
}

int main() {
    printf("== lambda\n");
    test_lambda();
    printf("== bind\n");
    test_bind();
    return 0;
}