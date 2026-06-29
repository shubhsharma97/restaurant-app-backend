---
name: passlib bcrypt compatibility
description: passlib 1.7.4 is incompatible with bcrypt >= 4.1; must pin bcrypt==4.0.1
---

# passlib + bcrypt Version Compatibility

## Rule
Always pin `bcrypt==4.0.1` when using `passlib[bcrypt]==1.7.4`.

**Why:** Replit installs the latest bcrypt (5.x as of mid-2026), which removed the `__about__` attribute that passlib uses for version detection. This causes passlib's backend init to raise `ValueError: password cannot be longer than 72 bytes` during startup — resulting in a 500 on any endpoint that hashes passwords.

**How to apply:** Add `bcrypt==4.0.1` as an explicit line in `requirements.txt` below `passlib[bcrypt]==1.7.4` so pip downgrades/pins it correctly.
