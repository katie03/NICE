#Stimulus
from psychopy import core, event, visual, sound
from playsound import playsound

#load_video

#This function loads a video into a psychopy MovieStim such that when the video is 
#played, the stimulus is not delayed by the opening and loading of the video.

#participant_no = participant number
#condition_no = condition number
#win = psychopy window
#porc = parent or child

def load_video(participant_no, condition_no, win, porc):

    #videos are loaded either from shared drive W or X depending on if they're in EVE (child) or JUNE (parent)
    #as videos are being recorded and saved locally on PC1 as to not have a network bottleneck during recording
    
    if porc == 'child':
        video_path = 'W:/videos/' + participant_no + '/converted_video/conv_' + participant_no + '_EVE_Parent_' + str(condition_no - 3) + '.mp4'
    else:
        video_path = 'X:/videos/' + participant_no + '/converted_video/conv_' + participant_no + '_JUNE_Child_' + str(condition_no - 3) + '.mp4'

    mov = visual.MovieStim3(win, filename=video_path)
    return mov
        

#eyeOpenClose_child

#This function gives instructions for the tasks of the stimulus for the child

#participant_no = participant number
#win = psychopy window
#on_dur = duration of on task (i.e. open your eyes)
#off_dur = duration of off task (i.e. close your eyes)
#condition_no = condition number
#reps = number of times each series of on-off tasks are repeated
#video = the loaded video - this is None if it's not a replay condition (i.e. conditions 1-3)

open_eyes = sound.Sound('open_eyes.wav', stereo=True, hamming=True)
close_eyes = sound.Sound('close_eyes.wav', stereo=True, hamming=True)
def eyeOpenClose_child(participant_no, win,on_dur, off_dur, condition_no,reps,video):

    #abort mechanism for if need to stop in the middle
    aborted = False
    if condition_no == 1 or condition_no == 2: #1: parent and kid together, 2: parent close eyes first
        win.winHandle.minimize()
        for i in range(reps):

            # play "open your eyes" command
            #playsound('open_eyes.wav', False)
            open_eyes.play()
            
            # wait for on_dur seconds
            clock = core.Clock()
            while(clock.getTime() < on_dur):
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()

            # play "close your eyes" command
            close_eyes.play()
            #playsound('close_eyes.wav', False)

            # wait for off_dur seconds
            clock = core.Clock()
            while(clock.getTime() < off_dur):
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()
        win.winHandle.maximize()
            
    elif condition_no == 3: #3: kids close eyes first
        win.winHandle.minimize()
        for i in range(reps):

            # play "close your eyes" command
            playsound('close_eyes.wav', False)

            # wait off_dur seconds
            clock = core.Clock()
            while(clock.getTime() < off_dur):
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()

            # play "open your eyes" command
            playsound('open_eyes.wav', False)

            # wait on_dur seconds
            clock = core.Clock()
            while(clock.getTime() < on_dur):
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()
        win.winHandle.maximize()
                
    elif condition_no == 4 or condition_no == 5:

        for i in range(reps):

            # play "open your eyes" command
            playsound('open_eyes.wav', False)

            
            # wait for on_dur seconds
            clock = core.Clock()
            while(clock.getTime() < on_dur):
                video.draw()
                win.flip()
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()

            # play "close your eyes" command
            playsound('close_eyes.wav', False)

            # wait for off_dur seconds
            clock = core.Clock()
            while(clock.getTime() < off_dur):
                video.draw()
                win.flip()
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()
        
    elif condition_no == 6: #3: kids close eyes first
        
        for i in range(reps):

            # play "close your eyes" command
            playsound('close_eyes.wav', False)

            # wait off_dur seconds
            clock = core.Clock()
            while(clock.getTime() < off_dur):
                video.draw()
                win.flip()
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()

            # play "open your eyes" command
            playsound('open_eyes.wav', False)

            # wait on_dur seconds
            clock = core.Clock()
            while(clock.getTime() < on_dur):
                video.draw()
                win.flip()
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()
          
    else:
        print("Condition must be between 1 & 6")
    return aborted


#eyeOpenClose_parent

#This function gives instructions for the tasks of the stimulus for the parent

#participant_no = participant number
#win = psychopy window
#on_dur = duration of on task (i.e. open your eyes)
#off_dur = duration of off task (i.e. close your eyes)
#condition_no = condition number
#reps = number of times each series of on-off tasks are repeated
#video = the loaded video - this is None if it's not a replay condition (i.e. conditions 1-3)

def eyeOpenClose_parent(participant_no, win,on_dur, off_dur, condition_no,reps,video):

    #abort mechanism for if need to stop in the middle
    aborted = False
    if condition_no == 1 or condition_no == 3: #1: parent and kid together, 3: kid closes eyes first
        win.winHandle.minimize()
        for i in range(reps):

            # play "open your eyes" command
            playsound('open_eyes.wav', False)

            
            # wait for on_dur seconds
            clock = core.Clock()
            while(clock.getTime() < on_dur):
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()

            # play "close your eyes" command
            playsound('close_eyes.wav', False)

            # wait for off_dur seconds
            clock = core.Clock()
            while(clock.getTime() < off_dur):
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()
        win.winHandle.maximize()
            
    elif condition_no == 2: #2: parent closes eyes first
        win.winHandle.minimize()
        for i in range(reps):

            # play "close your eyes" command
            playsound('close_eyes.wav', False)

            # wait off_dur seconds
            clock = core.Clock()
            while(clock.getTime() < off_dur):
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()

            # play "open your eyes" command
            playsound('open_eyes.wav', False)

            # wait on_dur seconds
            clock = core.Clock()
            while(clock.getTime() < on_dur):
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()
        win.winHandle.maximize()
        
    elif condition_no == 4 or condition_no == 6:

        for i in range(reps):

            # play "open your eyes" command
            playsound('open_eyes.wav', False)

            # wait for on_dur seconds
            clock = core.Clock()
            while(clock.getTime() < on_dur):
                video.draw()
                win.flip()
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()

            # play "close your eyes" command
            playsound('close_eyes.wav', False)

            # wait for off_dur seconds
            clock = core.Clock()
            while(clock.getTime() < off_dur):
                video.draw()
                win.flip()
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()

        
    elif condition_no == 5: 
        
        for i in range(reps):

            # play "close your eyes" command
            playsound('close_eyes.wav', False)

            # wait off_dur seconds
            clock = core.Clock()
            while(clock.getTime() < off_dur):
                video.draw()
                win.flip()
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()

            # play "open your eyes" command
            playsound('open_eyes.wav', False)

            # wait on_dur seconds
            clock = core.Clock()
            while(clock.getTime() < on_dur):
                video.draw()
                win.flip()
                if event.getKeys(['q']):
                    aborted = True
                    return aborted
                elif event.getKeys(['escape']):
                    win.close()
                    core.quit()
        
    else:
        print("Condition must be between 1 & 6")
    return aborted