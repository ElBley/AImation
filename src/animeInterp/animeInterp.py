import models
import datas
import argparse
import torch
import torchvision
import torchvision.transforms as TF
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
import time
import os
from math import log10
import numpy as np
import datetime
from utils.config import Config
import sys
import cv2
from utils.vis_flow import flow_to_color
from datas.AniTriplet import pil_loader
import json
from skimage.metrics import peak_signal_noise_ratio as compare_psnr
from skimage.metrics import structural_similarity as compare_ssim


def save_flow_to_img(flow, des):
        f = flow[0].data.cpu().numpy().transpose([1, 2, 0])
        fcopy = f.copy()
        fcopy[:, :, 0] = f[:, :, 1]
        fcopy[:, :, 1] = f[:, :, 0]
        cf = flow_to_color(-fcopy)
        cv2.imwrite(des + '.jpg', cf)


def interpolate( path1, path2, result_path):
    normalize1 = TF.Normalize([0., 0., 0.], [1.0, 1.0, 1.0])
    normalize2 = TF.Normalize([0, 0, 0], [1, 1, 1])
    trans = TF.Compose([TF.ToTensor(), normalize1, normalize2, ])
    revmean = [-x for x in [0., 0., 0.]]
    revstd = [1.0 / x for x in [1, 1, 1]]
    revnormalize1 = TF.Normalize([0.0, 0.0, 0.0], revstd)
    revnormalize2 = TF.Normalize(revmean, [1.0, 1.0, 1.0])
    revNormalize = TF.Compose([revnormalize1, revnormalize2])
    revtrans = TF.Compose([revnormalize1, revnormalize2, TF.ToPILImage()])
    to_img = TF.ToPILImage()

    # model = getattr(models, 'AnimeInterpNoCupy')(None).cuda()
    model = getattr(models, 'AnimeInterp')(None).cuda()
    model = nn.DataParallel(model)
    dict1 = torch.load("checkpoints/anime_interp_full.ckpt")
    model.load_state_dict(dict1['model_state_dict'], strict=False)
    model.eval()


    with torch.no_grad():
        filename_frame_1 = path1
        filename_frame_2 = path2
        output_frame_file_path = result_path
        frame1 = pil_loader(filename_frame_1)
        frame2 = pil_loader(filename_frame_2)
        transform1 = TF.Compose([TF.ToTensor()])
        frame1 = transform1(frame1).unsqueeze(0)
        frame2 = transform1(frame2).unsqueeze(0)
        outputs = model(frame1.cuda(), frame2.cuda(), 0.5)
        It_warp = outputs[0]
        to_img(revNormalize(It_warp.cpu()[0]).clamp(0.0, 1.0)).save(output_frame_file_path)


interpolate("/tmp/animeinterp/frame1.png", "/tmp/animeinterp/frame3.png", "/tmp/animeinterp/generated.png")