import os
import copy
import argparse
import random
from shutil import copyfile

parser = argparse.ArgumentParser(description='Script to split data into train, val and test set')
parser.add_argument('--input_dir', help="Input data directory")
parser.add_argument('--output_dir', help="Final directory with train, val and test splits")
args = parser.parse_args()

train_dir = os.path.join(args.output_dir, "train")
val_dir = os.path.join(args.output_dir, "valid")
test_dir = os.path.join(args.output_dir, "test")

os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

for class_name in os.listdir(args.input_dir):
    class_path = os.path.join(args.input_dir, class_name)
    for filename in os.listdir(class_path):
        img_path = os.path.join(class_path, filename)
        print(class_name, filename)
        
        prob = random.random()
        if prob <= 0.7:
            train_path = os.path.join(train_dir, class_name)
            os.makedirs(train_path, exist_ok=True)
            train_path = os.path.join(train_path, filename + ".jpeg")
            copyfile(img_path, train_path)
        elif prob <= 0.85:
            val_path = os.path.join(val_dir, class_name)
            os.makedirs(val_path, exist_ok=True)
            val_path = os.path.join(val_path, filename + ".jpeg")
            copyfile(img_path, val_path)
        else:
            test_path = os.path.join(test_dir, class_name)
            os.makedirs(test_path, exist_ok=True)
            test_path = os.path.join(test_path, filename + ".jpeg")
            copyfile(img_path, test_path)
