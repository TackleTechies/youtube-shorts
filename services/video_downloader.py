from pytube import YouTube
from os import listdir
from os.path import isfile, join

class VideoDownloader:

    def __init__(self,youtube_url,start_second):
        self.youtube_url = youtube_url
        self.start_second = start_second

    def run(self,staging_path):
        
        d = YouTube(self.youtube_url).streams.get_highest_resolution()
        d.download(staging_path)

        onlyfiles = [f for f in listdir(staging_path) if isfile(join(staging_path, f))]
        filename = onlyfiles[0]
        filepath =  f"{staging_path}/{filename}"

        with open( filepath, "rb") as file:
            file_bytes = file.read()
            return file_bytes,filepath,filename