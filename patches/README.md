# Die Hard 1 and Die Hard 2 patches

- [Die Hard 1 Dual Shock.ppf](Die%20Hard%201%20Dual%20Shock.ppf): selectable
  dual-stick controls and analog support in the launcher and Die Hard 1 menus.
  Follow its [separate instructions and base-image requirements](Die%20Hard%201%20Dual%20Shock.md).
  **Press the Analog button on your joypad: analog mode does not activate automatically.**

The application and upgrading instructions below apply to the Die Hard 2 patches.

- [Die Hard 2 Calibration Patch.ppf](Die%20Hard%202%20Calibration%20Patch.ppf):
  grenade-button entry on the title screen and center-shot aiming calibration.
- [Die Hard 2 UI Patch.ppf](Die%20Hard%202%20UI%20Patch.ppf): corrected health
  badges, smaller counters at bottom left, smaller centered score, and removal
  of the controller-mode icon.

![Calibration screen](../screenshots/calibration.png)

See the [project README](../README.md) for both previews and build instructions,
and [calibration instructions](Calibration.md) for controls and limitations.

## Applying and upgrading

Use USA v1.1 SLUS-00119 Track 01 BIN with the original Nuvee USA Greatest Hits
GunCon conversion already installed. The supported base SHA-256 is:

`1a2f348289285ad95cbaed49ffb535cc0d3792307a9a7d6c66fa6c486cdef3a1`

Make a backup and apply either or both PPFs with a PPF3-compatible patcher.
Calibration and UI may be applied in either order. Patch the BIN, not the CUE
or CHD; retain the other tracks and matching CUE. Rebuild CHD afterward if needed.

The former Gun Patch Mister and Gun Patch Emulator are superseded. Undo an
installed fixed aiming patch before applying calibration, or use your original
GunCon-patched backup. Do not combine calibration with a fixed aiming profile.
The UI patch may remain installed.

Start from a fresh boot, not an old savestate. Normal memory-card saves can
still be used. Each PPF contains undo data. Use your patcher's undo operation
or restore your backup to remove it.

Both patches were checked for application, undo, executable edits, regenerated
EDC/ECC, and compatibility in both application orders. See
[Verification.json](Verification.json). Live calibration/UI testing passed in
DuckStation; hardware testing remains outstanding.
