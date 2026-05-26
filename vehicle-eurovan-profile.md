# Vehicle Profile — System Rebuild Document

**Vehicle:** 1999 Volkswagen Eurovan (T4) — VR6 Automatic

**Last Updated:** 2026-05-13

---

# 1. Build Intent

> Rebuild as a **simple, modular camper system** after removal of Winnebago integrations.

**Principles**
- Preserve core camper function (sleeping, power, connectivity)
- Reduce system complexity
- Eliminate hidden dependencies from legacy RV integration
- Favor direct, understandable systems
- Modular and serviceable

---

# 2. Current Phase

> **Post-demolition → System reconstruction**

- All legacy Winnebago systems removed (except pop-top)
- Core vehicle intact
- Rebuilding independent systems from scratch

---

# 3. Active Todos

## Eurovan (main)
- [ ] EVAP system rebuild (mounting + hose replacement)
- [ ] Electrical system build-out (battery + distribution)
- [ ] Antenna upgrade (FM reception fix)
- [ ] Interior electrical panel (flush mount)
- [ ] Ignition / key retention -- see Bus trip finds below, status unresolved

## Bus trip finds (May 2026)

**Ignition / electrical -- status: unresolved, multiple open questions**
- Key lockout: removed shifter housing during trip; key started working (cause unclear -- broken piece of thin plastic sheeting inside shifter was found and not replaced on reassembly)
- Shifter housing is currently disassembled and not reassembled; deferred after starting issue below
- Starting failure: solenoid relay failed; guy in New Orleans helped wire starter directly to positive battery terminal; currently starting by touching two wires together
- [ ] Test relay before replacing -- may still be good
- [ ] Decide on permanent starting solution: button wired to bypass, or remove key ignition and replace with a switch
- [ ] Reassemble shifter housing (or decide to eliminate it as part of switch conversion)
- [ ] Trace mystery wires under passenger dash (black + green, likely old amp -- may connect to door locks; do not remove until traced)

**Engine**
- [ ] Cyl 6 misfire on acceleration (VR6); swap coil pack/wire to another cylinder first to diagnose

**HVAC / blower**
- [ ] Blower fan clicking: remove motor via lower passenger dash panel, inspect for debris, check bearing
- [ ] Clean windshield cowl intake -- debris likely entering and reaching blower

**Tires**
- [ ] Rear tires: get longer valve stems at next service
- [ ] Set up tire rotation schedule (check recommended interval for VR6 Automatic)

**Audio**
- [ ] Evaluate Kenwood KMM-X705 digital media receiver
- [ ] Research compact self-powered subwoofer for T4 cabin (8" or 10"; see what others have built)
- [ ] Door panel modifications for upgraded speakers

**Exterior / systems**
- [ ] Starlink: fix roof mount rattle, add cable strain relief
- [ ] Mosquito barrier for back opening (velcro or snaps OK)

**Interior**
- [ ] Secure cooler -- add tie-down solution
- [ ] Loft: investigate board attachment + table conversion (removable legs)
- [ ] Look into swivel base plate for car seat adaptation
- [ ] Rattle diagnosis: find riding companion for half-day detection session
- [ ] Create vehicle cheat sheet: tire pressure (45 psi), oil type, rotation interval, fluids

## Loft Bed sub-project (see vehicle-eurovan-loft-bed for design spec)
- [ ] Decide final material (hardwood vs plywood)
- [ ] Pick hardwood species if going that route (poplar / maple / oak / teak)
- [ ] Confirm final slat count / bed length
- [ ] Source materials
- [ ] Cut to spec (length 42 13/16", width 2.5–3")
- [ ] Sand edges
- [ ] Build webbing/hinge system for accordion panels
- [ ] Test fit in pop-top

---

# 4. System Overview

| System            | Status        | Notes |
|-------------------|---------------|-------|
| Fuel / EVAP       | Unstable      | Vent routing / mounting issue |
| Electrical        | Not built     | New architecture defined |
| Network (Starlink)| Planned       | Direct 12V integration |
| Audio / Antenna   | Degraded      | Poor reception |
| Interior Structure| Cleared       | Ready for rebuild |
| Mechanical        | Minor issues  | Ignition interlock |

