import os
import globals as g
import supervisely_lib as sly
from supervisely_lib.io.json import dump_json_file
from supervisely_lib.io.fs import get_file_name, mkdir

from supervisely_lib.video_annotation.video_tag_collection import VideoTag, VideoTagCollection


def start(api, meta, dataset, video_info, key_id, key_id_map):
    anns_path = os.path.join(g.img_project_dir, dataset.name, 'ann')
    mkdir(os.path.join(g.vid_project_dir, "ann"))

    res_ann_path = os.path.join(g.vid_project_dir, "ann", f"{dataset.name}.mp4.json")

    anns = []

    video_objects_col = []
    video_frames_col = []
    video_tags_col = []

    for idx, ann in enumerate(os.listdir(anns_path)):
        ann = sly.Annotation.load_json_file(os.path.join(anns_path, ann), meta)
        anns.append(ann)

        figures = []
        for label in ann.labels:
            video_object = sly.VideoObject(label.obj_class)
            video_objects_col.append(video_object)

            key_id_map.add_object(video_object.key(), key_id)
            key_id += 1

            figure = sly.VideoFigure(video_object, label.geometry, idx)
            key_id_map.add_object(figure.key(), key_id)
            key_id += 1
            figures.append(figure)

        for tag in ann.img_tags:
            pass
            #xx = tag
            #video_tag = VideoTag
#
            #video_tags_col.append(tag)
            #key_id_map.add_tag(video_tag.key(), key_id)
            #key_id += 1


        frame = sly.Frame(idx, figures=figures)
        video_frames_col.append(frame)

    img_size = anns[0].img_size

    video_objects_col = sly.VideoObjectCollection(video_objects_col)
    video_frames_col = sly.FrameCollection(video_frames_col)
    video_tags_col = VideoTagCollection(video_tags_col)

    video_ann = sly.VideoAnnotation(img_size, len(anns), video_objects_col, video_frames_col, video_tags_col)
    key_id_map.add_video(video_ann.key(), key_id)
    key_id += 1
    video_ann_json = video_ann.to_json(key_id_map)
    dump_json_file(video_ann_json, res_ann_path)

   # dump_json_file(key_id_map, os.path.join(g.vid_project_dir, "key_id_map.json"))

    g.api.video.annotation.upload_paths([video_info.id], [res_ann_path], meta)
