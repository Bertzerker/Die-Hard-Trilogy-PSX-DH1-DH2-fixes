# Die Hard 2 calibration patch

Apply **Die Hard 2 Calibration Patch.ppf** to the same USA v1.1 Track 01 BIN
with the original Nuvee GunCon conversion used by the other patches.

Base-image SHA-256:
`1a2f348289285ad95cbaed49ffb535cc0d3792307a9a7d6c66fa6c486cdef3a1`

If you applied **Gun Patch Mister** or **Gun Patch Emulator**, undo that aiming
patch first or start with your original GunCon-patched backup. Calibration
replaces those fixed offsets; do not stack it with either aiming patch.
The **Die Hard 2 UI Patch** can remain installed. UI and calibration may be
applied in either order.

## Using calibration

1. Boot the patched game fresh and enter Die Hard 2. Do not load an old savestate.
2. On its title screen, press and release the gun's **grenade button**.
3. Aim at the **center of the white target box** and shoot once.
4. Release the trigger to return to the title screen, then start playing.

**Start cancels calibration.** The grenade button opens calibration only on
the title screen and retains its grenade function during gameplay. Repeat
calibration from the title screen if needed.

Calibration applies X/Y offsets for the current session. It is not saved to
the memory card, and a fresh boot starts with neutral offsets. One center shot
corrects an offset, not aiming scale errors near the screen edges.

## Validation and limits

The user tested this version successfully in DuckStation. Its generated code
matches the installed RAM test byte for byte. The PPF was applied and undone
against the supported base sectors; executable edits and regenerated EDC/ECC
were verified. Combination with the UI patch passed in both orders.

MiSTer/hardware, other revisions/regions, and second-controller-port operation
have not been validated. The prototype uses the diagnostic-string scratch
ranges identified in the original Nuvee notes; exhaustive diagnostic/error-path
coverage remains outstanding.

The PPF includes undo data. Use a PPF3-compatible patcher on Track 01 BIN, not
the CUE or CHD. Patch BIN first if you later rebuild a CHD.
