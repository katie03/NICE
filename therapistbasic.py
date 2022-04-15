#This program sets up the eye tracker, records and saves eye tracking data, and runs the stimulus program.


# If you need to use a screen units other than 'pix', which we do not recommend as the gaze coordinates
# returned by pylink is in 'pix' units, please make sure to properly set the size of the cursor and the
# position of the gaze. However, the calibration/validation routine should work fine regardless of the
# screen units.

# import libraries
from __future__ import division
from psychopy.hardware.emulator import launchScan

from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy

import pylink, numpy, os, random, sys, time

from psychopy import sound, visual, core, gui, event, monitors

from playsound import playsound 

from psychopy.sound import Microphone

from psychopy.preferences import prefs

#from stimulus2 import sessionStartEnd #importing stimulus program

import os


#### Get subject info with GUI ########################################################
participant = {'participant':'', 'therapist or patient': ['therapist', 'patient']} #participant number and if parent or child

dlg = gui.DlgFromDict(dictionary=participant, title='participant')
if dlg.OK == False:
    core.quit()  # user pressed cancel

expName = u'Hyperscan - eyecontact'
if participant['therapist or patient'] == 'therapist':
    expInfo = {'participant':'hyperscan_' + participant['participant'] + 't', 'condition': 1, 'TR': 1.000, 'volumes': 5, 'sync':'5', 'ON': 20, 'OFF': 20, 'EyeTracking?': False}
else:
    expInfo = {'participant':'hyperscan_' + participant['participant'] + 'p', 'condition': 1, 'TR': 1.000, 'volumes': 5, 'sync':'5', 'ON': 20, 'OFF': 20, 'EyeTracking?': False}


dlg = gui.DlgFromDict(dictionary=expInfo, title=expName, order=['participant', 'condition', 'TR', 'volumes', 'sync'])
if dlg.OK == False:
    core.quit()  # user pressed cancel


#### Checks if eye-tracking - if not, will not connect to eye-tracker
if expInfo['EyeTracking?'] == True:
    dummyMode = False # If in Dummy Mode, press ESCAPE to skip calibration/validataion
else:
    dummyMode = True


#### Initialize custom graphics for camera setup & drift correction ##################
scnWidth, scnHeight = (1920, 100)

# you MUST specify the physical properties of your monitor first, otherwise you won't be able to properly use
# different screen "units" in psychopy
mon = monitors.Monitor('testMonitor', width=20.0, distance=132.3) #in cm
mon.setSizePix((scnWidth, scnHeight))
win = visual.Window((scnWidth, scnHeight), monitor=mon, color= 'black', units='pix', allowStencil=True)


#### settings for launchScan:
MR_settings = {
    'TR': expInfo['TR'],    # duration (sec) per whole-brain volume
    'volumes': expInfo['volumes'],   # number of whole-brain 3D volumes per scanning run
    'sync': expInfo['sync'],    # character to use as the sync timing event; assumed to come at start of a volume
    'skip':0,       # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
    }


duration = expInfo['volumes'] * expInfo['TR']
on_dur = expInfo['ON'] *  expInfo['TR']
off_dur = expInfo['OFF'] *  expInfo['TR']
repeats = int(expInfo['volumes']/(expInfo['ON']+expInfo['OFF']))



#### Established a link to the tracker ###############################################
if not dummyMode:
    tk = pylink.EyeLink('100.1.1.1')
else:
    tk = pylink.EyeLink(None)

begin_session = 'session_starts.wav'
end_session = 'session_ends.wav'

#path1= '/Users/katiechen/Downloads/NICE'
#os.chdir(path1)
#begin_session = sound.Sound('session_starts.wav')
'''end_session = sound.Sound('session_ends.wav', stereo=True, hamming=True)
end_session.setVolume(1.0)
end_session.setSound('session_ends.wav', secs=2, hamming=True)'''
'''song1= sound.Sound('session_starts.wav', stereo = True, hamming = True)
song1.setVolume(1.0)

song2= sound.Sound('session_ends.wav')
song2.setVolume(1.0)'''

