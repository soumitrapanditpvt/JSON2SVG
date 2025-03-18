# %%
import svgwrite
import json
import numpy as np 
from SVG_Floorplan import SVG_Floorplan
#from Scaled_Floorplan import Scaled_Floorplan
import os



# %%
#Path Variables
floorplan_path = r"C:\Users\smtrp\PrimeVision\PyVision\JSON_to_SVG\Floorplan_JSON_Files\\"
sortplan_path = r"C:\Users\smtrp\PrimeVision\PyVision\JSON_to_SVG\Sortplan_JSON_Files\\"
svg_file_path = r"C:\Users\smtrp\PrimeVision\PyVision\JSON_to_SVG\SVG_Files\\"

os.path.exists(floorplan_path) and os.path.exists(sortplan_path) and os.path.exists(svg_file_path)

# %%
#Floorplans:
test_floorplan1 = "1X1_CW.json"
test_floorplan2 = "3X2_USPS_CW.json"
test_floorplan3 = "floorplan_Chicago_V1.json"
test_floorplan4 = "floorplan_Indy.json"
test_floorplan5 = "floorplan_53_Dallas.json"
test_floorplan6 = "floorplan_48.json"
test_floorplan7 = "floorplan_50.json"
test_floorplan8 = "floorplan_indy_1.json"
test_floorplan9 = "USPS-Indy-left-floorplan.json"
test_floorplan10 = "USPS-Indy-right-floorplan.json"
test_floorplan11 = "floorplan 65.json"
test_floorplan12 = "floorplan 71.json"



# %%
#Sortplans:
test_floorplan1 = None
test_floorplan2 = None
test_floorplan3 = None
test_floorplan4 = "sortplan_Indy.json"
test_sortplan5 = "sortplan_25_Dallas.json"
test_sortplan6 = "sortplan_48.json"
test_sortplan7 = "sortplan_22.json"
test_sortplan8 = "sortplan_indy_1.json"
test_sortplan11 = "sortplan 29.json"
test_sortplan12 = "sortplan_30 1.json"

# %%
#Indicing:
idx = 12

# %%
floorplan = floorplan_path + globals()[f"test_floorplan{idx}"]
sortplan = sortplan_path + globals()[f"test_sortplan{idx}"]
if not(sortplan == None):
    print(os.path.exists(floorplan) and os.path.exists(sortplan))

else: 
    os.path.exists(floorplan)

# %%
svg_floorplan = SVG_Floorplan(floorplan_file=floorplan,sortplan_file=sortplan,svg_file=floorplan.replace(floorplan_path,svg_file_path).replace("json","svg"))

# %%
print(svg_floorplan)

# %%
svg_floorplan.x_max
svg_floorplan.x_min

# %%
svg_floorplan.y_max

# %%



