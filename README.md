# ArchBooBlender #
Arch generator scripts coded for Blender.

Maths adapted from Steve Gatesy's original Maya Mel Scripts.

In progress... (awaiting addon format)

## Insallation

Download the zip, install as an addon, and away you go.

## Instructions:

- Click 'create prism' to setup the prism and locators.  You should only do this once, as if you press it again it'll delete any existing prism/locators and regenerate them, so you'll loose any keyframing etc.
- move mpLocatorA, mpLocatorB, and heelLocator to correct positions.  You can easily select them with the buttons at the top of the UI
- Ensure prism is upwards (so mpLocatorA will always be to left of B, regardless of side of foot.
- select the mesh you want to calculate RAV for using the object picker (this will auto-update the archname)
- select left/right and foot/track accordingly.
- change arch name if you want.
- hit calculate.
- Values can be seen directly in object properties, or there's an export button that will put all arch's values into a CSV file.

## Known Issues:
- Tracks need to be non-manifold i.e. surfaces, rather than solids.  Don't know why. (feet can be manifold or not)
- If you hit undo (ctrl-Z) after pressing calculate, blender crashes hard and closes.  Don't know why.
- 'create prism' _will_ delete current prism+associate locators, losing any keyframing.

## ToDo:

- Add an 'are you sure' dialogue to 'create prism' if prism already exists.
- See if we can put a little 'print' button in the custom properties that would let you copy and paste values for just that one object.
- Possibly add prism height to the AMB UI, rather than leave it just on the prism's custom properties tab.
