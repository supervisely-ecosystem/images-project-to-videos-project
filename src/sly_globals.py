import json
import os

import supervisely as sly
from dotenv import load_dotenv
from supervisely.io.fs import mkdir

if sly.is_development():
    load_dotenv("local.env")
    load_dotenv(os.path.expanduser("~/supervisely.env"))


api: sly.Api = sly.Api.from_env()

TASK_ID = os.environ["TASK_ID"]
TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()
PROJECT_ID = sly.env.project_id()

logger = sly.logger

FRAME_RATE = os.environ["modal.state.frameRate"]
SELECTED_DATASETS = json.loads(
    os.environ["modal.state.selectedDatasets"].replace("'", '"')
)
ALL_DATASETS = os.getenv("modal.state.allDatasets").lower() in ("true", "1", "t")
if ALL_DATASETS:
    SELECTED_DATASETS = [dataset.name for dataset in api.dataset.get_list(PROJECT_ID)]

project_info = api.project.get_info_by_id(PROJECT_ID)
if project_info is None:
    raise RuntimeError("Project {!r} not found".format(project_info.name))
if project_info.type != str(sly.ProjectType.IMAGES):
    raise TypeError(
        "Project type is {!r}, but have to be {!r}".format(
            project_info.type, sly.ProjectType.IMAGES
        )
    )

project_meta_json = api.project.get_meta(project_info.id)
project_meta = sly.ProjectMeta.from_json(project_meta_json)
if "object_id" in [tag.name for tag in project_meta.tag_metas]:
    video_project_meta = project_meta.delete_tag_meta("object_id")
else:
    video_project_meta = project_meta

storage_dir = sly.app.get_data_dir()
work_dir = os.path.join(storage_dir, "work_dir")  # res
mkdir(work_dir, True)
