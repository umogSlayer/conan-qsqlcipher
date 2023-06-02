cmake_minimum_required(VERSION 3.26)
project(qsqlcipher)

find_package(Qt5 5.15.0 REQUIRED
    COMPONENTS
        Core
        Sql)

find_package(sqlcipher)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)

if (BUILD_SHARED_LIBS)
    add_library(qsqlcipher MODULE
        qsqlcipher/qsql_sqlite_p.h
        qsqlcipher/qsql_sqlite.cpp
        qsqlcipher/smain.cpp)
else ()
    add_library(qsqlcipher STATIC
        qsqlcipher/qsql_sqlite_p.h
        qsqlcipher/qsql_sqlite.cpp
        qsqlcipher/smain.cpp)
endif ()

target_link_libraries(qsqlcipher
    PRIVATE
        sqlcipher::sqlcipher
        Qt5::Core
        Qt5::CorePrivate
        Qt5::Sql
        Qt5::SqlPrivate)

if (BUILD_SHARED_LIBS)
    install(TARGETS qsqlcipher DESTINATION LIBRARY DESTINATION plugins/sqldrivers)
else ()
    install(TARGETS qsqlcipher DESTINATION ARCHIVE DESTINATION lib)
endif ()
