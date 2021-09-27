import os
import json
import supervisely_lib as sly
from supervisely_lib.io.fs import mkdir


my_app = sly.AppService()
api: sly.Api = my_app.public_api

TEAM_ID = int(os.environ['context.teamId'])
WORKSPACE_ID = int(os.environ['context.workspaceId'])
PROJECT_ID = int(os.environ['modal.state.slyProjectId'])
TASK_ID = int(os.environ["TASK_ID"])

logger = sly.logger

FRAME_RATE = os.environ['modal.state.frameRate']
SELECTED_DATASETS = json.loads(os.environ["modal.state.selectedDatasets"].replace("'", '"'))

project_info = api.project.get_info_by_id(PROJECT_ID)
if project_info is None:
    raise RuntimeError("Project {!r} not found".format(project_info.name))
if project_info.type != str(sly.ProjectType.IMAGES):
    raise TypeError("Project type is {!r}, but have to be {!r}".format(project_info.type, sly.ProjectType.IMAGES))

project_meta_json = api.project.get_meta(project_info.id)
project_meta = sly.ProjectMeta.from_json(project_meta_json)
video_project_meta = project_meta.delete_tag_meta("object_id")

if "object_id" not in [tag.name for tag in project_meta.tag_metas]:
    IS_OBJ_ID_TAG = False
    # vobj_id_tag_meta = sly.TagMeta(name="object_id", value_type=sly.TagValueType.ANY_NUMBER)
    # project_meta = project_meta.add_tag_meta(vobj_id_tag_meta)

storage_dir = my_app.data_dir
work_dir = os.path.join(storage_dir, "work_dir")  # res
mkdir(work_dir, True)
