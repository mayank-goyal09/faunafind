from ultralytics import YOLO
import os

# 1. This command 'magically' downloads the 10MB dataset 
# It includes Buffalo, Elephant, Rhino, and Zebra.
# It saves it to a folder called 'datasets/african-wildlife'
from ultralytics.utils.downloads import download
url = 'https://github.com/ultralytics/assets/releases/download/v0.0.0/african-wildlife.zip'
download(url, dir='data/')

print("🚀 Dataset downloaded and unzipped successfully!")