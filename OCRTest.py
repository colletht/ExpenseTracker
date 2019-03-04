from PIL import image
import pytesseract
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required = True, help = "path to input image to be ORC'd")
ap.add_argument()