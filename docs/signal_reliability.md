# CLARIS — Signal Reliability

## Purpose

CLARIS depends on the reliability of the physiological signals surrounding an alarm event.

A monitor alarm cannot be interpreted from the displayed value alone. The underlying waveform may contain motion artifact, baseline instability, signal dropout, clipping, noise, or other distortions that can produce misleading measurements.

This section summarizes the literature reviewed on the reliability of the three primary signals considered for CLARIS:

- ECG
- Arterial Blood Pressure (ABP)
- Photoplethysmography (PPG) / SpO₂

A central conclusion from the literature is that **signal quality is not equivalent to physiological truth**. Signal quality should therefore be treated as an input to alarm interpretation rather than as the final decision.

---

# 1. ECG Reliability

## 1.1 ECG as a physiological signal

The ECG represents the electrical activity of the heart.

Important waveform components include:

- P wave
- QRS complex
- T wave
- RR intervals
- QRS morphology
- beat-to-beat timing

For CLARIS, ECG provides the primary electrical evidence surrounding an arrhythmia alarm.

A reliable ECG should provide sufficiently clear and temporally consistent cardiac complexes to allow physiological interpretation.

---

## 1.2 ECG morphology

Research on automated ECG waveform classification demonstrates that ECG interpretation can use:

- P-QRS-T morphology
- QRS amplitude
- RR intervals
- waveform regularity
- temporal coherence between beats
- spatial coherence across multiple ECG leads

Complex QRS morphologies should not automatically be interpreted as noise. They may represent genuine physiological or conduction abnormalities.

### Relevance to CLARIS

CLARIS should therefore avoid a simplistic rule such as:

> unusual waveform = artifact

Instead, ECG evidence should consider:

1. waveform morphology
2. temporal consistency
3. multilead agreement
4. signal quality
5. relationship to other physiological signals

---

## 1.3 ECG artifacts

Common sources of ECG distortion include:

- baseline wander
- muscle / EMG artifact
- motion
- electrode problems
- electromagnetic interference
- respiration-related variation
- low-amplitude QRS complexes
- pacing-related morphology
- conduction abnormalities

ICU studies have shown that poor-quality ECG signals are strongly associated with false arrhythmia alarms.

One ICU study found that false alarms were associated with substantially greater baseline instability and increased high-frequency and EMG noise.

---

## 1.4 ECG Signal Quality Assessment

Several approaches have been developed to assess ECG signal quality.

Common approaches use:

- amplitude characteristics
- baseline characteristics
- QRS detectability
- beat-to-beat consistency
- morphology
- signal-to-noise characteristics
- signal quality indices (SQIs)

Research has also investigated arrhythmia-specific signal quality assessment because abnormal physiological rhythms can otherwise be incorrectly classified as poor-quality signals.

### Important CLARIS implication

A signal-quality system must distinguish between:

```text
poor signal quality
        vs.
unusual but genuine physiology
