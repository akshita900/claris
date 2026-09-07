# CLARIS — Multimodal Prior Art & Temporal Reasoning

## Purpose

CLARIS evaluates an ICU alarm using the physiological evidence surrounding the alarm event rather than relying on a single displayed monitor value.

The system considers multiple physiological signals, their reliability, their physiological behavior, and their temporal relationships.

The primary signals considered for the initial CLARIS prototype are:

- ECG
- Arterial Blood Pressure (ABP)
- Photoplethysmography (PPG)

The purpose of this review is to establish what has already been demonstrated in the literature and to identify the remaining research gap for CLARIS.

---

## 1. ECG and ABP

ECG represents the electrical activity of the heart, while ABP provides information about the resulting hemodynamic response.

Conceptually:

ECG electrical activity  
→ cardiac mechanical activity  
→ arterial pressure response

This physiological relationship makes ABP useful for evaluating ECG-based arrhythmia alarms.

### Aboukhalil et al. — Reducing False Alarm Rates for Critical Arrhythmias Using the Arterial Blood Pressure Waveform

Aboukhalil et al. investigated whether the ABP waveform could be used to reduce false critical arrhythmia alarms generated from ECG.

The study used MIMIC II data containing:

- 447 adult patient records
- 5,386 critical ECG arrhythmia alarms
- 41,301 hours of simultaneous ECG and ABP

The alarm categories included:

- asystole
- extreme bradycardia
- extreme tachycardia
- ventricular tachycardia
- ventricular tachycardia / ventricular fibrillation

The method examined ABP morphology and timing around ECG alarms and used ABP quality assessment before applying the information for alarm suppression.

The study reduced the overall false-alarm rate from 42.7% to 17.2% and suppressed approximately 59.7% of false alarms.

### Relevance to CLARIS

This establishes ECG–ABP corroboration as prior art.

The important distinction is that the existing system primarily asks whether an alarm should be suppressed.

CLARIS instead aims to represent the evidence surrounding the alarm explicitly, including:

- signal reliability
- physiological evidence
- supporting evidence
- contradictory evidence
- missing evidence
- temporal evolution

Therefore, ECG–ABP corroboration itself is not considered a novel contribution of CLARIS.

---

# 2. ECG and PPG

ECG and PPG provide complementary information about cardiovascular activity.

ECG captures electrical cardiac activity, while PPG captures changes in peripheral blood volume associated with the pulse.

A simplified relationship is:

ECG electrical event  
→ mechanical cardiac activity  
→ peripheral pulse  
→ PPG response

The two signals therefore should not necessarily be expected to occur at exactly the same timestamp.

### Existing research

Previous studies have used PPG as a supplementary source of pulse information for heart-rate and rhythm monitoring.

Agreement between ECG and PPG can provide additional physiological evidence.

However, disagreement does not automatically mean that one of the signals is incorrect.

Potential causes of disagreement include:

- low peripheral perfusion
- motion artifact
- sensor displacement
- weak peripheral pulses
- short RR intervals
- modality-specific limitations
- physiological delay

### Relevance to CLARIS

CLARIS should therefore evaluate ECG–PPG disagreement together with:

1. signal quality
2. physiological plausibility
3. temporal alignment
4. event duration
5. evidence from other available signals

The principle is:

> Cross-signal disagreement is evidence that requires interpretation, not automatic proof of a false alarm.

---

# 3. ECG, ABP and PPG

The combination of ECG, ABP and PPG has already been investigated for ICU alarm validation.

The signals provide different physiological perspectives:

| Signal | Primary information |
|---|---|
| ECG | Electrical cardiac activity |
| ABP | Hemodynamic response |
| PPG | Peripheral pulse response |

This creates the possibility of checking whether observations from multiple signals are physiologically consistent.

For example:

ECG shows a rapid ventricular rhythm  
+  
ABP shows corresponding arterial pulses  
+  
PPG shows corresponding peripheral pulses

This provides multimodal evidence consistent with the alarm.

Conversely:

ECG indicates an arrhythmia  
+  
high-quality ABP does not show a corresponding pulsatile response

