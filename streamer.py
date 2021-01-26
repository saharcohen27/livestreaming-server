import uuid, os
from DataBase import Database
from FLV import FLV

class Streamer:
    TS_FILL = 8

    def __init__(self, socket):
        self.socket = socket

        # Stream Handler
        self.file_index = -1
        self.settings = None
        self.current_path = None
        self.current_file = None
        self.m3u8 = None

        # Database Properties
        self.username = None
        self.stream_key = None
        self.is_live = False
        self._id = uuid.uuid4()
    
    def set_stream_key(self, stream_key):
        self.stream_key = stream_key
        self.username = Database().get_username_by_streamkey(stream_key)
    
    def start_live(self):
        self.is_live = True
        Database().start_live(self.username)
        self.current_path = os.getcwd() + "\\" + self.username
        try:
            os.mkdir(self.current_path)
        except FileExistsError:
            # its not the first time this user is creating live
            pass
        self.current_path += "\\" + str(self._id)
        os.mkdir(self.current_path) # creating folder for the current stream
        
    def live_on(self):
        return self.is_live

    def stop_live(self):
        self.is_live = False
        Database().stop_live(self.username)
        self.socket.close()

    def __next_file_name(self):
        self.file_index += 1
        return "segment" + str(self.file_index).zfill(Streamer.TS_FILL)

    def set_stream_settings(self, settings):
        # Ex: 
        # {'width': 1920.0, 'height': 1080.0, 'videocodecid': 7.0, 'videodatarate': 2500.0, 'framerate': 60.0, 'audiocodecid': 10.0, 'audiosamplesize': 16.0, 'audiochannels': 2.0, 'stereo': 1}
        self.settings = settings

    def handle_stream(self, data):
        # if len(FLV) >= 2 [sec]:
        #    flv.add(data)
        # else:
        #    m3u8.add(flv)
        #    flv = FLV(self.__next_file_name())
        if not self.settings:
            return

        if not self.current_file:
            # for the first time
            self.current_file = FLV(self.__next_file_name(), self.current_path, self.settings)
        
        elif self.current_file.finished():
            # m3u8.add(flv)
            self.current_file = FLV(self.__next_file_name(), self.current_path, self.settings)
        
        else:
            self.current_file.add(data)
