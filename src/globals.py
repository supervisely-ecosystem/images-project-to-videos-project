import os
import supervisely_lib as sly
from supervisely_lib.io.fs import mkdir


my_app = sly.AppService()
api: sly.Api = my_app.public_api

TEAM_ID = int(os.environ['context.teamId'])
WORKSPACE_ID = int(os.environ['context.workspaceId'])
PROJECT_ID = int(os.environ['modal.state.slyProjectId'])
TASK_ID = int(os.environ["TASK_ID"])

logger = sly.logger

project_info = api.project.get_info_by_id(PROJECT_ID)
project_name = project_info.name

datasets = api.dataset.get_list(PROJECT_ID)

storage_dir = my_app.data_dir

img_project_dir = os.path.join(storage_dir, project_name)  # dl
vid_project_dir = os.path.join(storage_dir, "vid_project_dir")  # res

mkdir(img_project_dir, True)
mkdir(vid_project_dir, True)

frame_rate = os.environ['modal.state.frameRate']
