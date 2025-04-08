import supervisely as sly
from supervisely.video_annotation.key_id_map import KeyIdMap

import functions as f
import sly_globals as g


@g.my_app.callback("images_project_to_videos_project")
@sly.timeit
def images_project_to_videos_project(api: sly.Api, task_id, context, state, app_logger):
    res_project = api.project.create(
        g.WORKSPACE_ID,
        f"{g.project_info.name}(videos)",
        sly.ProjectType.VIDEOS,
        change_name_if_conflict=True,
    )
    api.project.update_meta(res_project.id, g.video_project_meta.to_json())
    custom_data = {"original_images": {}}
    progress = sly.Progress(f"Processing videos:", len(g.SELECTED_DATASETS))
    for dataset_name in g.SELECTED_DATASETS:
        dataset = api.dataset.get_info_by_name(g.PROJECT_ID, dataset_name)
        vid_dataset = api.dataset.create(
            res_project.id, dataset.name, change_name_if_conflict=True
        )
        video_info, images_ids, image_shape, custom_data = f.process_video(
            api, dataset, vid_dataset, custom_data
        )
        if video_info is None:
            continue
        api.project.update_custom_data(id=res_project.id, data=custom_data)
        f.process_annotations(
            api, g.project_meta, dataset, video_info, images_ids, image_shape
        )
        progress.iter_done_report()

    g.my_app.stop()


def main():
    sly.logger.info(
        "Script arguments",
        extra={
            "TEAM_ID": g.TEAM_ID,
            "TASK_ID": g.TASK_ID,
            "WORKSPACE_ID": g.WORKSPACE_ID,
            "PROJECT_ID": g.PROJECT_ID,
        },
    )
    g.my_app.run(initial_events=[{"command": "images_project_to_videos_project"}])


if __name__ == "__main__":
    sly.main_wrapper("main", main)
