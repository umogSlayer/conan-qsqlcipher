cmake_minimum_required(VERSION 3.20)
project(qsqlcipher)

find_package(Qt6 6.6 REQUIRED
    COMPONENTS
        Core
        Sql)

find_package(sqlcipher REQUIRED)

include(GenerateExportHeader)
set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN 1)

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)
if (APPLE)
    set(CMAKE_SHARED_MODULE_SUFFIX ".dylib")
endif ()

if (DEFINED BUILD_SHARED_LIBS)
    if (BUILD_SHARED_LIBS)
        set(PLUGIN_TYPE SHARED)
    else ()
        set(PLUGIN_TYPE STATIC)
    endif ()
endif ()

qt_add_plugin(qsqlcipher ${PLUGIN_TYPE}
    CLASS_NAME QSQLCipherDriverPlugin
    src/qsql_sqlite_p.h
    src/qsql_sqlite.cpp
    src/smain.cpp)

generate_export_header(qsqlcipher)

target_link_libraries(qsqlcipher
    PRIVATE
        sqlcipher::sqlcipher
        Qt6::CorePrivate
        Qt6::Sql
        Qt6::SqlPrivate)

target_compile_definitions(qsqlcipher
    PRIVATE
        QT_NO_CAST_TO_ASCII
        QT_NO_CAST_FROM_ASCII
        DISABLE_COLUMN_METADATA)

install(TARGETS qsqlcipher
    RUNTIME DESTINATION plugins/sqldrivers
    LIBRARY DESTINATION plugins/sqldrivers
    ARCHIVE DESTINATION lib)
