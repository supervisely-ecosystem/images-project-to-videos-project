import cv2
import os
import globals as g
from supervisely_lib.io.fs import mkdir


def start(api, dataset, vid_dataset):
    imgs_path = os.path.join(g.img_project_dir, dataset.name,  'img')
    video_path = os.path.join(g.vid_project_dir, "video", f"{dataset.name}.mp4")
    mkdir(os.path.join(g.vid_project_dir, "video"))

    images_infos = api.image.get_list(dataset.id)
    if len(images_infos) == 0:
        g.my_app.logger.warn(f'There are no images in {dataset.name} dataset')
    image_shape = None
    for idx, image_info in enumerate(images_infos):
        if idx == 0:
            image_shape = (image_info.width, image_info.height)
        elif (image_info.width, image_info.height) != image_shape:
            g.my_app.logger.warn(f'Sizes of images in {dataset.name} dataset are not the same. Check your input data.')
            g.my_app.stop()
            return

    image_names = [image_info.name for image_info in images_infos]
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'vp09'), int(g.frame_rate), image_shape)
    for curr_im_name in image_names:
        curr_im_path = os.path.join(imgs_path, curr_im_name)
        img = cv2.imread(curr_im_path)
        video.write(img)
    video.release()

    video_names = [f"{dataset.name}.mp4"]
    video_paths = [video_path]
    video_info = api.video.upload_paths(vid_dataset.id, names=video_names, paths=video_paths)
    video_info = video_info[0]
    return video_info
