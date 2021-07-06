# cmd command: python vmf_convert.py "C:\path\to\vmf\file.vmf"

import re, sys, os

global classnameVar, saveLines, savingProces, deletingProces, ObseleteEntities, saveSolidLines, savingSolidProces

def LogPrint(inputString, print_bool = True):
    logFile.write(inputString + '\n')
    if print_bool == True:
        print(inputString)

INPUT_FILE_EXT = '.vmf'
# this leads to the root of the game folder, i.e. dota 2 beta/content/dota_addons/, make sure to remember the final slash!!
PATH_TO_GAME_CONTENT_ROOT = ""
PATH_TO_CONTENT_ROOT = ""
    
print('--------------------------------------------------------------------------------------------------------')
print('Source 2 .vmf Prepper! EXPERIMENTAL!! By "caseytube" and "The [G]amerX" via Github')
print('Converts .vmf files to be ready for Source 2 by fixing materials and entities')
print('--------------------------------------------------------------------------------------------------------')
#############################################################
someInput = input("Would you like to convert/delete 'weapon_*' entities?\n - 1: convert weapons entities\n - 2: delete weapons entities\n - 3: make them prop_physics with the appropriate model \n (1/2/3):").lower()
if someInput in "1":
    convert_weapons = 1
elif someInput in "2":
    convert_weapons = 2
elif someInput in "3":
    convert_weapons = 3
else:
    print("Please respond with '1', '2' or '3'. Quitting process!")
    quit()
#############################################################
someInput = input("Would you like to delete Player Clip brushes? (y/n):").lower()
if someInput in "yes":
    deletePlayerClips = 1
elif someInput in "no":
    deletePlayerClips = 0
else:
    print("Please respond with 'yes' or 'no'. Quitting process!")
    quit()
#############################################################
someInput = input("Would you like to delete Clip brushes? (y/n):").lower()
if someInput in "yes":
    deleteClips = 1
elif someInput in "no":
    deleteClips = 0
else:
    print("Please respond with 'yes' or 'no'. Quitting process!")
    quit()
#############################################################

filename = sys.argv[1]
convertedFilename = filename.replace('.vmf', '') + 'Converted.vmf'
LogFilename = filename.replace('.vmf', '') + '_log.txt'
logFile = open(LogFilename, 'w')
if not os.path.exists(filename):
    print("input file doesn't exist")
    quit()

LogPrint('Importing ' + os.path.basename(filename))
deletingProces = 0
savingProces = 0
savingSolidProces = 0
classnameVar = ""
saveLines = ""
saveSolidLines = ""
ObseleteEntities = [
    "\"func_areaportal\"", 
    "\"func_areaportalwindow\"", 
    "\"postprocess_controller\"", 
    "\"env_detail_controller\"", 
    "\"shadow_control\"", 
    "\"func_fish_pool\"", 
    "\"fish\"", 
    "\"pet_entity\"", 
    "\"chicken\"", 
    "\"func_no_defuse\"",
    "\"env_tonemap_controller_ghost\"", 
    "\"env_tonemap_controller_infected\"", 
    "\"prop_mapplaced_long_use_entity\"", 
    "\"item_dogtags\"", 
    "\"item_heavyassaultsuit\"",
    "\"item_cutters\"",
    "\"item_defuser\"",
    "\"prop_weapon_upgrade_tablet_droneintel\"",
    "\"prop_weapon_upgrade_tablet_highres\"",
    "\"prop_weapon_upgrade_tablet_zoneintel\"",
    "\"hostage\"",
    "\"hostage_entity\"",
    "\"info_hostage_spawn\"",
    "\"hostage_carriable_prop\"",
    "\"info_hostage_rescue_zone_hint\"",
    "\"inferno\"",
    "\"weapon_gascan\"",
    "\"weapon_zone_repulsor\"",
    "\"ability_selfdestruct\"",
    "\"ent_snowball_pile\"",
    "\"item_assaultsuit\"",
    "\"item_cash\"",
    "\"item_coop_coin\"",
	"\"trigger_survival_playarea\"",
	"\"info_gascanister_launchpoint\"",
	"\"info_map_parameters\"",
	"\"water_lod_control\"",
	"\"logic_eventlistener\"",
	"\"game_survival_logic\"",
	"\"info_map_region\"",
	"\"func_tablet_blocker\"",
	"\"func_survival_c4_target\"",
	"\"prop_counter\"",
	"\"func_bomb_target\"",
	"\"func_hostage_rescue\"",
	"\"func_clip_vphysics\"",
    "_projectile\""
]
if convert_weapons == 2:
    ObseleteEntities.append("\"weapon_")
