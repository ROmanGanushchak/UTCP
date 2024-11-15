cmake_minimum_required(VERSION 3.24)
project(protocol)
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_C_COMPILER "gcc")
set(CMAKE_CXX_COMPILER "g++")

set(SOURCE_FILES
    main.cpp
    receiver.cpp
    sender.cpp
    data.cpp
    connector.cpp
    fragmentator.cpp
    queues.cpp
    crc.cpp)

# set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static-libgcc -static-libstdc++ -static")

add_executable(${PROJECT_NAME} ${SOURCE_FILES})

target_link_libraries(protocol PRIVATE ws2_32)