---

# 5. Active Problems (Priority Order)

## 5.1 EVAP System (Critical)
- Tank overpressure (fuel spray when opening cap)
- Exhaust pulsing ("whomping")
- Likely cause: vent restriction due to routing / unstable mounting
- Status: temporarily stabilized
- Required:
- Permanent mounting solution
- Full hose replacement
- Routing verification (no kinks, correct orientation)

## 5.2 Electrical System (Blocking)
- No installed system
- Required for all downstream systems

## 5.3 Antenna / Radio (Quality Issue)
- Poor FM reception
- Likely due to low-quality passive antenna

## 5.4 Ignition Key Retention (Mechanical)
- Key stuck in ignition
- Related to automatic shifter interlock cable
- Status not yet confirmed resolved

---

# 6. System Designs (High-Level)

## 6.1 EVAP System
- Replace hoses:
- 5/8" tank vent
- 1/2" fresh air
- 1/4" purge
- Ensure:
- Smooth routing
- No kinks
- Upright canister orientation
- Stable mounting

## 6.2 Electrical System

**Architecture**
- Battery → main fuse → disconnect → fuse block
- Separate negative bus
- Dedicated circuits

**Loads**
- Starlink Mini (12V)
- USB outlets
- Lighting (with integrated USB)
- 12V refrigerator
- Accessory circuits

**Integration**
- Flush-mounted 12V panel (wood)
- No AC dependency

## 6.3 Starlink Integration
- Direct 12V wiring from fuse block
- Panel-mounted barrel socket
- 10–15A fused circuit
- No USB-C conversion

## 6.4 Antenna System
- Roof-mounted amplified antenna
- Mast-style preferred (not shark fin)
- Requirements:
- Powered via head unit antenna wire
- Proper metal ground plane
- Clean roof installation

---

# 7. Completed Work

- Full removal of Winnebago camper components (except pop-top)
- Rear heater removed
- Coach electrical system removed
- Floor removed
- Water pooling issue resolved
- Seatbelt repaired
- EVAP canister temporarily stabilized

---

# 8. Open Decisions

- Final EVAP mounting design
- Antenna model and placement
- Seat base correction approach
- Roof fairing modification decision

---

# 9. Constraints & Dependencies

## Structural
- Removal of Winnebago mounting points affects multiple systems

## Electrical
- All systems depend on new 12V architecture

## Roof
- Antenna and fairing decisions interact

---

# 10. System Inventory (Concrete Data — No Design Discussion)

## Vehicle
- Platform: T4
- Engine: VR6
- Transmission: Automatic

## Fuel / EVAP
- Charcoal canister: present, temporarily secured
- Hose sizes:
- 5/8" (tank vent)
- 1/2" (fresh air)
- 1/4" (purge)

## Electrical (Planned)
- Battery type: LiFePO₄ (model TBD)
- System type: custom 12V distribution

## Starlink
- Model: Starlink Mini
- Power: 12V DC barrel input

## Audio / Head Unit
- Brand: Kenwood
- Model: TBD
- Current antenna: passive aftermarket (low quality)
- Issue: poor FM reception (fading, limited stations)

## Seat Base
- Bolt pattern:
- Width: 13 1/8"
- Depth: 11 1/4"
- Issue: seat tilts backward (bucket effect)

## Interior — Bed Platform Components
- Slat length: 42 13/16" (42.8125")
- Slat width: 2 1/2" (2.5")
- Slat thickness: 3/4" (0.75")
- Notes:
- Existing slats confirmed comfortable
- Dimensions to be reused as baseline

## Roof / Exterior
- Pop-up roof: retained
- Front fairing: present (Winnebago)
- Status: modification under consideration

## Exterior Openings
- Former camper ports removed (water, shore power)
- Sealing complete
- No water intrusion observed

---

# 11. Deferred Work (Do Not Expand Here)

- Interior layout and storage
- Cosmetic work
- Non-critical comfort features

> Move detailed exploration of these items to separate documents when needed