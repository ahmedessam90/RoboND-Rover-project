import numpy as np
import time

#This is where you can build a decision tree for determining throttle, brake and steer 
# commands based on the output of the perception_step() function

def decision_step(Rover):

    # Implement conditionals to decide what to do given perception data
    # Here you're all set up with some basic functionality but you'll need to
    # improve on this decision tree to do a good job of navigating autonomously!

    # Example:
    # Check Rover.nav_angles is not empty
    if Rover.nav_angles.size:
        #Get Maximum distance at Maximum angle from the rover
        Max_angle=np.max(Rover.nav_angles)
        Max_angle_points=np.argmax(Rover.nav_angles)
        MAX_DIST=np.max(Rover.nav_dists[Max_angle_points])
        #Data for Debugging
        print('Maximum_angle=',Max_angle)
        print('Maximum distance=',MAX_DIST)
        print('Number of nav. points=',len(Rover.nav_angles))
        print('Rover mode',Rover.mode)
        print ('Count=',Rover.count)

        #Check if Rover is near or far from wall using Max_angle & Max_distance
        #This code makes the rover track the right wall

        #Check if Rover is far from wall
        #Max_angle is used to ensure that maximum distance measured is at the right of the Rover
        if Max_angle > 0.8:
            #Check if max distance is greater than 12 ,
            #Steer to the right with minimum angle of 8 and maximum 10
            if MAX_DIST > 12:
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
                        
                # If there's a lack of navigable terrain pixels then go to 'stop' mode
                    elif len(Rover.nav_angles) < Rover.stop_forward:
                    # Set mode to "stop" and hit the brakes!
                        Rover.throttle = 0
                    # Set brake to stored brake value
                        Rover.brake = Rover.brake_set
                        Rover.steer = 0
                        Rover.mode = 'stop'

             # If we're already in "stop" mode then make different decisions
                elif Rover.mode == 'stop':
            # If we're in stop mode but still moving keep braking
                    if Rover.vel > 0.2:
                        Rover.throttle = 0
                        Rover.brake = Rover.brake_set
                        Rover.steer = 0
            # If we're not moving (vel < 0.2) then do something else
                    elif Rover.vel <= 0.2:
                # Now we're stopped and we have vision data to see if there's a path forward
                        if len(Rover.nav_angles) < Rover.go_forward:
                            Rover.throttle = 0
                    # Release the brake to allow turning
                            Rover.brake = 0
                            #Steer to the left
                            Rover.steer = -5 
                # If we're stopped but see sufficient navigable terrain in front then go!
                        elif len(Rover.nav_angles) >= Rover.go_forward:
                    # Set throttle back to stored value
                            Rover.throttle = Rover.throttle_set
                    # Release the brake
                            Rover.brake = 0
                            Rover.steer = np.clip(np.mean(Rover.nav_angles * 180/np.pi), -4, 15)
                            Rover.mode = 'forward'        


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
        
    # Steer the robot to left if on angles is extracted from image
    else:
        Rover.throttle = 0
        Rover.steer = -15
        Rover.brake = 0

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
            
    else:
        Rover.stuck=0
 
    
    return Rover

