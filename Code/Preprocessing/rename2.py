import os
path = '/Users/rutwijdaptardar/Desktop/darkflow-master/dataset/Cars'
files = os.listdir(path)

i=568;
for i, file in enumerate(files):
    os.rename(os.path.join(path, file), os.path.join(path, ''.join([str(i), '.jpg'])))
    i=i+1