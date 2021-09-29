import os
import sys
import glob
from moviepy.editor import VideoFileClip, concatenate_videoclips
import argparse
from random import shuffle, choice

def get_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('--vid_dir', '-v', default='./videos')
    parser.add_argument('--vid_mul', '-vm', default=1, type=int)
    parser.add_argument('--begin', '-b', default='')
    parser.add_argument('--end', '-e', default='')
    parser.add_argument('--shuffle','-s',default=True, action='store_true')
    parser.add_argument('--output', '-o',default='output.mp4')
    parser.add_argument('--vid_len','-vl', default=59.7, type=float)
    parser.add_argument('--fps','-fps', default=30, type=int)
    parser.add_argument('--vertical', default=False, action='store_true')
    parser.add_argument('--vid_limit',default=None, type=int)
    parser.add_argument('--audio', '-a', default='./gimme_trim.m4a')
    parser.add_argument('--square',default=False,action='store_true')
    return parser.parse_args(sys.argv[1:])

if __name__=="__main__":

    args = get_args()

    # clips = glob.glob(args.vid_dir+'/*.MOV')
    clips = glob.glob(f'{args.vid_dir}/*.MOV')
    print(clips)
    shuffle(clips)
    print(clips)
    video_len,clips_ctr = 0,0
    video_clips = [VideoFileClip(clip) for clip in clips]
    video_lens = [video_clip.duration for video_clip in video_clips]
    print(min(video_lens))
    min_video_len = min(video_lens)
    min_video_len = args.vid_len/len(clips)

    montage = []
    for video_clip in video_clips:
        if video_clip.duration > min_video_len:
            clip_start = choice(range(0,int(video_clip.duration-min_video_len)))
        else:
            clip_start = 0
        clip_end = clip_start + min_video_len
        print(clip_start,clip_end)
        montage.append(video_clip.subclip(clip_start,clip_end))
    final_clip = concatenate_videoclips(montage)
    final_clip.write_videofile(f'{args.vid_dir}/output.mp4')

    # while video_len<args.vid_len:
    #     video_clip = VideoFileClip(clips[clips_ctr])

    #     import pdb; pdb.set_trace();
        # clips_ctr = (clips_ctr+1)%len(clips)
        # video_len += 

    # concatenate_videoclips([VideoFileClip(clip) for clip in clips])

    # clip1 = VideoFileClip("myvideo.mp4")
    # clip2 = VideoFileClip("myvideo2.mp4").subclip(50,60)
    # clip3 = VideoFileClip("myvideo3.mp4")





    # final_clip = concatenate_videoclips([clip1,clip2,clip3])
    # final_clip.write_videofile("my_concatenation.mp4")