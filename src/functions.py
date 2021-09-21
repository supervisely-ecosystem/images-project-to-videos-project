import os
import globals as g
import supervisely_lib as sly
from supervisely_lib.io.json import dump_json_file


def download_project(api, save_path, project_id, log_progress=True):
    sly.download_project(api, project_id, save_path, log_progress=log_progress)
    meta_json = sly.json.load_json_file(os.path.join(save_path, 'meta.json'))
    meta = sly.ProjectMeta.from_json(meta_json)
    dump_json_file(meta_json, os.path.join(g.vid_project_dir, "meta.json"))
    return meta
