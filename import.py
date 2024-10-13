import maya.cmds as cmds
import maya.mel as mel
import os

cmds.currentUnit(time='ntsc')
cmds.playbackOptions(min=1, max=9999)
cmds.playbackOptions(animationStartTime=1, animationEndTime=9999)

# Specify the directory containing your .anm files
anm_directory = r'D:\Program Files\League Modding\Thresh\assets\characters\thresh\skins\skin17\animations'

# Get a list of all .anm files
anm_files = [f for f in os.listdir(anm_directory) if f.endswith('.anm')]

# Sort the files if necessary
anm_files.sort()

# Initialize the starting frame
current_frame = 1

# List to hold clip information
clips = []

# Loop through each .anm file
for anm_file in anm_files:
    file_path = os.path.join(anm_directory, anm_file)
    clip_name = os.path.splitext(anm_file)[0]
    
    # Set the current time to current_frame
    cmds.currentTime(current_frame, edit=True)
    
    # Import the .anm file starting from the current frame
    try:
        cmds.file(file_path, i=True, type="League of Legends: ANM", ignoreVersion=True)
    except Exception as e:
        cmds.warning('Failed to import "{}". Error: {}'.format(anm_file, e))
        continue
    
    # Get all joints in the scene
    joints = cmds.ls(type='joint')
    if not joints:
        cmds.warning('No joints found in the scene.')
        continue
    
    # Determine the length of the animation by querying keyframes on the joints
    key_times = cmds.keyframe(joints, query=True, timeChange=True)
    if key_times:
        # Filter keyframes within the current animation segment
        key_times = [t for t in key_times if t >= current_frame]
        if key_times:
            anim_start = min(key_times)
            anim_end = max(key_times)
        else:
            cmds.warning('No keyframes found in the current segment for animation: "{}"'.format(clip_name))
            continue
    else:
        cmds.warning('No keyframes found for animation: "{}"'.format(clip_name))
        continue
    
    # Record clip information
    start_frame = int(current_frame)
    end_frame = int(anim_end)
    clips.append({'name': clip_name, 'start': start_frame, 'end': end_frame})
    
    # Update the current frame for the next animation
    current_frame = end_frame + 1
