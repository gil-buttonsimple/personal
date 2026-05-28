# Vehicle Profile — System Rebuild Document

**Vehicle:** 1999 Volkswagen Eurovan (T4) — VR6 Automatic

**Last Updated:** 2026-05-28

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

| Task | Priority | Tags |
|------|----------|------|
| Starlink roof mount: rattle fix + cable strain relief | P1 | |
| Wiring cleanup (mystery wires, interior, bypass) | P1 | |
| Add GPS antenna to roof mount + cables | P1 | |
| Diagnose cyl 6 misfire (swap coil pack/wire first) | P1 | |
| Install replacement relay 175 (ordered) | P2 | |
| Electrical system build-out (battery + distribution + panel) | P2 | |
| EVAP system rebuild (mounting + hose replacement) | P2 | |
| Tire rotation schedule | P2 | |
| Research compact self-powered subwoofer | | Decision |
| Cab roof air deflector (keep/modify/remove?) | | Decision |
| Clear SRS airbag fault | | |
| Rear tires: longer valve stems | | |
| Create vehicle cheat sheet | | |
| Secure cooler | | |
| Table conversion (loft boards) | | |
| Loft improvements: connect boards with webbing | | |
| Antenna upgrade (FM reception) | | |
| New seats | | |

---

# 4. System Overview

| System             | Status       | Notes |
|--------------------|--------------|-------|
| Fuel / EVAP        | Unstable     | Vent routing / mounting issue |
| Electrical         | Built        | 12V system installed pre-trip; documentation to be recovered |
| Network (Starlink) | Planned      | Direct 12V integration |
| Audio / Antenna    | Interim      | Direct-drive via Alpine; 6x9 upgrade pending |
| Interior Structure | Cleared      | Ready for rebuild |
| Mechanical         | Minor issues | Ignition interlock |

---

# 5. System Designs (High-Level)

## 5.1 EVAP System
- Replace hoses:
  - 5/8" tank vent
  - 1/2" fresh air
  - 1/4" purge
- Ensure:
  - Smooth routing
  - No kinks
  - Upright canister orientation
  - Stable mounting

## 5.2 Electrical System

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

## 5.3 Starlink Integration
- Direct 12V wiring from fuse block
- Panel-mounted barrel socket
- 10-15A fused circuit
- No USB-C conversion

## 5.4 Antenna System
- Roof-mounted amplified antenna
- Mast-style preferred (not shark fin)
- Requirements:
  - Powered via head unit antenna wire
  - Proper metal ground plane
  - Clean roof installation

---

# 6. Completed Work

- Full removal of Winnebago camper components (except pop-top)
- Rear heater removed
- Coach electrical system removed
- Floor removed
- Water pooling issue resolved
- Seatbelt repaired
- EVAP canister temporarily stabilized
- Boston Acoustics crossover: passenger side amplified crossover identified and bypassed
- Interim audio: door woofer wired direct to Alpine (4-ohm stable load); tweeter bypassed
- Blower fan clicking resolved (zip tie in squirrel cage)
- Knee panels removed (staying off)
- Relay 175 identified (3A0 927 181, shift lock / neutral safety relay)
- Starting solution decided: replace relay (over push button bypass)
- Shifter housing reassembled
- Shifter illumination bulb holder identified and verified against spec
- Clock spring / spiral cable identified
- Ignition / key retention: resolved
- Head unit replaced: Kenwood KMM-X705 installed

---

# 7. Constraints & Dependencies

## Structural
- Removal of Winnebago mounting points affects multiple systems

## Electrical
- All systems depend on new 12V architecture

## Roof
- Antenna and cab roof air deflector decisions interact

---

# 8. System Inventory (Concrete Data — No Design Discussion)

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
- Battery type: LiFePO4 (model TBD)
- System type: custom 12V distribution

## Starlink
- Model: Starlink Mini
- Power: 12V DC barrel input

## Audio / Head Unit
- Brand: Kenwood KMM-X705 (installed)
- Interim config: door woofer direct (4-ohm); tweeter bypassed
- Current antenna: passive aftermarket (low quality)
- Issue: poor FM reception (fading, limited stations)

## Seat Base
- Bolt pattern:
  - Width: 13 1/8"
  - Depth: 11 1/4"
- Issue: seat tilts backward (bucket effect)

## Interior -- Bed Platform Components
- Slat length: 42 13/16" (42.8125")
- Slat width: 2 1/2" (2.5")
- Slat thickness: 3/4" (0.75")
- Existing slats confirmed comfortable; dimensions to be reused as baseline

## Roof / Exterior
- Pop-up roof: retained
- Cab roof air deflector: present (Winnebago); keep/modify/remove decision open

## Exterior Openings
- Former camper ports removed (water, shore power)
- Sealing complete
- No water intrusion observed