#song3= sound.Sound('close_eyes.wav')
#This function gives instructions for the therapist/patient conversation 
def sessionStartEnd(participant_no, win,on_dur, off_dur, condition_no, duration, video):
    '''path1='/Users/katiechen/Downloads/NICE'
    os.chdir(path1)
    session_starts = sound.Sound('session_starts.wav', stereo = False)
    session_ends = sound.Sound('session_ends.wav', stereo = False)'''
    #abort mechanism for if need to stop in the middle
    #aborted = False
    if condition_no == 1: #1: eyeopentask
        #win.winHandle.minimize()

        # play "open your eyes" command followed by 
        playsound(begin_session)
        #session_starts.play()
        #time = 3
        #song2.play()

        # wait for on_dur seconds
        clock = core.Clock()
        while(clock.getTime() < duration):
            if event.getKeys(['q']):
                aborted = True
                return aborted
            elif event.getKeys(['escape']):
                win.close()
                core.quit()
                
        # play "close your eyes" command
        #song2.pause()
        playsound(end_session)
        session_ends.play()
    
        clock = core.Clock()
        while(clock.getTime() < time):
            if event.getKeys(['q']):
                aborted = True
                return aborted
            elif event.getKeys(['escape']):
                win.close()
                core.quit()
        
    else:
        print("Condition must be 1")
    return False


#### DEFINE FUNCTION TO RECORD - INCLUDES STIMULUS PROGRAM

def runTrial(window, mr_settings, trial_index, on, off, reps):

    # for conditions that include video replay, will load video for replay
    vid = None #will pass None to stim program if not replay condition
    if trial_index > 3:
        vid = load_video(participant['participant'], trial_index, window, participant['therapist or child'])

    # take the tracker offline
    tk.setOfflineMode()
    pylink.pumpDelay(50)

    # record_status_message : show some info on the host PC
    tk.sendCommand("record_status_message 'Starting Recording'")

    # drift check
    #try:
    #    err = tk.doDriftCorrect(int(scnWidth)/2, int(scnHeight)/2,1,1)
    #except:
    #    tk.doTrackerSetup()

    # uncomment this line to read out calibration/drift-correction results
    #print tk.getCalibrationMessage()

    # start recording
    tk.setOfflineMode()
    pylink.pumpDelay(50)
    error = tk.startRecording(1,1,1,1)
    pylink.pumpDelay(100) # wait for 100 ms to make sure data of interest is recorded

    #determine which eye(s) are available
    eyeTracked = tk.eyeAvailable()
    if eyeTracked==2: eyeTracked = 1

    # launch: operator selects Scan or Test (emulate); see API documentation

    vol = launchScan(window, mr_settings, globalClock=core.Clock())

    # send the standard "TRIALID" message to mark the start of a trial
    # see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration
    tk.sendMessage('TRIALID %d' % trial_index)

    if participant['therapist or patient'] == 'therapist':
        aborted = sessionStartEnd(participant['participant'], window, on, off, trial_index, duration, vid) #indicates if stimulus program aborts
    else:
        aborted = sessionStartEnd(participant['participant'], window, on, off, trial_index, duration, vid) #indicates if stimulus program aborts

    if aborted == True: #if the condition was aborted, the trial will be repeated
        trial = trial_index
        tk.sendMessage('TRIAL_ABORTED %d' % trial_index)
    else:
        trial = trial_index +1

    #mark end of trail in EDF file
    tk.sendMessage('TRIAL_RESULT 0')
    tk.stopRecording() # stop recording

    # send over the standard 'TRIAL_RESULT' message to mark the end of trial
    # see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration

    return trial


trial = expInfo['condition'] #trial number is based on condition number in the GUI dialogue - allows to start from any condition

