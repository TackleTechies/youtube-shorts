import os
from os import listdir
from os.path import isfile, join
from moviepy.editor import VideoFileClip, vfx

class ShortGenerator:

    def __init__(self,video_path,start_second,end_second=None):
        self.video_path = video_path
        self.video_name = self.video_path.split("/")[4]
        self.start_second = start_second
        self.end_second = end_second
        print(self.video_path,self.video_name,self.start_second,self.end_second)

    def crop(self,clip):    
        step = int(clip.size[0] / 16)

        margin = 4
        offset = 0
        x1= ((margin + offset) * step)
        x2= (clip.size[0] - ( (margin - offset) * step))

        clip_croped = clip.fx(vfx.crop,x1=x1, y1=0, x2=x2, y2=clip.size[1])        
        return clip_croped

    def run(self,staging_path):
        
        filepath =  f"{staging_path}/{self.video_name}"

        clip = VideoFileClip(self.video_path)
        clip = clip.subclip(self.start_second,self.end_second) 

        clip_croped = self.crop(clip)
        clip_croped.write_videofile(filepath)

        with open( filepath, "rb") as file:
            file_bytes = file.read()
            return file_bytes,filepath,self.video_name