with open(convertedFilename, 'w') as convFile:
    with open(filename, 'r') as vmfFile:
        for line in vmfFile.readlines():
            splitLine = line.replace('"', '').replace("'", "").split()
            last = len(splitLine) - 1
			#############################################################
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
                ForDelete = 0
                for ObseleteEntity in ObseleteEntities:
                    if ObseleteEntity in line:
                        ForDelete = 1
                        break
                if ForDelete == 1:
                    LogPrint(' --> Deleting ' + str(classnameVar) + ' entity.')
                    deletingProces = 1
                    savingProces = 0
                    saveLines = ""
                    continue
                else:
                    LogPrint(' --> Checking ' + str(classnameVar) + ' entity.')
                    convFile.write(saveLines)
                    deletingProces = 0
                    savingProces = 0
                    saveLines = ""
            if 1 == deletingProces:
                if "}" == line:
                    deletingProces = 0
                continue
            #############################################################
            if 1 == savingSolidProces:
                if "\"material\"" in line:
                    if "\"TOOLS/TOOLSDRONECLIP\"" in line:
                        saveSolidLines = saveSolidLines + line
                        continue
                    elif 1 == deletePlayerClips and "\"TOOLS/TOOLSPLAYERCLIP\"" in line:
                        saveSolidLines = saveSolidLines + line
                        continue
                    elif 1 == deleteClips and "\"TOOLS/TOOLSCLIP\"" in line:
                        saveSolidLines = saveSolidLines + line
                        continue
                    else:
                        convFile.write(saveSolidLines)
                        savingSolidProces = 0
                        saveSolidLines = ""
                elif "	}\n" == line:
                    LogPrint(' -> Deleting Clip brush.')
                    savingSolidProces = 0
                    saveSolidLines = ""
                    continue
                else:
                    saveSolidLines = saveSolidLines + line
                    continue
            if "worldspawn" in classnameVar:
                if "	solid\n" == line:
                    savingSolidProces = 1
                    saveSolidLines = line
                    continue
            #############################################################
            if "\"uaxis\"" in line:
                oldVar = splitLine[last]
                newVar = float(oldVar) * 32
                LogPrint('uaxis: ' + str(oldVar) + ' -> ' + str(newVar), False)
                newLine = line.replace(str(oldVar), str(newVar))
                convFile.write(newLine)
            elif "\"vaxis\"" in line:
                oldVar = splitLine[last]
                newVar = float(oldVar) * 32
                LogPrint('vaxis: ' + str(oldVar) + ' -> ' + str(newVar), False)
                newLine = line.replace(str(oldVar), str(newVar))
                convFile.write(newLine)
            elif "\"uniformscale\"" in line:
                oldVar = splitLine[last]
                newLine = line.replace("uniformscale", "scales")
                newLine = newLine.replace(str(oldVar), str(oldVar) + " " + str(oldVar) + " " + str(oldVar))
                convFile.write(newLine)
            elif "\"fog_volume\"" in line:
                newLine = line.replace("fog_volume", "env_volumetric_fog_volume")
                LogPrint('fog_volume -> env_volumetric_fog_volume')
                convFile.write(newLine)
            elif "\"env_fog_controller\"" in line:
                newLine = line.replace("env_fog_controller", "env_volumetric_fog_controller")
                LogPrint('env_fog_controller -> env_volumetric_fog_controller')
                convFile.write(newLine)
            elif "\"fogend\"" in line:
                newLine = line.replace("fogend", "FadeInEnd")
                LogPrint('Fixing "fogend" property...')
                convFile.write(newLine)
            elif "\"fogstart\"" in line:
                newLine = line.replace("fogstart", "FadeInStart")
                LogPrint('Fixing "fogstart" property...')
                convFile.write(newLine)
            elif "\"fogmaxdensity\"" in line:
                newLine = line.replace("fogmaxdensity", "FogStrength")
                LogPrint('Fixing "fogmaxdensity" property...')
                convFile.write(newLine)
            elif "\"fogenable\"" in line:
                oldVar = splitLine[last]
                newVar = int(oldVar) ^ 1
                newLine = line.replace("fogenable", "StartDisabled")
                LogPrint('Fixing "fogenable" property...')
                newLine = newLine.replace(str(oldVar), str(newVar))
                convFile.write(newLine)
            elif "\"foglerptime\"" in line:
                newLine = line.replace("foglerptime", "FadeSpeed")
                LogPrint('Fixing "foglerptime" property...')
                convFile.write(newLine)
            elif "\"env_sun\"" in line:
                newLine = line.replace("env_sun", "env_sky")
                LogPrint('env_sun -> env_sky')
                convFile.write(newLine)
            elif "\"info_player_terrorist\"" in line:
                newLine = line.replace("info_player_terrorist", "info_player_start")
                LogPrint('info_player_terrorist -> info_player_start')
                convFile.write(newLine)
            elif "\"info_player_counterterrorist\"" in line:
                newLine = line.replace("info_player_counterterrorist", "info_player_start")
                LogPrint('info_player_counterterrorist -> info_player_start')
                convFile.write(newLine)
            elif "\"info_player_teamspawn\"" in line:
                newLine = line.replace("info_player_teamspawn", "info_player_start")
                LogPrint('info_player_teamspawn -> info_player_start')
                convFile.write(newLine)
            elif "\"info_player_deathmatch\"" in line:
                newLine = line.replace("info_player_deathmatch", "info_player_start")
                LogPrint('info_player_deathmatch -> info_player_start')
                convFile.write(newLine)
            elif "\"game_player_equip\"" in line:
                newLine = line.replace("game_player_equip", "info_hlvr_equip_player")
                LogPrint('game_player_equip -> info_hlvr_equip_player')
                convFile.write(newLine)
            elif "\"info_teleport_destination\"" in line:
                newLine = line.replace("info_teleport_destination", "point_teleport")
                LogPrint('info_teleport_destination -> point_teleport')
                convFile.write(newLine)
            elif "\"_inner_cone\"" in line:
                convFile.write(line)
                newLine = line.replace("_inner_cone", "original_innerconeangle")
                LogPrint('Saving "_inner_cone" property...')
                convFile.write(newLine)
            elif "\"_cone\"" in line:
                convFile.write(line)
                newLine = line.replace("_cone", "original_outerconeangle")
                LogPrint('Saving "_cone" property...')
                convFile.write(newLine)
            elif "\"_linear_attn\"" in line:
                convFile.write(line)
                newLine = line.replace("_linear_attn", "original_attenuation1")
                LogPrint('Saving "_linear_attn" property...')
                convFile.write(newLine)
            elif "\"_quadratic_attn\"" in line:
                convFile.write(line)
                newLine = line.replace("_quadratic_attn", "original_attenuation2")
                LogPrint('Saving "_quadratic_attn" property...')
                convFile.write(newLine)
            elif "\"_lightHDR\"" in line:
                LogPrint('Skipping "_lightHDR" property...')
            elif "\"_lightscaleHDR\"" in line:
                LogPrint('Skipping "_lightscaleHDR" property...')
            elif "\"_light\"" in line:
                convFile.write(line)
                oldVar = line.replace('"', '').replace("'", "").replace("_light", "").replace("	 ", "").replace("\n", "")
                LogPrint('Saving "_light" property...')
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
                    LogPrint('Fixing "spawnflags" property for ' + classnameVar + ' entity...')
                    newLine = newLine.replace(str(oldVar), str(newVar))
                    convFile.write(newLine)
                elif "env_tonemap_controller" in classnameVar:
                    newLine = line.replace("spawnflags", "master")
                    LogPrint('Fixing "spawnflags" property for ' + classnameVar + ' entity...')
                    convFile.write(newLine)
                elif "env_fog_controller" in classnameVar:
                    newLine = line.replace("spawnflags", "IsMaster")
                    LogPrint('Fixing "spawnflags" property for ' + classnameVar + ' entity...')
                    convFile.write(newLine)
            elif "\"mingpulevel\"" in line:
                if "prop_static" in classnameVar:
                    LogPrint('Skipping "mingpulevel" property for ' + classnameVar + ' entity...')
            elif "\"mincpulevel\"" in line:
                if "prop_static" in classnameVar:
                    LogPrint('Skipping "mincpulevel" property for ' + classnameVar + ' entity...')
            elif "\"maxgpulevel\"" in line:
                if "prop_static" in classnameVar:
                    LogPrint('Skipping "maxgpulevel" property for ' + classnameVar + ' entity...')
            elif "\"maxcpulevel\"" in line:
                if "prop_static" in classnameVar:
                    LogPrint('Skipping "maxcpulevel" property for ' + classnameVar + ' entity...')
            elif "\"disableX360\"" in line:
                if "prop_static" in classnameVar:
                    LogPrint('Skipping "disableX360" property for ' + classnameVar + ' entity...')
            elif "\"is_security_door\"" in line:
                if "dz_door" in classnameVar:
                    LogPrint('Skipping "is_security_door" property for ' + classnameVar + ' entity...')
            elif "\"fademaxdist\"" in line:
                convFile.write(line)
                newLine = line.replace("fademaxdist", "original_fademaxdist")
                LogPrint('Saving "fademaxdist" property...')
                convFile.write(newLine)
            elif "\"fademindist\"" in line:
                convFile.write(line)
                newLine = line.replace("fademindist", "original_fademindist")
                LogPrint('Saving "fademindist" property...')
                convFile.write(newLine)
            elif "\"solid\"" in line:
                convFile.write(line)
                newLine = line.replace("solid", "original_solid")
                LogPrint('Saving "solid" property...')
                convFile.write(newLine)
            elif "\"prop_loot_crate\"" in line:
                newLine = line.replace("prop_loot_crate", "item_item_crate")
                LogPrint('prop_loot_crate -> item_item_crate')
                convFile.write(newLine)
            elif "\"prop_metal_crate\"" in line:
                newLine = line.replace("prop_metal_crate", "item_item_crate")
                LogPrint('prop_metal_crate -> item_item_crate')
                convFile.write(newLine)
            elif "\"prop_money_crate\"" in line:
                newLine = line.replace("prop_money_crate", "item_item_crate")
                LogPrint('prop_money_crate -> item_item_crate')
                convFile.write(newLine)
            elif "\"prop_paradrop_crate\"" in line:
                newLine = line.replace("prop_paradrop_crate", "item_item_crate")
                LogPrint('prop_paradrop_crate -> item_item_crate')
                convFile.write(newLine)
            elif "\"point_dz_weaponspawn\"" in line:
                newLine = line.replace("point_dz_weaponspawn", "item_item_crate")
                LogPrint('point_dz_weaponspawn -> item_item_crate')
                convFile.write(newLine)
            elif "\"point_dz_itemspawn\"" in line:
                newLine = line.replace("point_dz_itemspawn", "item_item_crate")
                LogPrint('point_dz_itemspawn -> item_item_crate')
                convFile.write(newLine)
			# start weapon_* entities...
            elif "\"weapon_deagle\"" in line or "\"weapon_usp" in line or "\"weapon_p250\"" in line or "\"weapon_fiveseven\"" in line or "\"weapon_hpk" in line or "\"weapon_glock" in line:
                oldVar = splitLine[last]
                newLine = line.replace(oldVar, "weapon_pistol")
                LogPrint(str(oldVar) + ' -> weapon_pistol')
                convFile.write(newLine)
            elif "\"weapon_nova\"" in line or "\"weapon_xm1014\"" in line or "\"weapon_autoshotgun\"" in line or "\"weapon_mag7\"" in line or "\"weapon_sawedoff\"" in line or "\"weapon_m13\"" in line:
                oldVar = splitLine[last]
                newLine = line.replace(oldVar, "weapon_shotgun")
                LogPrint(str(oldVar) + ' -> weapon_shotgun')
                convFile.write(newLine)
            elif "\"weapon_breachcharge\"" in line:
                newLine = line.replace("weapon_breachcharge", "item_hlvr_weapon_tripmine")
                LogPrint('weapon_breachcharge -> item_hlvr_weapon_tripmine')
                convFile.write(newLine)
            elif "\"weapon_ak47\"" in line or "\"weapon_m4a1" in line or "\"weapon_galil" in line or "\"weapon_famas" in line or "\"weapon_aug" in line:
                oldVar = splitLine[last]
                newLine = line.replace(oldVar, "weapon_ar2")
                LogPrint(str(oldVar) + ' -> weapon_ar2')
                convFile.write(newLine)
            elif "\"weapon_knife" in line or "\"weapon_bayonet" in line or "\"weapon_hammer\"" in line or "\"weapon_axe\"" in line or "\"weapon_spanner\"" in line or "\"weapon_melee\"" in line:
                oldVar = splitLine[last]
                newLine = line.replace(oldVar, "weapon_crowbar")
                LogPrint(str(oldVar) + ' -> weapon_crowbar')
                convFile.write(newLine)
            elif "\"weapon_hegrenade\"" in line:
                newLine = line.replace("weapon_hegrenade", "weapon_frag")
                LogPrint('weapon_hegrenade -> weapon_frag')
                convFile.write(newLine)
            elif "\"weapon_revolver\"" in line:
                newLine = line.replace("weapon_revolver", "weapon_357")
                LogPrint('weapon_revolver -> weapon_357')
                convFile.write(newLine)
            elif "\"weapon_healthshot\"" in line:
                newLine = line.replace("weapon_healthshot", "item_healthvial")
                LogPrint('weapon_healthshot -> item_healthvial')
                convFile.write(newLine)
			# end weapon_* entities.
            elif "\"dronegun\"" in line:
                newLine = line.replace("dronegun", "npc_turret_floor")
                LogPrint('dronegun -> npc_turret_floor')
                convFile.write(newLine)
            elif "\"point_dz_dronegun\"" in line:
                newLine = line.replace("point_dz_dronegun", "npc_turret_floor")
                LogPrint('point_dz_dronegun -> npc_turret_floor')
                convFile.write(newLine)
            elif "\"func_conveyor\"" in line:
                newLine = line.replace("func_conveyor", "func_brush")
                LogPrint('func_conveyor -> func_brush')
                convFile.write(newLine)
            elif "\"func_detail_blocker\"" in line:
                newLine = line.replace("func_detail_blocker", "func_brush")
                LogPrint('func_detail_blocker -> func_brush')
                convFile.write(newLine)
            elif "\"func_occluder\"" in line:
                newLine = line.replace("func_occluder", "func_brush")
                LogPrint('func_occluder -> func_brush')
                convFile.write(newLine)
            elif "\"func_illusionary\"" in line:
                newLine = line.replace("func_illusionary", "func_brush")
                LogPrint('func_illusionary -> func_brush')
                convFile.write(newLine)
                newLine = line.replace("classname", "solid")
                newLine = newLine.replace("func_illusionary", "0")
                convFile.write(newLine)
            elif "\"func_ladderendpoint\"" in line:
                newLine = line.replace("func_ladderendpoint", "func_useableladder")
                LogPrint('func_ladderendpoint -> func_useableladder')
                convFile.write(newLine)
            elif "\"startsound\"" in line:
                if "func_movelinear" in classnameVar:
                    newLine = line.replace("startsound", "StartSound")
                    LogPrint('Fixing "startsound" property for ' + classnameVar + ' entity...')
                    convFile.write(newLine)
            elif "\"stopsound\"" in line:
                if "func_movelinear" in classnameVar:
                    newLine = line.replace("stopsound", "StopSound")
                    LogPrint('Fixing "stopsound" property for ' + classnameVar + ' entity...')
                    convFile.write(newLine)
            elif "\"teamToBlock\"" in line or "\"affectsFlow\"" in line:
                if "func_nav_blocker" in classnameVar:
                    LogPrint('Skipping properties for "func_nav_blocker" entity...')
            elif "\"prop_exploding_barrel\"" in line:
                newLine = line.replace("prop_exploding_barrel", "prop_physics")
                LogPrint('prop_exploding_barrel -> prop_physics')
                convFile.write(newLine)
                newLine = line.replace("classname", "model")
                newLine = newLine.replace("prop_exploding_barrel", "models/props/coop_cementplant/exloding_barrel/exploding_barrel.vmdl")
                convFile.write(newLine)
            elif "\"dz_door\"" in line:
                newLine = line.replace("dz_door", "prop_door_rotating")
                LogPrint('dz_door -> prop_door_rotating')
                convFile.write(newLine)
            else:
                convFile.write(line)