while trial <= 6:

    #### STEP III: Open an EDF data file EARLY ####################################################
    dataFolder = os.getcwd() + '/edfData/'
    if not os.path.exists(dataFolder): os.makedirs(dataFolder)

    if participant['therapist or patient'] == 'therapist':
        dataFileName = participant['participant'] +'t' + str(trial) + '.EDF'
    else:
        dataFileName = participant['participant'] +'p' + str(trial) + '.EDF'

    # Note that for Eyelink 1000/II, the file name cannot exceeds 8 characters
    # we need to open eyelink data files early so as to record as much info as possible
    tk.openDataFile(dataFileName)

    # add personalized header (preamble text)
    tk.sendCommand("add_file_preamble_text 'Hyperscan version 2'")

    # this functional calls SR's custom calibration routin "EyeLinkCoreGraphicsPsychopy.py"
    genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
    pylink.openGraphicsEx(genv)


    #### STEP V: Set up the tracker ###############################################################
    # we need to put the tracker in offline mode before we change its configrations
    tk.setOfflineMode()
    # sampling rate, 250, 500, 1000, or 2000, won't work for EyeLInk II
    tk.sendCommand('sample_rate 500')

    # inform the tracker the resolution of the subject display
    # [see Eyelink Installation Guide, Section 8.4: Customizing Your PHYSICAL.INI Settings ]
    tk.sendCommand("screen_pixel_coords = 0 0 %d %d" % (scnWidth-1, scnHeight-1))

    # stamp display resolution in EDF data file for Data Viewer integration
    # [see Data Viewer User Manual, Section 7: Protocol for EyeLink Data to Viewer Integration]
    tk.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (scnWidth-1, scnHeight-1))


    # specify the calibration type, H3, HV3, HV5, HV13 (HV = horiztonal/vertical),
    tk.sendCommand("calibration_type = HV5") # tk.setCalibrationType('HV9') also works, see the Pylink manual

    # specify the proportion of subject display to calibrate/validate
    tk.sendCommand("calibration_area_proportion 0.85 0.85")
    tk.sendCommand("validation_area_proportion  0.85 0.85")

    # allows using buttons on the EyeLink Host PC gamepad to accept calibration/dirft check target, so you
    # do not need to press keys on the keyboard to initiate/accept calibration
    tk.sendCommand("button_function 1 'accept_target_fixation'")

    # data stored in data file and passed over the link (online)
    # [see Eyelink User Manual, Section 4.6: Settting File Contents]

    # the model of the tracker, 1-EyeLink I, 2-EyeLink II, 3-Newer models (100/1000Plus/DUO)
    eyelinkVer = tk.getTrackerVersion()

    #turn off scenelink camera stuff (EYeLInk II only)
    if eyelinkVer == 2:
        tk.sendCommand("scene_camera_gazemap = NO")

    # Set the tracker to parse Events using "GAZE" (or "HREF") data
    tk.sendCommand("recording_parse_type = GAZE")

    # Online parser configuration: 0-> standard/coginitve, 1-> sensitive/psychophysiological
    # the Parser for EyeLink I is more conservative, see below
    # [see Eyelink User Manual, Section 4.3: EyeLink Parser Configuration]
    if eyelinkVer>=2:
        tk.sendCommand('select_parser_configuration 0')
    else:
        tk.sendCommand("saccade_velocity_threshold = 35")
        tk.sendCommand("saccade_acceleration_threshold = 9500")

    # get Host tracking software version #
    hostVer = 0
    if eyelinkVer == 3:
        tvstr  = tk.getTrackerVersionString()
        vindex = tvstr.find("EYELINK CL")
        hostVer = int(float(tvstr[(vindex + len("EYELINK CL")):].strip()))

    # specify the EVENT and SAMPLE data that are stored in EDF or retrievable from the Link
    # see sectin 4.6 of the EyeLink user manual, software version > 4 adds remote tracking (and thus HTARGET)
    tk.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
    if hostVer >= 4:
        tk.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,GAZERES,PUPIL,HREF,AREA,STATUS,HTARGET,INPUT")
    else:
        tk.sendCommand("file_sample_data  = LEFT,RIGHT,GAZE,GAZERES,PUPIL,HREF,AREA,STATUS,INPUT")

    # sample and event data available over the link
    tk.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT")
    if hostVer >= 4:
        tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,PUPIL,HREF,AREA,STATUS,HTARGET,INPUT")
    else:
        tk.sendCommand("link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,PUPIL,HREF,AREA,STATUS,INPUT")



    # show some instructions here.
    msg = visual.TextStim(win, text = 'Press ENTER twice to calibrate the tracker\nPress Esc if not eye-tracking')
    msg.draw()
    win.flip()
    event.waitKeys()

    # set up the camera and calibrate the tracker at the beginning of each block
    tk.doTrackerSetup()


    #### STEP VIII: The real experiment starts here ##########################################

    #runTrial will run a stimulu trial and will return the next trial's ID
    #if aborted, will run with the same ID again
    print ("trial before" + str(trial))
    trial = runTrial(win, MR_settings,trial, on_dur, off_dur, repeats)
    print ("trial after" + str(trial))


    # close the EDF data file
    tk.setOfflineMode()
    tk.closeDataFile()
    pylink.pumpDelay(50)

    # Get the EDF data and say goodbye
    msg.text= 'Data transferring.....'
    msg.draw()
    win.flip()
    # EDF file is transferred from eye-tracker to this PC
    tk.receiveDataFile(dataFileName, dataFolder + dataFileName)
    
    trial = 7

#after done with all trials
#close the link to the tracker
tk.close()

# close the graphics
win.close()
core.quit()