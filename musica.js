/* =====================================================
   MÚSICA DE FONDO — pista original estilo synthwave
   Se genera en vivo con Web Audio (sin archivo de audio)
   y se repite en bucle infinito.

   Los navegadores no dejan sonar audio hasta que la persona
   interactúa con la página. Por eso:
   1) intenta sonar apenas carga;
   2) si el navegador lo bloquea, parte sola con el primer
      toque, clic o tecla en cualquier parte de la página.
   Se baja sola mientras el video del día suena con audio.
   ===================================================== */
(() => {
  'use strict';

  const AudioCtx = window.AudioContext || window.webkitAudioContext;
  if (!AudioCtx) {
    return;
  }

  const CONFIG = {
    bpm: 104,
    volume: 0.55,      // volumen general (0 a 1)
    duckVolume: 0.12,  // volumen mientras suena el video con audio
    fadeIn: 2.5        // segundos de entrada suave
  };

  const STEP = 60 / CONFIG.bpm / 4; // semicorchea
  const mtof = (m) => 440 * Math.pow(2, (m - 69) / 12);

  // La menor: Am – F – C – G (un compás cada uno)
  const CHORDS = [
    { root: 45, notes: [57, 60, 64] },
    { root: 41, notes: [53, 57, 60] },
    { root: 48, notes: [55, 60, 64] },
    { root: 43, notes: [55, 59, 62] }
  ];

  // Melodía de 4 compases: [paso (0-15), nota MIDI, duración en pasos]
  const MELODY = [
    [[0, 76, 3], [4, 74, 2], [6, 72, 2], [8, 74, 4], [12, 72, 2], [14, 69, 2]],
    [[0, 72, 6], [8, 69, 2], [10, 72, 2], [12, 74, 4]],
    [[0, 76, 3], [4, 79, 2], [6, 76, 2], [8, 74, 4], [12, 72, 4]],
    [[0, 74, 6], [8, 71, 2], [10, 74, 2], [12, 79, 4]]
  ];

  let ctx = null;
  let master = null;
  let bus = null;
  let delayIn = null;
  let noise = null;
  let nextTime = 0;
  let step = 0;
  let userMuted = false;
  let ducked = false;
  let fadedIn = false;

  function build() {
    ctx = new AudioCtx();

    master = ctx.createGain();
    master.gain.value = 0;
    const comp = ctx.createDynamicsCompressor();
    comp.threshold.value = -14;
    comp.ratio.value = 3;
    master.connect(comp);
    comp.connect(ctx.destination);

    bus = ctx.createGain();
    bus.connect(master);

    // Eco (delay) con retroalimentación filtrada
    delayIn = ctx.createGain();
    const delay = ctx.createDelay(1.5);
    delay.delayTime.value = STEP * 3;
    const feedback = ctx.createGain();
    feedback.gain.value = 0.38;
    const tone = ctx.createBiquadFilter();
    tone.type = 'lowpass';
    tone.frequency.value = 2400;
    const wet = ctx.createGain();
    wet.gain.value = 0.55;
    delayIn.connect(delay);
    delay.connect(tone);
    tone.connect(feedback);
    feedback.connect(delay);
    tone.connect(wet);
    wet.connect(bus);

    // Ruido blanco para batería
    noise = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
    const data = noise.getChannelData(0);
    for (let i = 0; i < data.length; i++) {
      data[i] = Math.random() * 2 - 1;
    }
  }

  function env(gainNode, t, peak, attack, decay) {
    const g = gainNode.gain;
    g.setValueAtTime(0.0001, t);
    g.exponentialRampToValueAtTime(peak, t + attack);
    g.exponentialRampToValueAtTime(0.0001, t + attack + decay);
  }

  // ---------- Instrumentos ----------
  function kick(t) {
    const o = ctx.createOscillator();
    const g = ctx.createGain();
    o.type = 'sine';
    o.frequency.setValueAtTime(150, t);
    o.frequency.exponentialRampToValueAtTime(42, t + 0.14);
    env(g, t, 0.95, 0.003, 0.38);
    o.connect(g);
    g.connect(bus);
    o.start(t);
    o.stop(t + 0.45);
  }

  function snare(t) {
    const n = ctx.createBufferSource();
    n.buffer = noise;
    const hp = ctx.createBiquadFilter();
    hp.type = 'highpass';
    hp.frequency.value = 1300;
    const g = ctx.createGain();
    env(g, t, 0.42, 0.002, 0.22);
    n.connect(hp);
    hp.connect(g);
    g.connect(bus);
    g.connect(delayIn);
    n.start(t);
    n.stop(t + 0.3);

    const o = ctx.createOscillator();
    const og = ctx.createGain();
    o.type = 'triangle';
    o.frequency.setValueAtTime(200, t);
    o.frequency.exponentialRampToValueAtTime(120, t + 0.1);
    env(og, t, 0.3, 0.002, 0.12);
    o.connect(og);
    og.connect(bus);
    o.start(t);
    o.stop(t + 0.2);
  }

  function hat(t, open) {
    const n = ctx.createBufferSource();
    n.buffer = noise;
    const hp = ctx.createBiquadFilter();
    hp.type = 'highpass';
    hp.frequency.value = 7500;
    const g = ctx.createGain();
    env(g, t, open ? 0.12 : 0.08, 0.002, open ? 0.18 : 0.05);
    n.connect(hp);
    hp.connect(g);
    g.connect(bus);
    n.start(t);
    n.stop(t + 0.25);
  }

  function bass(t, midi, dur) {
    const o = ctx.createOscillator();
    const f = ctx.createBiquadFilter();
    const g = ctx.createGain();
    o.type = 'sawtooth';
    o.frequency.value = mtof(midi);
    f.type = 'lowpass';
    f.Q.value = 6;
    f.frequency.setValueAtTime(900, t);
    f.frequency.exponentialRampToValueAtTime(180, t + dur);
    env(g, t, 0.3, 0.005, dur);
    o.connect(f);
    f.connect(g);
    g.connect(bus);
    o.start(t);
    o.stop(t + dur + 0.05);
  }

  function pad(t, notes, dur) {
    const f = ctx.createBiquadFilter();
    f.type = 'lowpass';
    f.frequency.setValueAtTime(700, t);
    f.frequency.linearRampToValueAtTime(1600, t + dur * 0.5);
    f.frequency.linearRampToValueAtTime(800, t + dur);
    const g = ctx.createGain();
    g.gain.setValueAtTime(0.0001, t);
    g.gain.linearRampToValueAtTime(0.1, t + 0.5);
    g.gain.setValueAtTime(0.1, t + dur - 0.3);
    g.gain.linearRampToValueAtTime(0.0001, t + dur + 0.2);
    f.connect(g);
    g.connect(bus);
    notes.forEach((m) => {
      [-8, 8].forEach((cents) => {
        const o = ctx.createOscillator();
        o.type = 'sawtooth';
        o.frequency.value = mtof(m);
        o.detune.value = cents;
        const og = ctx.createGain();
        og.gain.value = 0.22;
        o.connect(og);
        og.connect(f);
        o.start(t);
        o.stop(t + dur + 0.3);
      });
    });
  }

  function arp(t, midi) {
    const o = ctx.createOscillator();
    const f = ctx.createBiquadFilter();
    const g = ctx.createGain();
    o.type = 'square';
    o.frequency.value = mtof(midi);
    f.type = 'lowpass';
    f.frequency.value = 2600;
    env(g, t, 0.07, 0.004, 0.14);
    o.connect(f);
    f.connect(g);
    g.connect(bus);
    g.connect(delayIn);
    o.start(t);
    o.stop(t + 0.2);
  }

  function lead(t, midi, dur) {
    const o = ctx.createOscillator();
    const o2 = ctx.createOscillator();
    const lfo = ctx.createOscillator();
    const lfoGain = ctx.createGain();
    const f = ctx.createBiquadFilter();
    const g = ctx.createGain();
    o.type = 'sawtooth';
    o2.type = 'square';
    o.frequency.value = mtof(midi);
    o2.frequency.value = mtof(midi);
    o2.detune.value = 6;
    lfo.frequency.value = 5.5;
    lfoGain.gain.value = 9;
    lfo.connect(lfoGain);
    lfoGain.connect(o.detune);
    lfoGain.connect(o2.detune);
    f.type = 'lowpass';
    f.frequency.value = 2200;
    g.gain.setValueAtTime(0.0001, t);
    g.gain.linearRampToValueAtTime(0.06, t + 0.03);
    g.gain.setValueAtTime(0.06, t + dur * 0.8);
    g.gain.linearRampToValueAtTime(0.0001, t + dur);
    o.connect(f);
    o2.connect(f);
    f.connect(g);
    g.connect(bus);
    g.connect(delayIn);
    [o, o2, lfo].forEach((osc) => {
      osc.start(t);
      osc.stop(t + dur + 0.05);
    });
  }

  // ---------- Secuenciador ----------
  function playStep(s, t) {
    const bar = Math.floor(s / 16);
    const i = s % 16;
    const chord = CHORDS[bar % 4];
    const section = Math.floor(bar / 4); // bloques de 4 compases
    const drums = section >= 1;
    const melody = section >= 2 && section % 2 === 0;

    if (i === 0) {
      pad(t, chord.notes, STEP * 16);
    }

    if (i % 2 === 0) {
      bass(t, chord.root + (i % 4 === 2 ? 12 : 0), STEP * 1.7);
    }

    const pattern = [0, 1, 2, 1];
    if (i % 2 === 0) {
      arp(t, chord.notes[pattern[(i / 2) % 4]] + 12);
    }

    if (drums) {
      if (i === 0 || i === 8 || (i === 14 && bar % 4 === 3)) {
        kick(t);
      }
      if (i === 4 || i === 12) {
        snare(t);
      }
      if (i % 2 === 0) {
        hat(t, i % 4 === 2);
      }
    }

    if (melody) {
      MELODY[bar % 4].forEach(([at, note, len]) => {
        if (at === i) {
          lead(t, note, STEP * len);
        }
      });
    }
  }

  function scheduler() {
    if (!ctx) {
      return;
    }
    const lookahead = document.hidden ? 1.5 : 0.2;
    if (nextTime < ctx.currentTime) {
      nextTime = ctx.currentTime + 0.05;
    }
    while (nextTime < ctx.currentTime + lookahead) {
      playStep(step, nextTime);
      nextTime += STEP;
      step++;
    }
  }

  // ---------- Volumen ----------
  function targetVolume() {
    if (userMuted) {
      return 0;
    }
    return ducked ? CONFIG.duckVolume : CONFIG.volume;
  }

  function applyVolume(seconds) {
    if (!ctx) {
      return;
    }
    const g = master.gain;
    const now = ctx.currentTime;
    g.cancelScheduledValues(now);
    g.setValueAtTime(g.value, now);
    g.linearRampToValueAtTime(targetVolume(), now + seconds);
  }

  // ---------- Botón ----------
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'music-toggle';
  button.setAttribute('aria-label', 'Música de fondo');
  document.body.appendChild(button);

  function updateButton() {
    const running = ctx && ctx.state === 'running';
    button.classList.toggle('is-waiting', !running && !userMuted);
    button.classList.toggle('is-off', userMuted);
    button.setAttribute('aria-pressed', String(!userMuted));
    let label = 'Toca la pantalla para la música';
    if (userMuted) {
      label = 'Música: no';
    } else if (running) {
      label = 'Música: sí';
    }
    button.innerHTML = `<span class="mt-icon" aria-hidden="true">${userMuted ? '✕' : '♪'}</span><span class="mt-label">${label}</span>`;
    button.title = label;
  }

  // ---------- Arranque ----------
  function start() {
    if (!ctx) {
      build();
      nextTime = ctx.currentTime + 0.1;
      setInterval(scheduler, 25);
      ctx.onstatechange = () => {
        updateButton();
        if (ctx.state === 'running' && !fadedIn) {
          fadedIn = true;
          applyVolume(CONFIG.fadeIn);
        }
      };
    }
    if (ctx.state !== 'running') {
      ctx.resume().catch(() => {});
    }
    if (ctx.state === 'running' && !fadedIn) {
      fadedIn = true;
      applyVolume(CONFIG.fadeIn);
    }
    updateButton();
  }

  const unlockEvents = ['pointerdown', 'keydown', 'touchend', 'click'];
  function unlock() {
    start();
    if (ctx && ctx.state === 'running') {
      unlockEvents.forEach((ev) => document.removeEventListener(ev, unlock, true));
    }
  }
  unlockEvents.forEach((ev) => document.addEventListener(ev, unlock, true));

  button.addEventListener('click', (event) => {
    event.stopPropagation();
    if (!ctx || ctx.state !== 'running') {
      userMuted = false;
      start();
      return;
    }
    userMuted = !userMuted;
    applyVolume(0.4);
    updateButton();
  });

  // Baja la música mientras el video suena con audio
  const video = document.getElementById('finalVideo');
  if (video) {
    const syncDuck = () => {
      ducked = !video.paused && !video.ended && !video.muted;
      applyVolume(0.6);
    };
    ['play', 'playing', 'pause', 'ended', 'volumechange'].forEach((ev) => video.addEventListener(ev, syncDuck));
  }

  // Intenta sonar apenas carga (algunos navegadores lo permiten)
  start();
})();
