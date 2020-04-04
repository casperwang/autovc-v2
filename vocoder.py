#!/usr/bin/env python
# coding: utf-8

import torch
import librosa
import pickle
from synthesis import build_model
from synthesis import wavegen
from params import *
import os

model = build_model().to(device)
checkpoint = torch.load("checkpoint_step001000000_ema.pth", map_location = torch.device(device)) #Using the pretrained WaveNet Vocoder 
model.load_state_dict(checkpoint["state_dict"])

def genspec(pkl_path, write_name, save_dir = "./result_wav/"):
	spect_vc = pickle.load(open(pkl_path, "rb"))
	for spect in spect_vc:
		c = spect[1]
		waveform = wavegen(model, c=c)
		librosa.output.write_wav(save_dir + write_name + '.wav', waveform, sr=16000)

def genall(pkl_dir = "./result_pkl"):
	for (_, _, x) in os.walk(pkl_dir):
		for f in x:
			if f[0] == 'r':
				print("Gen: " + f[ : -4])
				genspec(pkl_dir + '/' + f, f[ : -4])

