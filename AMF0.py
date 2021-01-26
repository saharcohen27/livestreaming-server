import struct

class AMFBody:
    # each message type has its own id
    types = {
        "number": b'\x00',
        "bool"  : b'\x01',
        "string": b'\x02',
        "startobj": b'\x03',
        "null"  : b'\x05',
        "array" : b'\x08',
        "endobj": b'\x00\x00\x09' # 9 preceded by an empty 16-bit string length
    }

    def __init__(self):
        self.body = b''

    def decode_number(self, float_number):
        pass

    def __encode_number(self, data):
        # numbers in AMF0 are always doubles | float64
        if data == 0:
            return AMFBody.types['number'] + bytes.fromhex('0' * 16) # 16 hex digits = 8 bytes = 64 bits matches to float64 format

        hex_string = hex(struct.unpack('<Q', struct.pack('<d', data))[0])[2::] # double to hex # returns tuple with one value
        return AMFBody.types['number'] + bytes.fromhex(hex_string)
    
    def __encode_string(self, data):
        # b"\[STRING-TYPE-ID]\[LENGTH]\[THE-STRING]"
        if len(data) > 65535:
            print("[AMF0 Body] Too Long.")
            return False
        
        hex_len = hex(len(data))[2::] # removing the '0x' at the begining
        for _ in range(4 - len(hex_len)): # make it 4 hex digits long by adding 0's at the end
            hex_len = '0' + hex_len
        length = bytes.fromhex(hex_len)

        # convert to bytes will make it always 2 bytes long as it should be
        # Ex: "hello" (AMFBody type) => b'\x00\x05' (length = 5)

        byte_data = bytes.fromhex(data.encode().hex()) # string to hex to bytes

        return AMFBody.types['string'] + length + byte_data

    def __encode_key(self, key):
        # keys are always strings but its not acually a string so we dont want the string type id
        return self.__encode_string(key)[1:] # removing the type id of string

    def __encode_array(self, arr):
        encoded_arr = AMFBody.types['array']

        hex_len = hex(len(arr))[2::] # removing the '0x' at the begining
        for _ in range(8 - len(arr)): # make it 4 hex digits long by adding 0's at the end
            hex_len = '0' + hex_len
        length = bytes.fromhex(hex_len)

        encoded_arr += length

        for key, value in arr:
            encoded_arr += self.__encode_key(key)

            if type(value) == str:
                encoded_arr += self.__encode_string(value)
            
            elif type(value) == int or type(value) == float:
                encoded_arr += self.__encode_number(value)

        encoded_arr += AMFBody.types['endobj'] # we end array like we end object
        return encoded_arr

    def __encode_object(self, data):
        encoded_object = AMFBody.types['startobj']
        
        for key, value in data.items():
            encoded_object += self.__encode_key(key)
            
            if type(value) == str:
                encoded_object += self.__encode_string(value)
            
            elif type(value) == int or type(value) == float:
                encoded_object += self.__encode_number(value)

            elif type(value) == list:
                encoded_object += self.__encode_array(value)

        encoded_object += AMFBody.types['endobj']

        return encoded_object

    def add(self, data):
        if data == None:
            self.body += AMFBody.types['null']

        elif type(data) == str:
            self.body += self.__encode_string(data)
            
        elif type(data) == float or type(data) == int:
            data = float(data)
            self.body += self.__encode_number(data)
        
        elif type(data) == dict:
            self.body += self.__encode_object(data)
    
    def get_content(self):
        return self.body

    def __repr__(self):
        return str(self.body) if self.body else ''

    def __len__(self):
        return len(self.body)