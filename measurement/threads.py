import threading


class AudioInterfaceThread (threading.Thread):

    def __init__(self, thread_id, name, audio_device_manager):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.audio_device_manager = audio_device_manager

    def run(self):
        print("Starting " + self.name)
        if self.name == 'Thread-play':
            self.audio_device_manager.play()
        else:
            self.audio_device_manager.record()

        print("Exiting " + self.name)
