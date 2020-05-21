import parser
import argparse
import os
import json
import subprocess
from subprocess import run

parser = argparse.ArgumentParser(description='Download images')
parser.add_argument('--input', type=str, help='Json file', required=True)
parser.add_argument('--output_dir', type=str, help='Output dir for image data', default="")
args = parser.parse_args()

if args.output_dir == "":
    filename , extension = args.input.split(".json")
    args.output_dir = "./" + filename
    os.makedirs(args.output_dir, exist_ok=True)

if os.path.isdir(args.output_dir) == False:
    print("Directory does not exist")
    exit(1)

if os.path.exists(args.input) == False:
    print("Json file does not exist")
    exit(1)

with open(args.input) as json_file:
    data = json.load(json_file)


    for i in data.keys():
        link = data[i]['image_link']
        cmd = "wget " + link + " --directory-prefix " + args.output_dir
        proc = run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        broken_link = link.split("/")
        print("Downloaded image with id ",i)
        cmd = "mv " + args.output_dir+"/"+broken_link[-1] + " " + args.output_dir+"/"+i
        proc = run(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)