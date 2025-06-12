# A collection of basic tools for EVE: Online

A collection of lightweight tools for analysis and situational awareness in *EVE: Online*

## Hammerlock

> “[The hammerlock](https://youtu.be/P2iGCgIytO4?t=67)” (from *The Expanse*) refers to a critical distance at which evasive maneuvers are no longer feasible.

In *EVE: Online*, velocity and agility determines control of the encounter. One counter to superior velocity or agility is the **slingshot**: a maneuver where the pilot temporarily burns away from the pursuer, then reverses course to force a head-on approach. If timed correctly, this can break an orbit or create an escape window.

This tactic exploits the discrete simulation model of EVE’s physics engine. Ships update velocity vectors at 1-second intervals using discerete-time equations of motion. *Hammerlock* models this numerically to estimate the point where slingshots become infeasible based on ship stats.

**Use Case:**  
Reduce pilot cognitive load by identifying adversaries (based on ship class and stats) for which you must maintain manual position control to avoid being captured.

**Status:**  
- Basic simulation implemented 
- Parameter database for adverserial ship profiles and interpolation of engagement envelopes

---

## Intelligence Scraper

A passive tool to monitor unusual in-game activity, such as:

- Stargate camps
- Deployment or destruction of exotic or high-value modules (e.g., officer modules)  

**Use Case:**  
Supports solo and small-gang roamers with context on local threats and high-value targets.

---

## Notes

This is a hobby project used to prototype PvP analysis tools.
