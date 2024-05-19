import pyautogui
import pyperclip
import time
from pynput.keyboard import Key, Controller
import FocusWindow

keyboard = Controller()

# Constants
CURRENCY_TAB = (767, 109)
JEWEL_TYPES = ['Crimson Jewel', 'Cobalt Jewel', 'Viridian Jewel']
AUG_LOCATION = (227, 328)
ALT_LOCATION = (108, 267)
JEWEL_LOCATION = (337, 456)
WIS_LOCATION = (110, 205)
SCOUR_LOCATION = (430, 508)
TRANS_LOCATION = (55, 271)
DUMP_LOCATION = (763, 206)
DUMP_TL = (17, 127)
DUMP_BR = (647, 760)
DUMP_W = (DUMP_BR[0] - DUMP_TL[0]) / 24
STORE_LOCATION = (770, 348)
JEWEL_IN_INV = (1293, 613)
INV_TL = (1273, 588)
INV_BR = (1904, 848)
INV_W = (INV_BR[0] - INV_TL[0]) / 24

MOD_POOLS = {
    "life": ["Vivid", "Strength", "Spirit", "Infusion", "Potency", "Demolishing", "Elements", "Unmaking", "Atrophy", "Zealousness", "Exsanguinating", "Venom", "Combusting"],
    "1_hander": ["Harmonic", "Piercing", "Puncturing", "Strength", "Spirit", "Potency", "Demolishing", "Elements"],
    "2_hander": ["Beating", "Cleaving", "Fencing", "Blunt", "Rupturing", "Berserking", "Potency", "Demolishing", "Elements"],
    "bows": ["Volleying", "Dexterity", "Infusion", "Potency", "Demolishing", "Elements", "Unmaking"],
    "armour": ["Armoured", "Strength", "Spirit", "Infusion", "Potency", "Demolishing", "Elements"],
    "mana": ["Enlightened", "Intelligence", "Spirit", "Potency", "Elements", "Unmaking", "Zealousness"],
    "es": ["Shimmering", "Intelligence", "Spirit", "Potency", "Elements", "Unmaking", "Gelidity", "Exsanguinating"],
    "multi": ["Piercing", "Rupturing", "Puncturing", "Infernal", "Arctic", "Surging", "Potency", "Demolishing", "Elements", "Unmaking"],
    "reserv": ["Cerebral", "Elements", "Unmaking"],
    "trap": ["Honed", "Unmaking", "Elements"]
}

DUMP_ARRAY = [(row, col) for row in range(24) for col in range(24)]

def read_name():
    """Reads and returns the name of the current item."""
    pyperclip.copy('')
    keyboard.press(Key.ctrl)
    keyboard.press('c') 
    time.sleep(0.1)  
    keyboard.release('c')
    keyboard.release(Key.ctrl)
    name = pyperclip.paste().strip().split('\n')[2]
    return name

def right_click_action(location):
    """Right-clicks at the specified location."""
    pyautogui.keyUp('shift')
    pyautogui.moveTo(location[0], location[1], 0.1)
    pyautogui.rightClick()

def wisdom():
    """Performs the wisdom action."""
    right_click_action(WIS_LOCATION)
    pyautogui.moveTo(JEWEL_LOCATION[0], JEWEL_LOCATION[1], 0.1)
    pyautogui.leftClick()

def scoure():
    """Performs the scour action."""
    right_click_action(SCOUR_LOCATION)
    pyautogui.moveTo(JEWEL_LOCATION[0], JEWEL_LOCATION[1], 0.1)
    pyautogui.leftClick()

def transmute():
    """Performs the transmute action."""
    right_click_action(TRANS_LOCATION)
    pyautogui.moveTo(JEWEL_LOCATION[0], JEWEL_LOCATION[1], 0.1)
    pyautogui.leftClick()

def aug():
    """Performs the augment action."""
    right_click_action(AUG_LOCATION)
    pyautogui.moveTo(JEWEL_LOCATION[0], JEWEL_LOCATION[1], 0.1)
    pyautogui.leftClick()

def alt():
    """Performs the alt action."""
    print("getting new alt")
    keyboard.release(Key.shift)
    pyautogui.moveTo(ALT_LOCATION[0], ALT_LOCATION[1], 0.1)
    keyboard.press(Key.shift)
    pyautogui.rightClick()
    pyautogui.moveTo(JEWEL_LOCATION[0], JEWEL_LOCATION[1], 0.1)
    pyautogui.leftClick()

def alt2():
    """Performs the alt2 action."""
    print("alt shift clicked")
    keyboard.press(Key.shift)
    time.sleep(0.1)
    pyautogui.leftClick()

def extract_jewel_name_components(name, jewel_types):
    """Extracts components from a jewel name."""
    parts = name.split()
    components = {
        'optional_meta_type': None,
        'prefix': None,
        'jewel_type': None,
        'suffix': None
    }

    if "of" in parts:
        of_index = parts.index("of")
        components['suffix'] = ' '.join(parts[of_index:])

    for jewel_type in jewel_types:
        if jewel_type in name:
            components['jewel_type'] = jewel_type
            break

    if components['jewel_type']:
        jewel_type_index = name.index(components['jewel_type'])
        before_jewel_type = name[:jewel_type_index].strip()
        before_parts = before_jewel_type.split()

        if len(before_parts) > 1:
            components['optional_meta_type'] = before_parts[0]
            components['prefix'] = ' '.join(before_parts[1:])
        elif len(before_parts) == 1:
            components['prefix'] = before_parts[0]

    return components

