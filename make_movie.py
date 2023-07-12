import os
import glob

framerate = 5
delete_existing_bool = True

photos_dir = "photos"


def create_movie(dir_path):
    # Create glob pattern
    # ffmpeg -framerate 5 -pattern_type glob -i '/home/sabhijeet/Documents/Arecibo_Atmos_Data_Search/photos/*.jpg' -vf "scale=694:518" -c:v libx264 -pix_fmt yuv420p output.mp4
    # dir_path in example : /home/sabhijeet/Documents/Arecibo_Atmos_Data_Search/photos
    glob_pattern = os.path.join(dir_path, "*.jpg")
    image_filepath = glob.glob(glob_pattern)[0]
    image_filename = os.path.basename(image_filepath)
    video_filename = image_filename.split("_")[0]
    video_filename = video_filename + ".mp4"
    video_output_filepath = os.path.join(dir_path, video_filename)

    if os.path.exists(video_output_filepath) == True:
        if delete_existing_bool == True:
            command = f"rm {video_output_filepath}"
            os.system(command)
        else:
            return


    command = f"ffmpeg -framerate {framerate} -pattern_type glob -i '{glob_pattern}' -vf 'scale=694:518' -c:v libx264 -pix_fmt yuv420p {video_output_filepath}"
    os.system(command)

# Example usage
dir_paths = []

for root, dirs, files in os.walk(photos_dir):
    jpg_files = []
    if files != []:
        for file in files:
            if file.lower().endswith('.jpg'):
                jpg_files.append(file)
        if jpg_files != []:
            dir_paths.append(root)


for dir_path in dir_paths:
    create_movie(dir_path)
