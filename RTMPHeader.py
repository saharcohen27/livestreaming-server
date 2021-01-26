import re
from AMF0 import AMFBody # only for the add operator

class RTMPHeader:
    # each message type has its own id
    RTMP_message_type_ids = {
       "setChunkSize": b'\x01',
        "abort"      : b'\x02',
        "ack"        : b'\x03',
        "control"    : b'\x04',
        "serverBW"   : b'\x05',
        "clientBW"   : b'\x06',
        "audio"      : b'\x08',
        "video"      : b'\x09',
        "command"    : b'\x14'
   }
    
    timestamp = b'\x00\x00\x00' # now days, almost no one uses real timestap, defualt is 0. 3 bytes long.

    def __init__(self, RTMP_header_type=b'\x03'):
        # every RTMP header usually stats with 3 at the begining and defualt timestamp. 
        self.header = RTMP_header_type + RTMPHeader.timestamp
    
    def add_length(self, data):
        # after the defualt begining, we need to add the length of the data (AMFBody)
        if len(data) > 16777215: # max 3 bytes FF FF FF
            print("[RTMP HEADER] AMF0 data length is too long.")
            return False
        
        else:
            hex_len = hex(len(data))[2::] # removing the '0x' at the begining
            for _ in range(6 - len(hex_len)): # make it 6 hex digits long by adding 0's at the end
                hex_len = '0' + hex_len
            length = bytes.fromhex(hex_len)
            # convert to bytes will make it always 3 bytes long as it should be
            # Ex: b"/x05/x24/x15/x49" (AMFBody type) => b'\x00\x00\x04' (length = 4)

            self.header += length
    
    def add_type_id(self, message_type):
        if not message_type in RTMPHeader.RTMP_message_type_ids:
            print("[ERROR!] Requested message type id does not exist.")
            return
        
        self.header += RTMPHeader.RTMP_message_type_ids[message_type]

    def add_stream_id(self, this=False):
        # TODO manage this stream id
        if this:
            self.header += this
        else:
            self.header += b'\x00\x00\x00\x00'

    def get_content(self):
        return self.header

    def __repr__(self):
        return str(self.header)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.header + other.header
        elif isinstance(other, AMFBody):
            return self.header + other.get_content()
        elif isinstance(other, bytes):
            return self.header + other
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(self.__class__, type(other)))