# CLARIS — Documentation

This directory contains the research, problem definition, prior-art analysis, and design documentation for CLARIS.

## Project Foundation

- [`problem.md`](problem.md) — Initial definition of the clinical problem addressed by CLARIS.
- [`definitions.md`](definitions.md) — Core terminology and concepts used throughout the project.

## Phase 0 — Research

- [`icu_alarm_fatigue.md`](icu_alarm_fatigue.md) — Literature review on ICU alarm fatigue, false alarms, and non-actionable alarms.
- [`literature_synthesis.md`](literature_synthesis.md) — High-level synthesis of the literature reviewed during the initial research phase.
- [`signal_reliability.md`](signal_reliability.md) — Review of ECG, ABP, and PPG/SpO₂ reliability, artifacts, and signal-quality assessment.
- [`multimodal_prior_art.md`](multimodal_prior_art.md) — Review of multimodal alarm validation, cross-signal evidence, and temporal reasoning.
- [`novelty_and_gap.md`](novelty_and_gap.md) — Prior-art analysis, novelty boundary, and the proposed CLARIS research gap.

## Current Research Direction

CLARIS is being developed as an evidence-centric framework for interpreting ICU monitor alarms.

Rather than treating an alarm as simply true or false, CLARIS aims to examine the physiological evidence surrounding an alarm event and determine:

- what evidence supports the alarm
- what evidence contradicts the alarm
- what evidence is unreliable
- what evidence is missing
- how the evidence evolves over time
- why the resulting alarm interpretation is credible or uncertain

The initial implementation will focus on ventricular tachycardia (VT) alarms using ECG, ABP, and PPG waveforms.

## Phase 0 Status

The initial literature and prior-art investigation is sufficiently complete to begin system design and prototype development.

The next phase will focus on:

1. Dataset selection
2. Alarm-event definition
3. Temporal window design
4. Signal-quality inputs
5. Physiological evidence extraction
6. Evidence representation
7. Evidence-reconciliation logic
8. Evaluation methodology
9. Prototype implementation
