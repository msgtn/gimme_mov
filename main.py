from PIL import Image
import numpy as np
import cv2
import os
import random
import skvideo.io
from moviepy.editor import *

img_dir, vid_mul = './jpn/', 1
# img_dir, vid_mul = './bdc/down/', 10
imgs = []

max_max_dim = 0

ar = 16/9.
vid_res = 480
vid_dim = (vid_res,int(ar*vid_res))
vid_dim = (2000,2000)
vid_dim = (360,640)
if img_dir == './jpn/':
    vid_dim = (int(4/5*640), 640)
else:
    vid_dim = (640,360) 

fps = 30
out = cv2.VideoWriter(
    img_dir+'output.mp4',
    # cv2.cv.CV_FOURCC('m','p','4','v'),
    cv2.VideoWriter_fourcc('m','p','4','v'),
    fps,
    vid_dim,
    )

vid_list = os.listdir(img_dir)
for rm_file in ['.DS_Store', 'output.mp4', 'final.mp4']:
    try:
        vid_list.remove(rm_file)
    except:
        pass
vid_list *= vid_mul
random.shuffle(vid_list)

add_begin = [
    'IMG_9178.mov',
    'IMG_2824.mov',
    '8ee369d3d69f46abb5d9c9247ce8665e.mov'
]
add_end = [
    'IMG_4457.mov',
    'video_afd0e95e5efc429582a0afac3e990cbe.mov',
]

# definite start and end - should be arguable
if img_dir == './jpn/':
    for v in add_begin[::-1]:
        vid_list.remove(v)
        vid_list.insert(0,v)
    for v in add_end:
        vid_list.remove(v)
        vid_list.append(v)
else:
    # vid_list = vid_list[:2]
    pass

# video length in seconds
vid_len = 59.7
# vid_len = 51
# how many frames for each clip
len_clip = 7
len_clip = int(vid_len*fps/len(vid_list))
print("{} frames for each of the {} videos".format(len_clip, len(vid_list)))

rem_clips = (vid_len*fps)-(len_clip*len(vid_list))
rem_ctr = 0
# rem_clips = 0
print("{} clips will be extended to {} frames".format(rem_clips,len_clip+1))

# problem_vid_id = '6921'
# vid_list.remove('IMG_{}.mov'.format(problem_vid_id))
# vid_list.insert(0,'IMG_{}.mov'.format(problem_vid_id))
# vid_list = vid_list[:2]

for i,vid_name in enumerate(vid_list):
    print("Processing {}, {}/{}".format(vid_name, i, len(vid_list)))
    try:
        vid_data = skvideo.io.FFmpegReader(img_dir+vid_name)
        (clip_len, h, w, _) = vid_data.getShape()
    except:
        # guess that it's a 1-sec long vertical video
        clip_len = 30
        h, w = 640,360
    # print(h,w)
    vertical = True if h>w else False
    # vertical = True
    vidcap = cv2.VideoCapture(img_dir+vid_name)
    vid_start = np.random.choice(
        range(clip_len*3//4-len_clip),
        )

    # vid_start = int(np.random.normal(clip_len//4, clip_len//4))
    for _ in range(vid_start):
        success, img = vidcap.read()
    vid_size = img.shape
    # print(vid_size)
    vertical = vid_size[0]<vid_size[1]
    if 'video' not in vid_name and img_dir == './jpn/':
        if vertical:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        # else:
        #     img = cv2.rotate(img, cv2.ROTATE_180)

    # vid_size = img.shape
    # max_dim = np.max(vid_size)
    # mid_dim = vid_size[1]//2
    # h_dim = vid_size[0]
    # w_dim = h_dim*9//16
    # img = img[:,mid_dim-w_dim//2:mid_dim+w_dim//2,:]

    vid_size = img.shape
    max_dim = np.max(vid_size)
    try:
        x_diff, y_diff = (vid_dim[1]-vid_size[0])//2,(vid_dim[0]-vid_size[1])//2
    except:
        x_diff, y_diff = (vid_dim[0]-vid_size[0])//2,(vid_dim[1]-vid_size[1])//2


    clip_ctr = 0 if (rem_ctr>rem_clips) else -1


    # p_ext = (rem_clips-rem_ctr)/rem_clips
    # # definitely extend if running out of clips
    # if len(vid_list)<=(rem_clips-rem_ctr):
    #     p_ext = 1
    p_ext = np.min([(rem_clips-rem_ctr)/(len(vid_list)-i),1.0])
    clip_ctr = np.random.choice(
        [0,-1],
        p=[1-p_ext, p_ext],
        )
    if clip_ctr == -1:
        rem_ctr += 1
    while success and clip_ctr<len_clip:

        img = np.pad(
            img,
            pad_width=[[x_diff,x_diff],[y_diff,y_diff],[0,0]],
            mode='constant',
            constant_values=255)
        img = cv2.resize(img, vid_dim)
        # imgs.append(np.array(img))
        out.write(np.uint8(img))
        # burn some frames 
        # for _ in range(60):
        #     success,img = vidcap.read()
        # if success:
        success, img = vidcap.read()
        if 'video' not in vid_name and img_dir == './jpn/':
            if vertical:
                img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            # else:
            #     img = cv2.rotate(img, cv2.ROTATE_180)
        # img = img[:,mid_dim-w_dim//2:mid_dim+w_dim//2,:]
        clip_ctr += 1

    # rem_ctr += 1


out.release()

# attach audio
vid = VideoFileClip(img_dir+"output.mp4")
aud = AudioFileClip("./gimme_trim.m4a").set_duration(vid.duration)
vid = vid.set_audio(aud)
vid.write_videofile(img_dir+"final.mp4",
    audio=True,
    # temp_audiofile="temp-audio.m4a", remove_temp=True,
    codec="libx264", audio_codec="aac")



