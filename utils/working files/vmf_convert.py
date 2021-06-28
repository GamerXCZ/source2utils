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

with open(convertedFilename, 'w') as convFile:
    with open(filename, 'r') as vmfFile:
        for line in vmfFile.readlines():
            splitLine = line.replace('"', '').replace("'", "").split()
            last = len(splitLine) - 1
            
            if "uaxis" in line:
                oldVar = splitLine[last]
                newVar = float(oldVar) * 32
                print('uaxis:' + str(oldVar) + '->' + str(newVar))
                newLine = line.replace(str(oldVar), str(newVar))
                convFile.write(newLine)
            elif "vaxis" in line:
                oldVar = splitLine[last]
                newVar = float(oldVar) * 32
                print('vaxis:' + str(oldVar) + '->' + str(newVar))
                newLine = line.replace(str(oldVar), str(newVar))
                convFile.write(newLine)
            elif "uniformscale" in line:
                oldVar = splitLine[last]
                newLine = line.replace("uniformscale", "scales")
                newLine = newLine.replace(str(oldVar), str(oldVar) + " " + str(oldVar) + " " + str(oldVar))
                convFile.write(newLine)
            elif "fog_volume" in line:
                newLine = line.replace("fog_volume", "env_volumetric_fog_volume")
                print('fog_volume -> env_volumetric_fog_volume')
                convFile.write(newLine)
            elif "env_fog_controller" in line:
                newLine = line.replace("env_fog_controller", "env_volumetric_fog_controller")
                print('env_fog_controller -> env_volumetric_fog_controller')
                convFile.write(newLine)
            elif "fogend" in line:
                newLine = line.replace("fogend", "FadeInEnd")
                print('Fixing "fogend" property...')
                convFile.write(newLine)
            elif "fogstart" in line:
                newLine = line.replace("fogstart", "FadeInStart")
                print('Fixing "fogstart" property...')
                convFile.write(newLine)
            elif "fogmaxdensity" in line:
                newLine = line.replace("fogmaxdensity", "FogStrength")
                print('Fixing "fogmaxdensity" property...')
                convFile.write(newLine)
            elif "fogenable" in line:
                oldVar = splitLine[last]
                newVar = int(oldVar) ^ 1
                newLine = line.replace("fogenable", "StartDisabled")
                print('Fixing "fogenable" property...')
                newLine = newLine.replace(str(oldVar), str(newVar))
                convFile.write(newLine)
            elif "foglerptime" in line:
                newLine = line.replace("foglerptime", "FadeSpeed")
                print('Fixing "foglerptime" property...')
                convFile.write(newLine)
            elif "env_sun" in line:
                newLine = line.replace("env_sun", "env_sky")
                print('env_sun -> env_sky')
                convFile.write(newLine)
            elif "info_player_terrorist" in line:
                newLine = line.replace("info_player_terrorist", "info_player_start")
                print('info_player_terrorist -> info_player_start')
                convFile.write(newLine)
            elif "info_player_counterterrorist" in line:
                newLine = line.replace("info_player_counterterrorist", "info_player_start")
                print('info_player_counterterrorist -> info_player_start')
                convFile.write(newLine)
            elif "game_player_equip" in line:
                newLine = line.replace("game_player_equip", "info_hlvr_equip_player")
                print('game_player_equip -> info_hlvr_equip_player')
                convFile.write(newLine)
            else:
                convFile.write(line)
