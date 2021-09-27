import os
import cv2
import globals as g
import supervisely_lib as sly
from supervisely_lib.io.fs import silent_remove
from supervisely_lib.video_annotation.video_tag_collection import VideoTag, VideoTagCollection


def process_video(api, img_dataset, vid_dataset):
    images_infos = api.image.get_list(img_dataset.id, sort='name')
    if len(images_infos) == 0:
        g.my_app.logger.warn(f'There are no images in {img_dataset.name} dataset')
    image_shape = None
    for idx, image_info in enumerate(images_infos):
        if idx == 0:
            image_shape = (image_info.width, image_info.height)
        elif (image_info.width, image_info.height) != image_shape:
            g.my_app.logger.warn(f'Sizes of images in {img_dataset.name} dataset are not the same. Check your input data.')
            g.my_app.stop()
            return

    images_ids = [image_info.id for image_info in images_infos]
    images_paths = [os.path.join(g.work_dir, image_info.name) for image_info in images_infos]
    api.image.download_paths(img_dataset.id, images_ids, images_paths)

    video_path = os.path.join(g.work_dir, f"{vid_dataset.name}.mp4")
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), int(g.FRAME_RATE), image_shape)
    progress = sly.Progress("Processing video frames:", len(images_infos))
    for img_path in images_paths:
        img = cv2.imread(img_path)
        video.write(img)
        silent_remove(img_path)
        progress.iter_done_report()
    video.release()
    video_names = [f"{vid_dataset.name}.mp4"]
    video_paths = [video_path]

    upl_progress = sly.Progress("Uploading video:", 1)
    video_info = api.video.upload_paths(vid_dataset.id, names=video_names, paths=video_paths)
    upl_progress.iter_done_report()

    video_info = video_info[0]
    silent_remove(video_path)
    return video_info, images_ids


def get_object_name_id_map(anns):
    unique_obj_ids = {}
    for ann in anns:
        for label in ann.labels:
            for tag in label.tags:
                tag_names = [tag.name for tag in label.tags]
                if "object_id" in tag_names:
                    if tag.name == "object_id":
                        if label.obj_class.name in unique_obj_ids:
                            if tag.value in unique_obj_ids[label.obj_class.name]:
                                continue
                            else:
                                unique_obj_ids[label.obj_class.name].append(tag.value)
                        else:
                            unique_obj_ids[label.obj_class.name] = [tag.value]
                else:
                    return None
    return unique_obj_ids


def create_id_to_video_objects_map_from_object_name_ids_map(object_name_ids_map):
    video_objects_map = {}
    for obj_class_name, obj_class_ids in object_name_ids_map.items():
        for obj_class_id in obj_class_ids:
            video_object = sly.VideoObject(g.project_meta.get_obj_class(obj_class_name), class_id=obj_class_id)
            video_objects_map[obj_class_id] = video_object
    return video_objects_map


def process_annotations(api, meta, img_dataset, video_info, images_ids):
    ann_infos = api.annotation.download_batch(img_dataset.id, images_ids)
    anns = [sly.Annotation.from_json(x.annotation, meta) for x in ann_infos]

    video_objects_map = None
    video_objects_col = None
    if g.IS_OBJ_ID_TAG is True:
        object_name_ids_map = get_object_name_id_map(anns)
        video_objects_map = create_id_to_video_objects_map_from_object_name_ids_map(object_name_ids_map)
    else:
        video_objects_col = []
    video_frames_col = []
    video_tags_col = []
    progress = sly.Progress("Processing annotations:", len(ann_infos))
    for idx, ann in enumerate(anns):
        figures = []
        for label in ann.labels:
            object_tag_col = []
            vobj_id = None
            for tag in label.tags:
                if tag.name == "object_id":
                    vobj_id = tag.value
                    continue
                if tag.value is not None:
                    video_tag = VideoTag(tag.meta, tag.value)
                else:
                    video_tag = VideoTag(tag.meta)
                object_tag_col.append(video_tag)
            if g.IS_OBJ_ID_TAG is True:
                figure = sly.VideoFigure(video_objects_map[vobj_id], label.geometry, idx, class_id=vobj_id)
            else:
                video_object = sly.VideoObject(label.obj_class, VideoTagCollection(object_tag_col))
                video_objects_col.append(video_object)
                figure = sly.VideoFigure(video_object, label.geometry, idx)
            figures.append(figure)

        for tag in ann.img_tags:
            video_tag = VideoTag(tag.meta, frame_range=[idx, idx])
            video_tags_col.append(video_tag)
        frame = sly.Frame(idx, figures=figures)
        video_frames_col.append(frame)
        progress.iter_done_report()

    img_size = anns[0].img_size
    if g.IS_OBJ_ID_TAG:
        video_objects_col = sly.VideoObjectCollection(list(video_objects_map.values()))
    else:
        video_objects_col = sly.VideoObjectCollection(video_objects_col)

    video_frames_col = sly.FrameCollection(video_frames_col)
    video_tags_col = VideoTagCollection(video_tags_col)
    upl_progress = sly.Progress("Uploading video annotation:", 1)
    video_ann = sly.VideoAnnotation(img_size, len(anns), video_objects_col, video_frames_col, video_tags_col)
    api.video.annotation.append(video_info.id, video_ann)
    upl_progress.iter_done_report()
