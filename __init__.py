bl_info = {
    "name": "ArchBooMaker2023Blender",
    "author": "Peter L. Falkingham (with help from Bing/ChatGPT)",
    "version": (1, 0),
    "blender": (3, 4, 1),
    "location": "",
    "description": "Addon for generating RAV and other variables of foot and track arches",
    "warning": "",
    "doc_url": "",
    "category": ""
}

#this was implemented without me really knowing what it does - I didn't really understand declaring a module at the time.  It all works, but aplogies for it not being as straightfoward as my other addons
if "bpy" in locals():
    import importlib
    if "ArchBooMaker2023B" in locals():
        importlib.reload(ArchBooMaker2023B)
    if "ArchBooSetup2023B" in locals():
        importlib.reload(ArchBooSetup2023B)
    if "exportValues" in locals():
        importlib.reload(exportValues)
    if "MathsPart" in locals():
        importlib.reload(MathsPart)
else:
    from . import ArchBooMaker2023B
    from . import ArchBooSetup2023B
    from . import exportValues
    from . import MathsPart

def register():
    ArchBooMaker2023B.register()
    ArchBooSetup2023B.register()
    exportValues.register()
    MathsPart.register()

def unregister():
    ArchBooMaker2023B.unregister()
    ArchBooSetup2023B.unregister()
    exportValues.unregister()
    MathsPart.unregister()