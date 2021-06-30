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
global classnameVar, saveLines, savingProces, deletingProces
deletingProces = 0
savingProces = 0
classnameVar = ""
saveLines = ""
with open(convertedFilename, 'w') as convFile:
    with open(filename, 'r') as vmfFile:
        for line in vmfFile.readlines():
            splitLine = line.replace('"', '').replace("'", "").split()
            last = len(splitLine) - 1
			
            if 1 == savingProces:
                if "\"classname\"" not in line:
                    saveLines = saveLines + line
                    continue
                
            if "entity\n" == line:
                savingProces = 1
                saveLines = line
                continue
			
            if "\"classname\"" in line:
                classnameVar = splitLine[last]
                if "\"shadow_control\"" in line or "\"env_detail_controller\"" in line or "\"postprocess_controller\"" in line or "\"func_areaportal\"" in line or "\"func_areaportalwindow\"" in line:
                    print(' --> Deleting ' + str(classnameVar) + ' entity.')
                    deletingProces = 1
                    savingProces = 0
                    saveLines = ""
                    continue
                else:
                    print(' --> Checking ' + str(classnameVar) + ' entity.')
                    convFile.write(saveLines)
                    deletingProces = 0
                    savingProces = 0
                    saveLines = ""

            if 1 == deletingProces:
                if "}" == line:
                    deletingProces = 0
                continue

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
            elif "\"info_player_teamspawn\"" in line:
                newLine = line.replace("info_player_teamspawn", "info_player_start")
                print('info_player_teamspawn -> info_player_start')
                convFile.write(newLine)
            elif "\"info_player_deathmatch\"" in line:
                newLine = line.replace("info_player_deathmatch", "info_player_start")
                print('info_player_deathmatch -> info_player_start')
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
                print('Saving "_inner_cone" property...')
                convFile.write(newLine)
            elif "\"_cone\"" in line:
                convFile.write(line)
                newLine = line.replace("_cone", "original_outerconeangle")
                print('Saving "_cone" property...')
                convFile.write(newLine)
            elif "\"_linear_attn\"" in line:
                convFile.write(line)
                newLine = line.replace("_linear_attn", "original_attenuation1")
                print('Saving "_linear_attn" property...')
                convFile.write(newLine)
            elif "\"_quadratic_attn\"" in line:
                convFile.write(line)
                newLine = line.replace("_quadratic_attn", "original_attenuation2")
                print('Saving "_quadratic_attn" property...')
                convFile.write(newLine)
            elif "\"_lightHDR\"" in line:
                print('Skipping "_lightHDR" property...')
            elif "\"_lightscaleHDR\"" in line:
                print('Skipping "_lightscaleHDR" property...')
            elif "\"_light\"" in line:
                convFile.write(line)
                oldVar = line.replace('"', '').replace("'", "").replace("_light", "").replace("	 ", "").replace("\n", "")
                print('Saving "_light" property...')
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
            elif "\"mingpulevel\"" in line:
                print('Skipping "mingpulevel" property...')
            elif "\"mincpulevel\"" in line:
                print('Skipping "mincpulevel" property...')
            elif "\"maxgpulevel\"" in line:
                print('Skipping "maxgpulevel" property...')
            elif "\"maxcpulevel\"" in line:
                print('Skipping "maxcpulevel" property...')
            elif "\"disableX360\"" in line:
                print('Skipping "disableX360" property...')
            elif "\"fademaxdist\"" in line:
                convFile.write(line)
                newLine = line.replace("fademaxdist", "original_fademaxdist")
                print('Saving "fademaxdist" property...')
                convFile.write(newLine)
            elif "\"fademindist\"" in line:
                convFile.write(line)
                newLine = line.replace("fademindist", "original_fademindist")
                print('Saving "fademindist" property...')
                convFile.write(newLine)
            elif "\"solid\"" in line:
                convFile.write(line)
                newLine = line.replace("solid", "original_solid")
                print('Saving "solid" property...')
                convFile.write(newLine)
            elif "\"prop_loot_crate\"" in line:
                newLine = line.replace("prop_loot_crate", "item_item_crate")
                print('prop_loot_crate -> item_item_crate')
                convFile.write(newLine)
            elif "\"prop_metal_crate\"" in line:
                newLine = line.replace("prop_metal_crate", "item_item_crate")
                print('prop_metal_crate -> item_item_crate')
                convFile.write(newLine)
            elif "\"prop_money_crate\"" in line:
                newLine = line.replace("prop_money_crate", "item_item_crate")
                print('prop_money_crate -> item_item_crate')
                convFile.write(newLine)
            elif "\"prop_paradrop_crate\"" in line:
                newLine = line.replace("prop_paradrop_crate", "item_item_crate")
                print('prop_paradrop_crate -> item_item_crate')
                convFile.write(newLine)
            elif "\"point_dz_weaponspawn\"" in line:
                newLine = line.replace("point_dz_weaponspawn", "item_item_crate")
                print('point_dz_weaponspawn -> item_item_crate')
                convFile.write(newLine)
            elif "\"point_dz_itemspawn\"" in line:
                newLine = line.replace("point_dz_itemspawn", "item_item_crate")
                print('point_dz_itemspawn -> item_item_crate')
                convFile.write(newLine)
            elif "\"weapon_healthshot\"" in line:
                newLine = line.replace("weapon_healthshot", "item_healthvial")
                print('weapon_healthshot -> item_healthvial')
                convFile.write(newLine)
            elif "\"dronegun\"" in line:
                newLine = line.replace("dronegun", "npc_turret_floor")
                print('dronegun -> npc_turret_floor')
                convFile.write(newLine)
            elif "\"point_dz_dronegun\"" in line:
                newLine = line.replace("dronegun", "npc_turret_floor")
                print('point_dz_dronegun -> npc_turret_floor')
                convFile.write(newLine)
            else:
                convFile.write(line)
