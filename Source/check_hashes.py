import os.path
from logic_supervisor import md5
import json

root_root_dir = "C:/Users/JediKnight/Documents/Unreal Projects/ECRPackagedShipping/prod_1.0.0/"
game_dir = os.path.join(root_root_dir, "Windows")
archive = os.path.join(root_root_dir, root_root_dir.split("/")[-2] + ".zip")

if os.path.exists(archive):
    print("Archive", md5(archive))

files = [
    'ECR.exe',
    'ECR/Binaries/Win64/ECR-Win64-Shipping.exe',
]

folders = [
    'ECR/Content/Paks/'
]

result = {}
for file in files:
    fp = os.path.join(game_dir, file)
    hash = md5(fp)
    result[file] = hash

for folder in folders:
    files = os.listdir(os.path.join(game_dir, folder))
    for file in files:
        fp = os.path.join(game_dir, folder, file)
        hash = md5(fp)
        result[os.path.join(folder, file)] = hash

print(json.dumps(result, indent=5))
