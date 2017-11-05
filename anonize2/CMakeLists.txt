project(anonize2 CXX)
include_directories(${CMAKE_CURRENT_SOURCE_DIR}/../relic/include)
add_subdirectory(../relic-darwin ../relic-darwin)

set(CMAKE_C_COMPILER /usr/bin/clang)
set(CMAKE_CXX_COMPILER /usr/bin/clang++)
add_compile_options(-std=c++11 -stdlib=libc++ -fomit-frame-pointer -DNDEBUG -msse2 -mfpmath=sse -march=native -fPIC)
add_compile_options(-DRELIC_LIBRARY)

add_library(anon SHARED anon.cpp sha2.cpp)
add_executable(anontest anontest.cpp)
target_link_libraries(anon PRIVATE anon relic_s c++)
target_link_libraries(anontest PRIVATE anon relic_s c++)
