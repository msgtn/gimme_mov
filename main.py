from PIL import Image
import numpy as np
import cv2
import os
import random
import skvideo.io
from moviepy.editor import *
import argparse
import sys
import glob
import progress
from progress.bar import Bar

parser = argparse.ArgumentParser()
parser.add_argument('--vid_dir', '-v', default='./videos')
parser.add_argument('--vid_mul', '-vm', default=1, type=int)
parser.add_argument('--begin', '-b', default='')
parser.add_argument('--end', '-e', default='')
parser.add_argument('--shuffle','-s',default=True, action='store_true')
parser.add_argument('--output', '-o',default='output.mp4')
parser.add_argument('--vid_len','-vl', default=59.7, type=float)
parser.add_argument('--vertical', default=False, action='store_true')
parser.add_argument('--vid_limit',default=None, type=int)
parser.add_argument('--audio', '-a', default='./gimme_trim.m4a')
parser.add_argument('--square',default=False,action='store_true')


args = parser.parse_args(sys.argv[1:])

# vid_dir, vid_mul = './videos/jpn_//', 1
vid_dir = args.vid_dir
vid_dir += '' if vid_dir[-1]=='/' else '/'
print(vid_dir)
vid_mul = args.vid_mul
vid_begin = args.begin.split(',')
vid_end = args.end.split(',')
shuffle = args.shuffle
output_fn = args.output
temp_output_fn = 'temp_'+output_fn
audio_file = args.audio
if not os.path.exists(audio_file):
    print("Audio file {} does not exist".format(audio_file))
    exit()
# vid_dir, vid_mul = './bdc/down/', 10
imgs = []

ar = 16/9
vid_res = 480
vid_dim = (vid_res,int(ar*vid_res))
vid_dim = (2000,2000)
vid_dim = (360,640)
# if 'jpn' in vid_dir:
#     vid_dim = (int(4/5*640), 640)
# else:
#     vid_dim = (640,360) 
vert = args.vertical

fps = 30

# vid_list = os.listdir(vid_dir)
vid_list = glob.glob(vid_dir+'*')
# vid_list.sort()
for rm_file in ['.DS_Store', temp_output_fn, output_fn]:
    print(vid_dir+rm_file)
    try:
        vid_list.remove(vid_dir+rm_file)
        print("Skipping {}".format(rm_file))
    except:
        print("Could not skip {}".format(rm_file))

vid_list *= vid_mul
if shuffle:
    random.shuffle(vid_list)
else:
    vid_list = sorted(vid_list)


# vid_begin = [
#     'IMG_9178.mov',
#     'IMG_2824.mov',
#     '8ee369d3d69f46abb5d9c9247ce8665e.mov'
# ]
# vid_end = [
#     'IMG_4457.mov',
#     'video_afd0e95e5efc429582a0afac3e990cbe.mov',
# ]

for v in vid_begin[::-1]:
    try:
        vid_list.remove(v)
        vid_list.insert(0,v)
    except:
        print("Could not shift {} to beginning".format(v))
for v in vid_end:
    try:
        vid_list.remove(v)
        vid_list.append(v)
    except:
        print("Could not shift {} to end".format(v))

# video length in seconds
# assuming each video is one second
vid_len = np.min([args.vid_len,len(vid_list)//2])
# how many frames for each clip
len_clip = int(vid_len*fps/len(vid_list))
print("{} frames for each of the {} videos".format(len_clip, len(vid_list)))

rem_clips = int((vid_len*fps)-(len_clip*len(vid_list)))
rem_ctr = 0
print("{} clips will be extended to {} frames".format(rem_clips,len_clip+1))
# truncate if flagged
vid_limit = args.vid_limit
vid_list = vid_list if vid_limit is None else vid_list[:vid_limit]

bar = Bar('Processing',max=len(vid_list))
bar.start()
# try:
for i,vid_name in enumerate(vid_list):
    bar.next()
    print("Processing {}, {}/{}".format(vid_name, i, len(vid_list)))
    try:
        vid_data = skvideo.io.FFmpegReader(vid_name)
        (clip_len, h, w, _) = vid_data.getShape()
    except:
        # guess that it's a 1-sec long vertical video
        clip_len = 30
        h, w = 640,360
    vidcap = cv2.VideoCapture(vid_name)
    vid_start = np.random.choice(
        range(clip_len*3//4-len_clip),
        )

    # vid_start = int(np.random.normal(clip_len//4, clip_len//4))
    for _ in range(vid_start):
        success, img = vidcap.read()
    vid_size = img.shape
    # print(vid_size)
    rotate = vid_size[0]<vid_size[1]
    print("rotate {}".format(rotate))

    if i == 0:
        vid_dim = (vid_size[0],vid_size[1])
        vertical = h>w
        vid_dim = vid_dim if vertical else vid_dim[::-1]
        print(vid_dim)
        print(vertical)
        if args.square:
            vid_dim = tuple([np.max(vid_dim)]*2)
        out = cv2.VideoWriter(
            vid_dir+temp_output_fn,
            # cv2.cv.CV_FOURCC('m','p','4','v'),
            cv2.VideoWriter_fourcc('m','p','4','v'),
            fps,
            # vid_dim if vertical else vid_dim[::-1],
            vid_dim,
            )
    if rotate and vertical:
        print("rotating "+vid_name)
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
    # print(vid_size, vid_dim)
    # if rotate and vertical:
        # print("a")
    x_diff, y_diff = (vid_dim[1]-vid_size[0])//2,(vid_dim[0]-vid_size[1])//2
    if x_diff<0 or y_diff<0:
        x_diff, y_diff = (vid_dim[0]-vid_size[0])//2,(vid_dim[1]-vid_size[1])//2

    # probabilistically extend a clip to meet frame quota
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
        if rotate and vertical:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            # else:
            #     img = cv2.rotate(img, cv2.ROTATE_180)
        # img = img[:,mid_dim-w_dim//2:mid_dim+w_dim//2,:]
        clip_ctr += 1

    # rem_ctr += 1
# except:
#     print("Failed on {}".format(vid_name))
bar.finish()

out.release()

print(vid_dir+temp_output_fn)
# attach audio
vid = VideoFileClip(vid_dir+temp_output_fn)
aud = AudioFileClip(audio_file).set_duration(vid.duration)
vid = vid.set_audio(aud)
vid.write_videofile(
    vid_dir+output_fn,
    audio=True,
    codec="libx264",
    audio_codec="aac")



