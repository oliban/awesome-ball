# Stick Hockey Penguin TODO List

- [X] Find/create `sword_hit.wav` sound file (code now attempts to load it).
- [ ] Manually update sword collision code (around lines 1248 & 1295) to use `loaded_sounds.get('sword_hit', ...)` instead of placeholders.
- [ ] Test SWORD power-up functionality (appearance, animation, puck hits, player hits).
- [ ] Refine sword-player collision detection (currently uses `clipline`, could be more precise).
- [ ] Improve sword swing animation (currently matches stick/leg).
- [ ] Balance SWORD power-up parameters (duration, forces) after testing.
- [X] Add SWORD constants (duration, colors, forces etc.)
- [X] Add `SWORD` to `POWERUP_TYPES` list.
- [X] Add `is_sword`, `sword_angle` to `StickMan.__init__`.
- [X] Add SWORD timer handling in `StickMan.update`.
- [X] Add SWORD drawing logic in `StickMan.draw`.
- [X] Add SWORD puck collision logic in main loop.
- [X] Add SWORD player collision logic in main loop.
- [X] Add SWORD display text/color to UI dictionaries. 