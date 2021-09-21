import globals as g
import functions as f
import supervisely_lib as sly
import render_video_from_images
import convert_annotations

from supervisely_lib.io.json import dump_json_file

from supervisely_lib.project.project import Project, OpenMode, Progress
from supervisely_lib.project.video_project import VideoProject
from supervisely_lib.video_annotation.key_id_map import KeyIdMap


@g.my_app.callback("images_project_to_videos_project")
@sly.timeit
def images_project_to_videos_project(api: sly.Api, task_id, context, state, app_logger):
    project_meta = f.download_project(api, g.img_project_dir, g.PROJECT_ID, True)

    res_project = api.project.create(g.WORKSPACE_ID, f"{g.project_name}_video", sly.ProjectType.VIDEOS, change_name_if_conflict=True)
    api.project.update_meta(res_project.id, project_meta.to_json())


    key_id_map = KeyIdMap()
    #project_fs = VideoProject(g.vid_project_dir, OpenMode.READ)
    #project_fs.set_meta(project_meta)

    key_id = 0
    for dataset in g.datasets:
        vid_dataset = api.dataset.create(res_project.id, dataset.name, change_name_if_conflict=True)
        video_info = render_video_from_images.start(api, dataset, vid_dataset)
        convert_annotations.start(api, project_meta, dataset, video_info, key_id, key_id_map)

    g.my_app.stop()


def main():
    sly.logger.info("Script arguments", extra={
        "TEAM_ID": g.TEAM_ID,
        "TASK_ID": g.TASK_ID,
        "WORKSPACE_ID": g.WORKSPACE_ID,
        "PROJECT_ID": g.PROJECT_ID

    })
    g.my_app.run(initial_events=[{"command": "images_project_to_videos_project"}])


if __name__ == '__main__':
    sly.main_wrapper("main", main)
