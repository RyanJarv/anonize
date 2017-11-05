cmake_minimum_required(VERSION 2.8.12)
project(cmake_example)

add_subdirectory(anonize2)

include_directories(anonize2)
include_directories(relic/include)

#add_compile_options("-undefined dynamic_lookup")

#link_libraries(anon)
#pybind11_add_module(cmake_example src/main.cpp)
#target_link_libraries(cmake_example PRIVATE anon relic_s c++)
#set_target_properties(anon PROPERTIES POSITION_INDEPENDENT_CODE TRUE)