def check_prefix_suffix_in_desired_mods(name_components, mod_pools):
    """Checks if prefix or suffix matches the desired mods."""
    category_matches = {category: 0 for category in mod_pools}

    if name_components['prefix']:
        for category, mods in mod_pools.items():
            if any(mod in name_components['prefix'] for mod in mods):
                category_matches[category] += 1

    if name_components['suffix']:
        for category, mods in mod_pools.items():
            if any(mod in name_components['suffix'] for mod in mods):
                category_matches[category] += 1

    if any(matches == 2 for matches in category_matches.values()):
        return 2
    if any(matches == 1 for matches in category_matches.values()):
        return 1
    
    return 0

def craft():
    """Executes the crafting process."""
    alting = False
    alts = 0
    augs = 0
    while True:
        j_name = read_name()
        jewel = extract_jewel_name_components(j_name, JEWEL_TYPES)
        
        matches = check_prefix_suffix_in_desired_mods(jewel, MOD_POOLS)

        if matches == 2:
            time.sleep(0.1)
            keyboard.release(Key.shift)
            print(f"augs used: {augs}, alts used: {alts}")
            break
        elif matches == 1 and (not jewel['prefix'] or not jewel['suffix']):
            alting = False
            aug()
            augs += 1
        else:
            if alting:
                alt2()
                alts += 1
            else:
                alting = True
                alt()
                alts += 1

def read_item():
    """Reads and returns the item description."""
    pyperclip.copy('')
    keyboard.press(Key.ctrl)
    keyboard.press('c')
    time.sleep(0.1)
    keyboard.release(Key.ctrl)
    keyboard.release('c')
    item_text = pyperclip.paste()
    return item_text

def go_to_cell(cell):
    """Moves the cursor to the specified cell."""
    x = cell[0] * DUMP_W + DUMP_TL[0] + 20
    y = cell[1] * DUMP_W + DUMP_TL[1] + 20
    pyautogui.moveTo(x, y, 0.2)

def grab_jewel(cell, grabbing):
    """Attempts to grab a jewel from the specified cell."""
    if not grabbing:
        pyautogui.moveTo(DUMP_LOCATION[0], DUMP_LOCATION[1], 0.2)
        pyautogui.click()
    go_to_cell(cell)
    item_text = read_item()
    item_lines = item_text.split('\n')
    if any("Jewel" in line for line in item_lines) and all("Corrupted" not in line and "Unique" not in line and "Mirrored" not in line for line in item_lines):
        keyboard.press(Key.ctrl)
        time.sleep(0.1)
        pyautogui.click()
        keyboard.release(Key.ctrl)
        return True   
    return False

def setup_craft():
    """Sets up the crafting process."""
    pyautogui.moveTo(CURRENCY_TAB[0], CURRENCY_TAB[1], 0.1)
    pyautogui.click()
    pyautogui.moveTo(JEWEL_IN_INV[0], JEWEL_IN_INV[1], 0.1)
    keyboard.press(Key.ctrl)
    time.sleep(0.1)
    pyautogui.click()
    keyboard.release(Key.ctrl)
    wisdom()
    j_name = read_name()
    jewel = extract_jewel_name_components(j_name, JEWEL_TYPES)
    matches = check_prefix_suffix_in_desired_mods(jewel, MOD_POOLS)
    if matches < 1:
        scoure()
        transmute()

def store():
    """Stores the crafted jewel."""
    pyautogui.moveTo(STORE_LOCATION[0], STORE_LOCATION[1], 0.1)
    pyautogui.click()
    pyautogui.moveTo(JEWEL_IN_INV[0], JEWEL_IN_INV[1], 0.1)
    keyboard.press(Key.ctrl)
    time.sleep(0.1)
    pyautogui.click()
    keyboard.release(Key.ctrl)

def clear_jewel_location():
    pyautogui.moveTo(CURRENCY_TAB[0], CURRENCY_TAB[1], 0.1)
    pyautogui.click()
    pyautogui.moveTo(JEWEL_LOCATION[0], JEWEL_LOCATION[1], 0.1)
    keyboard.press(Key.ctrl)
    time.sleep(0.1)
    pyautogui.click()
    keyboard.release(Key.ctrl)
    store()

# Main execution
FocusWindow.focus_window('Path of Exile')
time.sleep(1)
clear_jewel_location()

grabbing = False

for cell in DUMP_ARRAY:
    got_jewel = grab_jewel(cell, grabbing)
    if got_jewel:
        grabbing = False
        setup_craft()
        pyautogui.moveTo(JEWEL_LOCATION[0], JEWEL_LOCATION[1], 0.1)
        craft()
        keyboard.press(Key.ctrl)
        time.sleep(0.01)
        pyautogui.click()
        keyboard.release(Key.ctrl)
        store()
    else:
        grabbing = True
        continue