may provide evidence against the interpretation.

However, such reasoning must account for signal quality and physiological timing.

---

# 4. PhysioNet/CinC 2015 Challenge

The PhysioNet/CinC 2015 Challenge focused on reducing false alarms associated with five life-threatening arrhythmias:

- asystole
- extreme bradycardia
- extreme tachycardia
- ventricular tachycardia
- ventricular fibrillation

The dataset contained 1,250 multi-parameter ICU alarm segments:

- 750 training records
- 500 hidden test records

Available signals included:

- two ECG leads
- ABP
- PPG
- respiration

The records contained approximately five minutes before the alarm and additional data following the alarm.

Expert annotations included categories such as:

- true
- false
- reject
- uncertain

Multiple approaches were investigated, including:

- ECG QRS analysis
- ABP pulse detection
- PPG signal-quality assessment
- dynamic time warping
- multimodal fusion
- tachogram correlation

The challenge demonstrated that multimodal physiological signals can substantially improve ICU alarm validation.

### Relevance to CLARIS

This establishes multimodal ICU alarm validation as existing prior art.

CLARIS therefore does not claim novelty simply from combining ECG, ABP and PPG.

The research question must move beyond binary alarm classification or false-alarm suppression.

---

# 5. Cross-Signal Agreement

Cross-signal agreement has been used as evidence in existing ICU alarm validation systems.

For example:

ECG detects a rapid rhythm  
→ ABP shows corresponding arterial pulses  
→ PPG shows corresponding peripheral pulses

When multiple reliable signals demonstrate physiologically consistent behavior, confidence in the alarm interpretation can increase.

However, agreement alone is not sufficient evidence.

Two signals may agree because they are affected by:

- a shared artifact
- a common source of noise
- correlated measurement errors

Therefore:

> Agreement should be treated as evidence rather than proof.

Signal quality and physiological plausibility remain necessary.

---

# 6. Cross-Signal Contradiction

Cross-signal contradiction is also represented in existing ICU alarm adjudication research.

For example:

ECG indicates ventricular tachycardia  
→ ABP quality is high  
→ ABP does not show a corresponding pulsatile response

This may provide evidence that contradicts the alarm.

However:

> Contradiction does not automatically mean false alarm.

The absence of a response in another signal may result from:

- poor signal quality
- physiological delay
- low peripheral perfusion
- transient physiological events
- modality-specific limitations
- genuine physiological complexity

Therefore CLARIS should distinguish between:

- contradictory physiological evidence
- unreliable evidence
- genuinely missing evidence

---

# 7. Multimodal Signal Quality

Silva, Lee and Mark investigated signal-quality estimation using multiple physiological channels in ICU data.

The study included signals such as:

- ECG
- PPG
- ABP
- respiration
- CVP
- PAP
- other invasive pressure signals

The method used multichannel adaptive filtering and relationships between physiological signals to estimate signal quality.

Human annotations classified signal epochs as:

- Good
- Maybe
- Bad

Reported ROC AUC values included approximately:

- PPG: 0.86
- ABP: 0.82
- ECG: 0.68

The study demonstrated that information from multiple physiological channels can assist in determining whether a signal is reliable.

### Important limitation

The study also highlights an important problem for CLARIS:

> Poor agreement between signals can occur because of genuine physiological changes, not only because of signal corruption.

This prevents a simple rule such as:

> signals disagree → one signal is bad

### Relevance to CLARIS

Signal quality should therefore remain separate from physiological interpretation.

A signal can be:

- high quality and physiologically abnormal
- low quality and partially informative
- consistent with another signal
- inconsistent with another signal because of genuine physiology

This distinction is fundamental to the CLARIS evidence model.

---

# 8. Temporal Reasoning

## 8.1 Alarm as an Event

ICU alarm datasets commonly provide waveform data surrounding an alarm rather than only the exact alarm timestamp.

This allows the system to examine:

- what happened before the alarm
- what happened during the alarm
- what happened immediately after the alarm

Conceptually:

```text
                    ALARM
                      ↓
───────────────|──────|──────|───────────────
               PRE   EVENT   POST
