# 3D Printed Case

Enclosure for Texas Wildlife ID system.

## Print Settings
- Material: PETG or ABS for UV resistance
- Infill: 20-30%
- Wall: 3 perimeters
- Size: ~150x120x60mm

## Files
- `case.scad` – parametric OpenSCAD model with lid, solar bracket and cable gland
- `enclosure_base.stl` – base STL placeholder
- `enclosure_lid.stl` – lid STL placeholder
- `solar_bracket.stl` – L-bracket for solar panel mounting
- `cable_gland.stl` – weatherproof PG7 style gland body

## Parts
- case.scad – main enclosure with Pi5 standoffs, camera cutout, vents
- Lid optional

## Assembly
1. Print base and lid
2. Mount Pi5 to M2.5 standoffs
3. Coral TPU plugs into USB 3.0 port
4. SIM modem mounts on side bracket
5. Solar charge controller + battery in base compartment
6. Motor driver board on GPIO header
7. Camera module on ribbon cable through cutout
8. Seal with silicone gasket for weatherproofing

## Customization
Edit parameters at top of case.scad for your specific modules.
