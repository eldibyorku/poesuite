import pyautogui
import pyperclip 
from pynput.keyboard import Key, Controller
keyboard = Controller()
import time
import FocusWindow as FocusWindow

CURRENCY_TAB = (767, 109)
CHAOS = (551, 267)
MAP_TAB = (296, 112)
T17 = (458, 244)
SANCTUARY = (328, 323)
ABOM = (110, 322)
MAPS_TL = (43, 459)
MAPS_BR = (619, 748)
MAP_W = (MAPS_BR[0] - MAPS_TL[0]) /  12

def roll():
    lines = read_map().split("\n")
    if lines[0] == '':
        exit()
        # return True
   
    scarabs = 0

    
    currency = 0
    total = 0
    quant = 0
    pack_size = 0
    life = 0

    for line in lines:
        if "Item Quantity:" in line:
             quant = int(line.split("+")[1].split("%")[0])
        if "Pack Size:" in line:
             pack_size = int(line.split("+")[1].split("%")[0])
        if "More Scarabs:" in line:
            # Extracting the number and removing the percentage sign
            scarabs = int(line.split("+")[1].split("%")[0])
        if "More Currency:" in line:
            # Extracting the number and removing the percentage sign
            currency = int(line.split("+")[1].split("%")[0])
        if "Monster Life" in line:
             life = int(line.split("%")[0])

    contains_keywords = any("Barrels" in line or "Modifiers" in line for line in lines)
    
    bad_mods = ["Auras", "Monster Life", "Union", "for 4 out of", "of Maximum Life as Extra M", "Marked for Death", "from Critical Strikes"]
    bad_mods_count = sum(1 for keyword in bad_mods if any(keyword in line for line in lines))
    bad_combos = bad_mods_count >=2
    no_go = any("% reduced Action Speed for" in line or "Monsters take 100% reduced Extra Damage from Critical Strikes" in line for line in lines )
    total = scarabs + currency

    if scarabs >= 200:
         return True
    
    if not no_go and not bad_combos:
        if scarabs + quant >= 300:
                print( "Map meets the requirement with 175%+ More Scarabs.")
                return True
        if currency + quant + scarabs >= 450:
                print( "Map meets the requirement with 240%+ More Currency.")
                return True

        if contains_keywords:
            if scarabs >= 100 or (total >= 250 and scarabs > 0):
                print("Map meets the requirement with either 100%+ More Scarabs or a total of 200+ with Currency.")
                return True
            else:
                return False
        else:
             return False
    else:
        print("ese")
        print(no_go, bad_combos)
        return False
    
def grab_c():
    pyautogui.moveTo(CURRENCY_TAB[0], CURRENCY_TAB[1], 0.2)
    pyautogui.click()
    time.sleep(0.1)
    pyautogui.moveTo(CHAOS[0], CHAOS[1], 0.1)
    pyautogui.rightClick()
    time.sleep(0.1)
    
def open_maps():
    pyautogui.moveTo(MAP_TAB[0], MAP_TAB[1], 0.2)
    pyautogui.click()
    pyautogui.moveTo(T17[0], T17[1], 0.2)
    pyautogui.click()
    pyautogui.moveTo(ABOM[0], ABOM[1], 0.2)
    pyautogui.click()
    time.sleep(0.1)

def read_map():
    pyperclip.copy('')
    keyboard.press(Key.ctrl)
    keyboard.press('c')
    time.sleep(0.1)
    keyboard.release('c')
    keyboard.release(Key.ctrl)
    item_text = pyperclip.paste()
    return item_text

def main():
    FocusWindow.focus_window("Path of Exile")
    time.sleep(1)
    pyautogui.PAUSE = 0.05
    grab_c()
    keyboard.press(Key.shift)
    open_maps()
    pyautogui.moveTo(MAPS_TL[0] + 20 + 0 * MAP_W, MAPS_TL[1] + 20 + 0 * MAP_W, 0.1)
    # item = read_map()
    # print(roll())
    for col in range(12):
         for row in range(6):
              pyautogui.moveTo(MAPS_TL[0] + 20 + col * MAP_W, MAPS_TL[1] + 20 + row * MAP_W, 0.2)
              hit = roll()
              while not hit:
                   pyautogui.click()
                   time.sleep(0.2)
                   hit = roll()
    keyboard.release(Key.shift)

main()
    
# Example map description
map_description = """
Item Class: Maps
Rarity: Rare
Unstable Abyss
Sanctuary Map
--------
Map Tier: 17
Item Quantity: +156% (augmented)
Item Rarity: +176% (augmented)
Monster Pack Size: +36% (augmented)
More Scarabs: +50% (augmented)
More Currency: +179% (augmented)
Quality: +20% (augmented)
--------
Item Level: 84
--------
Monster Level: 84
--------
45% increased number of Rare Monsters
Monsters take 100% reduced Extra Damage from Critical Strikes
Debuffs on Monsters expire 100% faster
All Monster Damage from Hits always Ignites
Monsters gain 180% of their Physical Damage as Extra Damage of a random Element
Players have 50% less Defences
Rare Monsters each have 2 additional Modifiers
--------
Travel to this Map by using it in a personal Map Device. Maps can only be used once.
--------
Modifiable only with Chaos Orbs
"""

# # Call the function with the map description
# result = roll(map_description)
# print(result)

