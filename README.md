<div align="center" markdown>
<img src="https://user-images.githubusercontent.com/106374579/182890521-18378f94-eaea-42f0-b438-1a10ffcfb6ca.png"/>



# Images project to videos project

<p align="center">
  <a href="#Overview">Overview</a> •
  <a href="#How-To-Use">How To Use</a> •
  <a href="#Results">Results</a> 
</p>

[![](https://img.shields.io/badge/supervisely-ecosystem-brightgreen)](https://ecosystem.supervisely.com/apps/supervisely-ecosystem/images-project-to-videos-project)
[![](https://img.shields.io/badge/slack-chat-green.svg?logo=slack)](https://supervisely.com/slack)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/supervisely-ecosystem/images-project-to-videos-project)
[![views](https://app.supervisely.com/img/badges/views/supervisely-ecosystem/images-project-to-videos-project.png)](https://supervisely.com)
[![runs](https://app.supervisely.com/img/badges/runs/supervisely-ecosystem/images-project-to-videos-project.png)](https://supervisely.com)

</div>

# Overview

Transforms supervisely **images** project to supervisely **videos** project.


Application key points:  
- The application has a technical tag `object_id` (applicable only: to an object, possible value: Number), all objects marked with this tag with a specific ID will belong in the video to object with the ID number specified in the tag value
- Backward compatible with [Videos project to images project](https://ecosystem.supervisely.com/apps/turn-video-project-into-images) or man
- Result project name format: `{original_project_name}(videos)`
- Images in dataset must be the **same size** (you can use [`Resize images`](https://app.supervisely.com/ecosystem/apps/resize-images)), otherwise images that will not match resolution size of the first image in the dataset will ignored.
- Customize FPS
 
# How To Use 

1. Add [Images project to videos project](https://ecosystem.supervisely.com/apps/images-project-to-videos-project) to your team from Ecosystem.

<img data-key="sly-module-link" data-module-slug="supervisely-ecosystem/images-project-to-videos-project" src="https://i.imgur.com/yvK4ij7.png" width="350px" style='padding-bottom: 20px'/>  

2. Run app from the context menu of **Images Project**:

<img src="https://i.imgur.com/eYFZ7sQ.png" width="100%"/>

3. Select frame rate, datasets and press the `Run` button.
 
<div align="center" markdown>
<img src="https://i.imgur.com/HP2nCw4.png" width="500"/>
</div>


# Results

After running the application, you will be redirected to the `Tasks` page.  
Once application processing has finished, your project will be available.  
Click on the `project name` to proceed to it.

<img src="https://i.imgur.com/MRS9CKh.png"/>
