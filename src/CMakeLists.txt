set(SOURCE_FILES
    main.cpp
    socket.cpp
    data.cpp
    connector.cpp
    fragmentator.cpp
    fileFragment.cpp
    structs.cpp
    crc.cpp
)
list(TRANSFORM SOURCE_FILES PREPEND "src/")
set(SOURCE_FILES ${SOURCE_FILES} PARENT_SCOPE)