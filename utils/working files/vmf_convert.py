# cmd command: python vmf_convert.py "C:\path\to\vmf\file.vmf"

import re, sys, os

def parseLine(inputString):
    inputString = inputString.lower().replace('"', '').replace("'", "").replace("\n", "").replace("\t", "").replace("{", "").replace("}", "").replace(" ", "")
    return inputString


INPUT_FILE_EXT = '.vmf'
# this leads to the root of the game folder, i.e. dota 2 beta/content/dota_addons/, make sure to remember the final slash!!
PATH_TO_GAME_CONTENT_ROOT = ""
PATH_TO_CONTENT_ROOT = ""
    
print('--------------------------------------------------------------------------------------------------------')
print('Source 2 .vmf Prepper! EXPERIMENTAL!! By "caseytube" and "The [G]amerX" via Github')
print('Converts .vmf files to be ready for Source 2 by fixing materials and entities')
print('--------------------------------------------------------------------------------------------------------')

someInput = input("Would you like to convert/delete 'weapon_*' entities?\n - Yes: convert weapons entities\n - No: delete weapons entities\n (y/n):").lower()
if someInput in "yes":
    convert_weapons = True
elif someInput in "no":
    convert_weapons = False
elif someInput == "": # debug: casey's favorite default value
    convert_weapons = True
else:
    print("Please respond with 'yes' or 'no.' Quitting process!")
    quit()


filename = sys.argv[1]
convertedFilename = filename.replace('.vmf', '') + 'Converted.vmf'
if not os.path.exists(filename):
    print("input file doesn't exist")
    quit()

print('Importing', os.path.basename(filename))
global classnameVar, saveLines, savingProces, deletingProces, ObseleteEntities
deletingProces = 0
savingProces = 0
classnameVar = ""
saveLines = ""
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
    "\"inferno\"",
    "\"weapon_gascan\"",
    "\"weapon_zone_repulsor\"",
    "\"ability_selfdestruct\"",
    "\"ent_snowball_pile\"",
    "\"item_assaultsuit\"",
    "\"item_cash\"",
    "\"item_coop_coin\"",
    "_projectile\""
]
if convert_weapons == False:
    ObseleteEntities.append("\"weapon_")
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
                ForDelete = 0
                for ObseleteEntity in ObseleteEntities:
                    if ObseleteEntity in line:
                        ForDelete = 1
                        break
                if ForDelete == 1:
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
                elif "env_tonemap_controller" in classnameVar:
                    newLine = line.replace("spawnflags", "master")
                    print('Fixing "spawnflags" property for ' + classnameVar + ' entity...')
                    convFile.write(newLine)
                elif "env_fog_controller" in classnameVar:
                    newLine = line.replace("spawnflags", "IsMaster")
                    print('Fixing "spawnflags" property for ' + classnameVar + ' entity...')
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
			# start weapon_* entities...
            elif "\"weapon_deagle\"" in line or "\"weapon_usp" in line or "\"weapon_p250\"" in line or "\"weapon_fiveseven\"" in line or "\"weapon_hpk" in line or "\"weapon_glock" in line:
                oldVar = splitLine[last]
                newLine = line.replace(oldVar, "weapon_pistol")
                print(str(oldVar) + ' -> weapon_pistol')
                convFile.write(newLine)
            elif "\"weapon_nova\"" in line or "\"weapon_xm1014\"" in line or "\"weapon_autoshotgun\"" in line or "\"weapon_mag7\"" in line or "\"weapon_sawedoff\"" in line or "\"weapon_m13\"" in line:
                oldVar = splitLine[last]
                newLine = line.replace(oldVar, "weapon_shotgun")
                print(str(oldVar) + ' -> weapon_shotgun')
                convFile.write(newLine)
            elif "\"weapon_breachcharge\"" in line:
                newLine = line.replace("weapon_breachcharge", "item_hlvr_weapon_tripmine")
                print('weapon_breachcharge -> item_hlvr_weapon_tripmine')
                convFile.write(newLine)
            elif "\"weapon_ak47\"" in line or "\"weapon_m4a1" in line or "\"weapon_galil" in line or "\"weapon_famas" in line or "\"weapon_aug" in line:
                oldVar = splitLine[last]
                newLine = line.replace(oldVar, "weapon_ar2")
                print(str(oldVar) + ' -> weapon_ar2')
                convFile.write(newLine)
            elif "\"weapon_knife" in line or "\"weapon_bayonet" in line or "\"weapon_hammer\"" in line or "\"weapon_axe\"" in line or "\"weapon_spanner\"" in line or "\"weapon_melee\"" in line:
                oldVar = splitLine[last]
                newLine = line.replace(oldVar, "weapon_crowbar")
                print(str(oldVar) + ' -> weapon_crowbar')
                convFile.write(newLine)
            elif "\"weapon_hegrenade\"" in line:
                newLine = line.replace("weapon_hegrenade", "weapon_frag")
                print('weapon_hegrenade -> weapon_frag')
                convFile.write(newLine)
            elif "\"weapon_revolver\"" in line:
                newLine = line.replace("weapon_revolver", "weapon_357")
                print('weapon_revolver -> weapon_357')
                convFile.write(newLine)
            elif "\"weapon_healthshot\"" in line:
                newLine = line.replace("weapon_healthshot", "item_healthvial")
                print('weapon_healthshot -> item_healthvial')
                convFile.write(newLine)
			# end weapon_* entities.
            elif "\"dronegun\"" in line:
                newLine = line.replace("dronegun", "npc_turret_floor")
                print('dronegun -> npc_turret_floor')
                convFile.write(newLine)
            elif "\"point_dz_dronegun\"" in line:
                newLine = line.replace("point_dz_dronegun", "npc_turret_floor")
                print('point_dz_dronegun -> npc_turret_floor')
                convFile.write(newLine)
            elif "\"func_conveyor\"" in line:
                newLine = line.replace("func_conveyor", "func_brush")
                print('func_conveyor -> func_brush')
                convFile.write(newLine)
            elif "\"func_detail_blocker\"" in line:
                newLine = line.replace("func_detail_blocker", "func_brush")
                print('func_detail_blocker -> func_brush')
                convFile.write(newLine)
            elif "\"func_illusionary\"" in line:
                newLine = line.replace("func_illusionary", "func_brush")
                print('func_illusionary -> func_brush')
                convFile.write(newLine)
                newLine = line.replace("classname", "solid")
                newLine = newLine.replace("func_illusionary", "0")
                convFile.write(newLine)
            elif "\"func_ladderendpoint\"" in line:
                newLine = line.replace("func_ladderendpoint", "func_useableladder")
                print('func_ladderendpoint -> func_useableladder')
                convFile.write(newLine)
            elif "\"startsound\"" in line:
                if "func_movelinear" in classnameVar:
                    newLine = line.replace("startsound", "StartSound")
                    print('Fixing "startsound" property for ' + classnameVar + ' entity...')
                    convFile.write(newLine)
            elif "\"stopsound\"" in line:
                if "func_movelinear" in classnameVar:
                    newLine = line.replace("stopsound", "StopSound")
                    print('Fixing "stopsound" property for ' + classnameVar + ' entity...')
                    convFile.write(newLine)
            elif "\"teamToBlock\"" in line or "\"affectsFlow\"" in line:
                if "func_nav_blocker" in classnameVar:
                    print('Skipping properties for "func_nav_blocker" entity...')
            else:
                convFile.write(line)
