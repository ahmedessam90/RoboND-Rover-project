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

### 1-Notebook Analysis

#### 1-Modification of perspect_transform function.  
### a-Add mask image for field of view of camera which is used next to get obstacle map.  
#### 2-Add find_rocks function to get rock location.  


### 2-Autonomous Navigation and Mapping  

#### a-Edits in perception.py  
##### 1-  obs_map=np.absolute(np.float32((threshed)-1))*mask
##### Added to get obstacle map by getting non-navigable pixels and multiplying by mask to get obstacles in field of view of camera

### 2-Update worldmap  
   #### data.worldmap[y_world, x_world, 2] =255  
   #### data.worldmap[obs_y_world, obs_x_world, 0] =255  
   #### nav_pix=data.worldmap[:,:,2]>0  
   #### data.worldmap[nav_pix,0]=0  
#### Navigable pixels is populated in blue and obstacle pixels is populated in red.  
#### The last 2 lines added to prevent overlap between navigable and obstacle pixels.  

## b- Edits in decision.py   
### The code makes the rover track the right wall.The Rover is checked near or far from wall using Max_angle & Max_distance.# Check Rover.nav_angles is not empty
    if Rover.nav_angles.size:
        #Get Maximum distance at Maximum angle from the rover
        Max_angle=np.max(Rover.nav_angles)
        Max_angle_points=np.argmax(Rover.nav_angles)
        MAX_DIST=np.max(Rover.nav_dists[Max_angle_points])
### Maximum angle should still positive to get maximum distance at the right of the rover  
#Max_angle is used to ensure that maximum distance measured is at the right of the Rover
        if Max_angle > 0.8:
            #Check if max distance is greater than 12 ,
            #Steer to the right with minimum angle of 8 and maximum 10
            if MAX_DIST > 12:
### if the maximum angle and maximum distance are greater than certain thershold specified in the code,the rover steer angle is positive
### so it steers to right.  
# Check for Rover.mode status
                if Rover.mode == 'forward': 
                    # Check the extent of navigable terrain
                    if len(Rover.nav_angles) >= Rover.stop_forward:  
                        # If mode is forward, navigable terrain looks good 
                        # and velocity is below max, then throttle 
                        if Rover.vel < Rover.max_vel:
                        # Set throttle value to throttle setting
                            Rover.throttle = Rover.throttle_set
                        else: 
                            Rover.throttle = 0
                        Rover.brake = 0
                        #Right wall is tracked because steer angle is alaways positive
                        Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), 10, 12)
### if maximum angle and maximum distance are less than certain threshold specifed in the code, the rover steer angle is negative so,it ### steers to left
       #Check if rover is near to wall
            #Check Max_distance
            #Steer the rover to left with maximum angle of 6 
            elif MAX_DIST < 8:
                Rover.brake = 0
                Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -6, -2)
                Rover.throttle = 0

        #Check Max_angle
        #Steer the rover to left with maximum angle of 10       
        elif Max_angle < 0.8:

            Rover.brake = 0
            Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -10, -8)
            Rover.throttle = 0
### The rover can get stuck in some regions of the map so, The velocity of rover is checked to know whether it is moving or stuck  
### A counter is used to count number of images the rover is stuck  
### If the counter exceeds 100 so ,the rover is stuck 
### To get out of being stucked, The rover throttle is zero and steer angle is -15  
 # If in a state where want to pickup a rock send pickup command
    if Rover.near_sample and Rover.vel == 0 and not Rover.picking_up:
        Rover.send_pickup = True

    #Check if rover can not move for 100 images so ,it is stuck
    if Rover.vel <0.01 :
        if Rover.count==100 :
            #Get Rover position to check if rover is stuck
            Rover.pos_old=Rover.pos
            Rover.stuck=1
        else:
            Rover.count=Rover.count+1
    elif Rover.vel > 0.6 :
        Rover.count=0

    #If Rover is stuck ,Steer to the left
    #In this code,Rover gets stuck if throttle=0.2 and steer is positive
    #That part of code need to be executed several times before releasing Rover from being stuck
    if (Rover.pos==Rover.pos_old):
        if Rover.stuck==1:
            if Rover.steer > 0 :
                Rover.throttle = 0
                Rover.steer=-15
                Rover.count=0
                Rover.stuck=0
                Rover.throttle = 0

#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

#### a-The Rover maps 48% of the environment with fidelty 54%
#### b-The Rover get stuck in wide palces"keep moving in circles"
#### c-this can be improved by making the rover track the wall "The rover can track the wall by measuring the max distance of navigable pixels to get information about distance from wall"

**Note:
Resolution:1280*720
Graphics quality:Good
FPS:20**
