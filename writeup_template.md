## Project: Search and Sample Return

**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
Here is an example of how to include an image in your writeup.

*1-Modification of perspect_transform function
*a-Add mask image for field of view of camera which is used next to get obstacle map
*2-Add find_rocks function to get rock location

### Autonomous Navigation and Mapping
#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were

#### a.  obs_map=np.absolute(np.float32((threshed)-1))*mask
*Added to get obstacle map by getting non-navigable pixels and multiplying by mask to get obstacles in field of view of camera

#### b.Update worldmap 
   #### data.worldmap[y_world, x_world, 2] =255
   #### data.worldmap[obs_y_world, obs_x_world, 0] =255
   #### nav_pix=data.worldmap[:,:,2]>0
   #### data.worldmap[nav_pix,0]=0
*Navigable pixels is populated in blue and obstacle pixels is populated in red 
*The last 2 lines added to prevent overlap between navigable and obstacle pixels  

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

#### a-The Rover maps 48% of the environment with fidelty 54%
#### b-The Rover get stuck in wide palces"keep moving in circles"
#### c-this can be improved by making the rover track the wall "The rover can track the wall by measuring the max distance of navigable pixels to get information about distance from wall"

**Note:
Resolution:1280*720
Graphics quality:Good
FPS:20**
