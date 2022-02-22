
import requests
from random import choice
import re
import json
from pytube import YouTube
import cv2 as cv
from os import listdir, remove
from ffpyplayer.player import MediaPlayer
import time



KEY = API_KEY

class Video:
    
    def __init__(self, key):
        self.key = key
    
    def api_link(self, vid):
        return f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={vid}&key={self.key}" 

    def info(self, vid, find):
        return requests.get(self.api_link(vid)).json()["items"][0]["snippet"][find]

    def get_data(self, title):

        search = '+'.join(title.split())

        url = f"https://www.youtube.com/results?search_query={search}"
        html = requests.get(url).text
        video_ids = re.findall(r"watch\?v=(\S{11})", html)
        

        return [(self.info(id_,"title")+ ' - [' +self.info(id_,"channelTitle") + ']', "https://www.youtube.com/watch?v=" + id_) for id_ in video_ids[:6]]




vid = Video(KEY)


class Play:
    
    def choose(self, lst):

        while True:
            inp = input()
            if inp.isdigit() and int(inp)>=1 and int(inp)<=len(lst):
                return int(inp)
            

    def find(self, title):

        data = vid.get_data(title)

        for num, (title, link) in enumerate(data):
            print(f"\n {num+1}. {title}")
        
        inp = self.choose(data)

        return "\n" + data[inp-1][1]

    def play(self, vid_path):

        capture = cv.VideoCapture(vid_path)
        player = MediaPlayer(vid_path)

        fps = capture.get(cv.CAP_PROP_FPS)
        window = 'Video'

        cv.namedWindow(window, cv.WND_PROP_FULLSCREEN)
        cv.setWindowProperty(window, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

        end, start = 0,0

        while True:

            delay = end-start
            start = time.time()

            isTrue, frame = capture.read()
            audio_frame, value = player.get_frame()
            cv.imshow(window,frame)
            

            if cv.waitKey(int((1000/fps)-delay)) & 0xFF==ord('d'):
                cv.destroyAllWindows()
                break

            if cv.getWindowProperty(window, 4) < 1:
                cv.destroyAllWindows()
                break
            
            end = time.time()
    
        capture.release()

play = Play()



for path in list(filter(lambda x: '.mp4' in x,listdir())): remove(path)

YouTube(play.find(input('What do you feel like watching? '))).streams.get_highest_resolution().download()


play.play(list(filter(lambda x: '.mp4' in x,listdir()))[0])




