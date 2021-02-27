#!/usr/bin/python
import mediapipe as mp
import cv2
import os, glob
import sys

# Utils
def detect_hand(path):
  image = cv2.imread(path, cv2.IMREAD_COLOR)
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

  mp_hands = mp.solutions.hands
  hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

  results = hands.process(image)

  if results.multi_hand_landmarks:
    hands.close()
    return True

  else:
    hands.close()
    return False

def split_video(path, output_path):
  os.system(f'ffmpeg -i {path} -vf fps=1 {output_path}output%06d.png')

def merge_video(path, frame_path, framerate): 
  os.system(f'''ffmpeg -framerate {framerate} -i {frame_path}output%06d.png {path}''')

def rename_files(path):
  index = 0
  for file in os.scandir(path):
    index += 1
    decimals = 6 - len(str(index))
    
    name = f'{path}output'
    for i in range(decimals):
      name += '0'

    name += str(index)
    name += '.png'

    os.rename(file.path, name)

def clear_dir(dir):
  for file in os.scandir(dir):
      os.remove(file.path)

# Main
def main(input_path, output_path):
  split_video(input_path, 'frames/')

  for file in os.scandir('frames/'):
    if detect_hand(file.path):
      os.remove(file.path)

  rename_files('frames/')
  merge_video(output_path, 'frames/', 2)
  clear_dir('frames/')

if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2])