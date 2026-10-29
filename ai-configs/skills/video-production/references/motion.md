# Motion

For HyperFrames animation, read `/hyperframes-animation` and follow its runtime and seek-safety rules. For continuous motion across scenes, also consult `/motion-doctrine` when available. Those references own the framework mechanics; this file records the personal motion preference.

- Use GSAP timelines for authored motion when the project uses GSAP. Avoid defaulting to `linear` easing: most movement should accelerate through the middle and ease into a deliberate stop, such as a suitable `power2.inOut` or `power3.inOut` curve.
- Vary movement to fit the moment. Entrances can ease out; exits can accelerate; scene changes can carry momentum. Keep motion connected to what the viewer should notice.
- Use a restrained spring or overshoot occasionally to make an element feel like it settles into place. Keep the bounce brief and intentional; do not make every object wobble or bounce.
- Stagger related reveals to follow the spoken idea. Avoid animating every element at once or adding motion that competes with narration.
