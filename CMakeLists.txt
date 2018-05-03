cmake_minimum_required(VERSION 3.2 FATAL_ERROR)
project(http_parser)

# Build options
#
option(WITH_CONAN   "Include conan declarations" OFF)
option(STRICT       "Strict mode" OFF)
option(WITH_TESTS   "Enable testing" OFF)

if (WITH_CONAN)
  include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
  conan_basic_setup()
endif()

if (STRICT)
  add_definitions(-DHTTP_PARSER_STRICT=1)
else()
  add_definitions(-DHTTP_PARSER_STRICT=0)
endif()

# Library build
# Understands standard BUILD_SHARED_LIBS option (default static)
#
add_library(http_parser http_parser.c)
if (UNIX OR MINGW)
  target_compile_options(http_parser PRIVATE -Wall -Wextra -Werror)
endif()
target_include_directories(http_parser PUBLIC .)

# Contrib and benchmarks
#
if (UNIX OR MINGW)
  add_executable(bench bench.c)
  target_link_libraries(bench http_parser)
endif()

add_executable(parsertrace contrib/parsertrace.c)
target_link_libraries(parsertrace http_parser)

add_executable(url_parser contrib/url_parser.c)
target_link_libraries(url_parser http_parser)

# Testing
#
if (WITH_TESTS)
  enable_testing()

  add_executable(test_http_parser test.c)
  target_link_libraries(test_http_parser http_parser)

  add_test(NAME test_http_parser COMMAND $<TARGET_FILE:test_http_parser>)
endif()

# Installation
#
install(TARGETS http_parser 
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)

install(FILES http_parser.h
        DESTINATION include)
