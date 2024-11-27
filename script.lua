-- Declare the protocol
local my_protocol = Proto("MyProtocol", "My Custom Protocol")

local types = {
    [0] = "PureData",
    [1] = "Resend",
    [2] = "KeepAlive",
    [3] = "ACK",
    [4] = "Connection",
    [5] = "ConnectionApproval",
    [6] = "EndConnection",
    [7] = "String",
    [8] = "File",
    [255] = "Unknown"
};

local f_crc = ProtoField.uint16("my_protocol.crc", "CRC", base.HEX)
local f_data_length = ProtoField.uint16("my_protocol.data_length", "Data Length", base.DEC)
local f_seq = ProtoField.uint16("my_protocol.seq", "Sequence Number", base.DEC)
local f_type = ProtoField.uint8("my_protocol.type", "Data Type", base.DEC, types)
local f_is_next_fragment = ProtoField.bool("my_protocol.is_next_fragment", "Is Next Fragment", 8, {"False", "True"}, 0x01)
local f_window = ProtoField.uint16("my_protocol.window", "Window", base.DEC)
local f_data = ProtoField.bytes("my_protocol.data", "Data")

my_protocol.fields = {f_crc, f_data_length, f_seq, f_type, f_is_next_fragment, f_window, f_data}

function my_protocol.dissector(buffer, pinfo, tree)
    if buffer:len() < 10 then return end

    pinfo.cols.protocol = my_protocol.name

    local subtree = tree:add(my_protocol, buffer(), "My Custom Protocol")
    subtree:add(f_crc, buffer(0, 2))
    local data_length = buffer(2, 2):le_uint()
    subtree:add(f_data_length, buffer(2, 2))
    local seq = buffer(4, 2):le_uint()
    subtree:add(f_seq, buffer(4, 2))
    local data_type = buffer(6, 1):uint()
    subtree:add(f_type, buffer(6, 1))
    subtree:add(f_is_next_fragment, buffer(7, 1):bitfield(0, 1))
    subtree:add(f_window, buffer(8, 2):le_uint())

    if buffer:len() > 10 then
        local data_offset = 10
        local data_end = math.min(buffer:len(), data_offset + data_length)
        subtree:add(f_data, buffer(data_offset, data_end - data_offset))
    end

    local type_description = types[data_type] or "Unknown"
    pinfo.cols.info:set(string.format("Type: %s, Seq: %d", type_description, seq))
end

local udp_table = DissectorTable.get("udp.port")
udp_table:add(8080, my_protocol)
udp_table:add(8082, my_protocol)
udp_table:add(8084, my_protocol)
udp_table:add(8086, my_protocol)
