# CLARIS

**Clinical Alarm Reconstruction & Interpretability System**

> An explainable clinical decision support system that evaluates the credibility of ICU physiological alarms using synchronized ECG, arterial blood pressure (ABP), and SpO₂ waveforms within the patient's clinical context.

---

## Research Question

**Can multimodal physiological evidence and patient clinical context improve the credibility assessment of ICU monitor alarms without replacing existing bedside monitoring?**

## Overview

CLARIS is a biomedical AI research project that addresses **ICU alarm fatigue** through explainable alarm interpretation.

Instead of predicting diseases or replacing bedside monitors, CLARIS reconstructs the physiological context surrounding an alarm using synchronized ECG, arterial blood pressure (ABP), and pulse oximetry (SpO₂) waveforms. The system provides clinicians with contextual playback and an evidence-based assessment of alarm credibility.

## Clinical Problem

ICU monitors generate hundreds of physiological alarms per patient every day, with a substantial proportion being false or non-actionable. This contributes to alarm fatigue, increased cognitive workload, delayed responses, and reduced trust in monitoring systems.

CLARIS is designed to support clinician judgement by determining **how trustworthy an alarm is**, rather than how severe it appears.

## Current Progress

### Phase 1 — Clinical Foundation

- [x] CLARIS definitions & terminology
- [x] Problem statement
- [x] Alarm credibility framework
- [x] ICU alarm fatigue literature review (4 papers)
- [x] Literature synthesis
- [ ] ECG artifact & signal reliability
- [ ] ABP waveform reliability
- [ ] SpO₂ & plethysmography
- [ ] Clinical Context Profile (CCP)

## Repository Structure

| Folder | Purpose |
|---------|----------|
| `docs/` | Scientific documentation, literature reviews & project foundation |
| `src/` | Core implementation of the CLARIS pipeline |
| `notebooks/` | Research experiments and exploratory analysis |
| `data/` | Public ICU datasets and preprocessing workflows |

---

**Status:** Active biomedical engineering research project.
