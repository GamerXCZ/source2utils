# cmd command: python vmf_convert.py "C:\path\to\vmf\file.vmf"

import re, sys, os

INPUT_FILE_EXT = '.vmf'
# this leads to the root of the game folder, i.e. dota 2 beta/content/dota_addons/, make sure to remember the final slash!!
PATH_TO_GAME_CONTENT_ROOT = ""
PATH_TO_CONTENT_ROOT = ""
    
print('Source 2 .vmf Prepper! EXPERIMENTAL!! By caseytube via Github')
print('Converts .vmf files to be ready for Source 2 by fixing materials')
print('--------------------------------------------------------------------------------------------------------')

filename = sys.argv[1]
convertedFilename = filename.replace('.vmf', '') + 'Converted.vmf'
if not os.path.exists(filename):
    print("input file doesn't exist")
    quit()

print('Importing', os.path.basename(filename))
global classnameVar
classnameVar = ""
with open(convertedFilename, 'w') as convFile:
    with open(filename, 'r') as vmfFile:
        for line in vmfFile.readlines():
            splitLine = line.replace('"', '').replace("'", "").split()
            last = len(splitLine) - 1
            if "\"classname\"" in line:
                classnameVar = splitLine[last]
                print('Checking ' + str(classnameVar) + ' entity.')
			
            if "\"uaxis\"" in line:
                oldVar = splitLine[last]
                newVar = float(oldVar) * 32
                print('uaxis: ' + str(oldVar) + ' -> ' + str(newVar))
                newLine = line.replace(str(oldVar), str(newVar))
                convFile.write(newLine)
            elif "\"vaxis\"" in line:
                oldVar = splitLine[last]
                newVar = float(oldVar) * 32
                print('vaxis: ' + str(oldVar) + ' -> ' + str(newVar))
                newLine = line.replace(str(oldVar), str(newVar))
                convFile.write(newLine)
            elif "\"uniformscale\"" in line:
                oldVar = splitLine[last]
                newLine = line.replace("uniformscale", "scales")
                newLine = newLine.replace(str(oldVar), str(oldVar) + " " + str(oldVar) + " " + str(oldVar))
                convFile.write(newLine)
            elif "\"fog_volume\"" in line:
                newLine = line.replace("fog_volume", "env_volumetric_fog_volume")
                print('fog_volume -> env_volumetric_fog_volume')
                convFile.write(newLine)
            elif "\"env_fog_controller\"" in line:
                newLine = line.replace("env_fog_controller", "env_volumetric_fog_controller")
                print('env_fog_controller -> env_volumetric_fog_controller')
                convFile.write(newLine)
            elif "\"fogend\"" in line:
                newLine = line.replace("fogend", "FadeInEnd")
                print('Fixing "fogend" property...')
                convFile.write(newLine)
            elif "\"fogstart\"" in line:
                newLine = line.replace("fogstart", "FadeInStart")
                print('Fixing "fogstart" property...')
                convFile.write(newLine)
            elif "\"fogmaxdensity\"" in line:
                newLine = line.replace("fogmaxdensity", "FogStrength")
                print('Fixing "fogmaxdensity" property...')
                convFile.write(newLine)
            elif "\"fogenable\"" in line:
                oldVar = splitLine[last]
                newVar = int(oldVar) ^ 1
                newLine = line.replace("fogenable", "StartDisabled")
                print('Fixing "fogenable" property...')
                newLine = newLine.replace(str(oldVar), str(newVar))
                convFile.write(newLine)
            elif "\"foglerptime\"" in line:
                newLine = line.replace("foglerptime", "FadeSpeed")
                print('Fixing "foglerptime" property...')
                convFile.write(newLine)
            elif "\"env_sun\"" in line:
                newLine = line.replace("env_sun", "env_sky")
                print('env_sun -> env_sky')
                convFile.write(newLine)
            elif "\"info_player_terrorist\"" in line:
                newLine = line.replace("info_player_terrorist", "info_player_start")
                print('info_player_terrorist -> info_player_start')
                convFile.write(newLine)
            elif "\"info_player_counterterrorist\"" in line:
                newLine = line.replace("info_player_counterterrorist", "info_player_start")
                print('info_player_counterterrorist -> info_player_start')
                convFile.write(newLine)
            elif "\"game_player_equip\"" in line:
                newLine = line.replace("game_player_equip", "info_hlvr_equip_player")
                print('game_player_equip -> info_hlvr_equip_player')
                convFile.write(newLine)
            elif "\"info_teleport_destination\"" in line:
                newLine = line.replace("info_teleport_destination", "point_teleport")
                print('info_teleport_destination -> point_teleport')
                convFile.write(newLine)
            elif "\"_inner_cone\"" in line:
                convFile.write(line)
                newLine = line.replace("_inner_cone", "original_innerconeangle")
                print('Fixing "_inner_cone" property...')
                convFile.write(newLine)
            elif "\"_cone\"" in line:
                convFile.write(line)
                newLine = line.replace("_cone", "original_outerconeangle")
                print('Fixing "_cone" property...')
                convFile.write(newLine)
            elif "\"_linear_attn\"" in line:
                convFile.write(line)
                newLine = line.replace("_linear_attn", "original_attenuation1")
                print('Fixing "_linear_attn" property...')
                convFile.write(newLine)
            elif "\"_quadratic_attn\"" in line:
                convFile.write(line)
                newLine = line.replace("_quadratic_attn", "original_attenuation2")
                print('Fixing "_quadratic_attn" property...')
                convFile.write(newLine)
            elif "\"_lightHDR\"" in line:
                print('Skipping "_lightHDR" property...')
            elif "\"_lightscaleHDR\"" in line:
                print('Skipping "_lightscaleHDR" property...')
            elif "\"_light\"" in line:
                convFile.write(line)
                oldVar = line.replace('"', '').replace("'", "").replace("_light", "").replace("	 ", "").replace("\n", "")
                print('Fixing "_light" property...')
                R, G, B, A = oldVar.split(' ', 4)
                newA = float(A) * 0.0039215686274509803921568627451
                newLine = line.replace("_light", "original_color")
                newLine = newLine.replace(str(oldVar), str(R) + " " + str(G) + " " + str(B))
                convFile.write(newLine)
                newLine = line.replace("_light", "original_brightness")
                newLine = newLine.replace(str(oldVar), str(newA))
                convFile.write(newLine)
            elif "\"spawnflags\"" in line:
                if "light_spot" in classnameVar:
                    oldVar = splitLine[last]
                    newVar = int(oldVar) ^ 1
                    newLine = line.replace("spawnflags", "enabled")
                    print('Fixing "spawnflags" property for ' + classnameVar + ' entity...')
                    newLine = newLine.replace(str(oldVar), str(newVar))
                    convFile.write(newLine)
            else:
                convFile.write(line)
