import os, struct, binascii
import socket
from RTMPHeader import RTMPHeader
from AMF0 import AMFBody

class RTMP:
    BUFFER = 4096

    def __init__(self):
        self.message = ""

    def handshake(self, conn, data):
        c1 = data[1::]
        s0 = b'\x03'
        s1 = os.urandom(1536)
        response = s0 + s1
        conn.send(response) # sending '3' and 1536 another random bytes just as like the client sent us

        c2 = conn.recv(RTMP.BUFFER)
        # c2 is the copy of the bytes the server sent c2 == s1
        conn.send(c1)
        # just as like the client sent us the bytes we sent him, we need to send him the bytes he sent us.
        # Thats the idea of handshake.

    def set_chunk_size(self, conn, size=4096):     
        # defualt size 4096
        size = hex(size)[2::] # coverting to hex and removeing the "0x" from the begining

        for _ in range(8 - len(size)):
            size = '0' + size # add zeros from the end to make the string 8 hex digits long
        # 8 digits long converting to bytes will create the right formula of empty bytes
        size = bytes.fromhex(size)
        # Ex: size = 5 => size = b'\x00\x00\x00\x05' (8 digits!)


        message = RTMPHeader(b'\x02') # creating RTMP header type 2
        message.add_length(size) # setting the length of the message (in this case, it will be always 4 bytes)
        message.add_type_id("setChunkSize") # add type id
        message.add_stream_id() # * always 0's for now.

        message = message + size
        conn.send(message)

    def _result(self): # not fully working right now

        amf0 = AMFBody()
        amf0.add("_result")
        amf0.add(1) # The command specifies the transaction ID (always equal to 1 for the connect command)

        obj1 = {
            # TODO understand what is that
            "fmsVer": "FMS/3,5,5,2004",
            "capabilities": 31.0,
            "mode": 1.0
        }

        arr = [("version", "3,5,5,2004")]

        obj2 = {
            "level"          : "status",
            "code"           : "NetConnection.Connect.Success", # the code we have to send in order to cuntinute the conntion
            "description"    : "Connection succeeded.", # could be any random string, just desc
            "data"           : arr,
            "clientId"       : 1584259571.0,
            "objectEncoding" : 0.0 # telling the user we will use AMF0 encoding and not AMF3
        }

        amf0.add(obj1)
        amf0.add(obj2)
        
        header = RTMPHeader()
        header.add_length(amf0)
        header.add_type_id("command")
        header.add_stream_id()
        
        self.message = header + amf0
        return self.message

    def OnStatus(self):
        rtmp_body = AMFBody()
        rtmp_body.add("onStatus")
        rtmp_body.add(0) #  Transaction ID set to 0
        rtmp_body.add(None) # we have to send one null type

        obj = {
            "level":"status",
            "code" :"NetStream.Publish.Start"
        }
        rtmp_body.add(obj)
        
        header = RTMPHeader() # TODO try to delete that because it make no sense
        header.add_length(rtmp_body)
        header.add_type_id("command")
        header.add_stream_id(b'\x01\x00\x00\x00')

        self.message = header + rtmp_body
        return self.message

    def onMetaData(self, data):
        # returns all the propertites
        settings = {
            "width":None,
            "height":None,
            "videocodecid":None,
            "videodatarate":None,
            "framerate":None,
            "audiocodecid":None,
            "audiosamplesize":None,
            "audiochannels":None,
            "stereo":None
        }

        for key in settings:
            if key.encode() not in data:
                continue
            
            start = data.index(key.encode()) + len(key) + 1
            float64_hex_value = data[start:start+8].hex() # float numbers are 8 bytes long
            float_value = struct.unpack("d", struct.pack("Q",int("0x"+float64_hex_value, 16)))[0] # hex to 

            if key == "stereo":
                float_value = data[start]
            
            settings[key] = float_value

        return settings

    def __repr__(self):
        return str(self.message) if self.message else None
