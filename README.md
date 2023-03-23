# ArchBooBlender #
Arch generator scripts coded for Blender.

Maths adapted from Steve Gatesy's original Maya Mel Scripts.

In progress... (awaiting addon format)

## Insallation

Download the zip, install as an addon, and away you go.

## Instructions:

- move mpLocatorA, mpLocatorB, and heelLocator to correct positions.  You can easily select them with the buttons at the top of the UI
- Ensure prism is upwards (so mpLocatorA will always be to left of B, regardless of side of foot.
- select the mesh you want to calculate RAV for using the object picker (this will auto-update the archname)
- select left/right and foot/track accordingly.
- change arch name if you want.
- hit calculate.
- Values can be seen directly in object properties, or there's an export button that will put all arch's values into a CSV file.

## Known Issues:
- Tracks need to be non-manifold i.e. surfaces, rather than solids.  Don't know why.
- If you hit undo (ctrl-Z) after pressing calculate, blender crashes hard and closes.  Don't know why.

## ToDo:

### Setupfile:

~~- Just make relation lines invisible by default.~~

### Makerfile:

~~- Change object selection from text entry to object picker~~

~~- Auto name arch model based on object picked~~

~~- do ALL the maths, and add to arch model as custom properties.~~ moved to mathpart (and mostly done)

### MathsPart

~~- Roll.  Need to get creative.~~

~~- Assign variables to arch object as custom properties (UI work needed here)~~

### Overall

~~- change to a add-on structure

~~- remove the close button when this happens.~~
