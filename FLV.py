import subprocess, os, struct

class FLV:

    # Header
    SIGNATURE = b"\x46\x4C\x56"
    VERSION = b"\x01"
    FLAGS = bytes([0b00000101])
    DATA_OFFSET = bytes([0,0,0,9])

    # Body
    # FILE_SIZE = NUMBER_OF_FRAMES * FRAME_SIZE
    # FILE_SIZE = FRAMES_PER_SECONDS * DURATION * FRAME_SIZE
    # FILE_SIZE = FRAMES_PER_SECONDS * DURATION * {(Width * Height * Bit Depth[6 - 2 for RGB])/8*1024}
    

    DURATION = 8 # 8sec per video segment
    TagTypes = {
        "audio": bytes([8]),
        "video": bytes([9])
    }

    def __init__(self, file_name, path, settings):
        self.file_name = file_name
        self.full_path = path + "\\" + file_name + ".flv"
        self.previous_tag_size = 0
        self.current_body_size = 0

        with open(self.full_path, 'ab') as file:
            file.write(
                # FLV Header
                FLV.SIGNATURE +
                FLV.VERSION +
                FLV.FLAGS + 
                FLV.DATA_OFFSET
            )


        # {'width': 1920.0, 'height': 1080.0, 'videocodecid': 7.0, 'videodatarate': 2500.0, 'framerate': 60.0, 'audiocodecid': 10.0, 'audiosamplesize': 16.0, 'audiochannels': 2.0, 'stereo': 1}
        self.settings = settings
        self.frame_size = (settings['width'] * settings['height'] * 6) / (8 * 1024)
        self.number_of_frames = settings['framerate'] * FLV.DURATION
        self.max_size = self.frame_size * self.number_of_frames # in KB


    def add(self, data):
        if data[0] != 68:
            # self.write_data(data[8::])
            return


        # 68 is the defualt byte number '\x44' for new data
        # The 7th byte indecated the data type, 8 for audio, 9 for video.
        if data[7] != 8 and data[7] != 9:
            return

        TAG_TYPE = struct.pack("b", data[7]) # b for 1 byte long
        DATA_SIZE = data[4:7] 
        TIMESTAMP = data[1:4]
        TIMESTAMP_EXTENDED = bytes(1) # b'/x00'
        STREAM_ID = bytes(3) # b'/x00/x00/x00'
        start = [TAG_TYPE, DATA_SIZE, TIMESTAMP, TIMESTAMP_EXTENDED, STREAM_ID]
        
        if TAG_TYPE == FLV.TagTypes["audio"]:
            # Add Tag [start]

            self.write_data(struct.pack("i", self.previous_tag_size)[::-1]) # "i" = integer = 32 bits = 8 bytes
            self.previous_tag_size = 0
            for i in start:
                self.write_data(i)
                self.previous_tag_size += len(i)
            self.__add_audio(data[9::])

        elif TAG_TYPE == FLV.TagTypes["video"]:
            self.__add_video(data[8::])


    def __add_audio(self, data):
        # start
        # sound_format = 0b1010 # 10 = AAC
        # sound_rate = 0b11 # For AAC: always 3 (44-kHz)
        # sound_size = 0b0
        # sound_type = 0b1 # For AAC: always 1 (Stereo)
        start_audio_tag = bytes([0b10101101])
        self.write_data(start_audio_tag)
        self.previous_tag_size += len(start_audio_tag)

        # data
        self.write_data(data) # acutally the data
        self.previous_tag_size += len(data)
        print(self.previous_tag_size, len(data) + 12)

    def __add_video(self, data):
        pass

    def finished(self):
        return self.current_body_size >= self.max_size

    def write_data(self, data_input):
        with open(self.full_path, 'ab') as file:
            file.write(data_input)

    # Conertion system
    TS_FILL = 6

    def to_ts(self):
        # os.chdir(r"C:\Users\Sahar_Cohen\Desktop\Cyber Project - Sahar Cohen\FlaskServerApp\static\streams\video")
        subprocess.call(f"ffmpeg -i temp.flv -vcodec libx264 -acodec aac { self.file_name }.ts")
        os.remove(self.file_name)