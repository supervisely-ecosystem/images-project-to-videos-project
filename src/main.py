import supervisely as sly

import functions as f
import sly_globals as g

from supervisely import handle_exceptions


@sly.timeit
@handle_exceptions(has_ui=False)
def images_project_to_videos_project(api: sly.Api):
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
        # Process dataset (with automatic nested dataset handling if empty)
        custom_data = f.process_dataset_with_nested(
            api, dataset, vid_dataset, custom_data, res_project.id
        )
        api.project.update_custom_data(id=res_project.id, data=custom_data)
        progress.iter_done_report()


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
    images_project_to_videos_project(g.api)


if __name__ == "__main__":
    sly.main_wrapper("main", main)
