# CLARIS Experiment Log

This document records the practical investigations, observations, decisions, and changes made during the development of CLARIS.

---

## 2026-09-24 — Phase 1: VTaC Dataset Verification

### Objective

Begin Phase 1 by verifying the structure of the selected VTaC dataset and establishing how individual alarm events are represented before developing the larger CLARIS processing pipeline.

The initial investigation focuses on:

- dataset structure
- event labels
- waveform format
- sampling frequency
- alarm timing
- available physiological channels
- annotator-level labels
- initial waveform visualization

The purpose of this stage is dataset and pipeline verification, not model development.

---

## 1. Dataset Access

The selected dataset from Phase 0 is:

**VTaC — Ventricular Tachycardia Alarm Challenge**

**Version:** 1.1  
**Source:** PhysioNet

The complete dataset was not downloaded at this stage.

Only the files required for initial investigation were obtained locally.

---

## 2. Files Obtained

The following files were obtained under:

```text
data/raw/vtac/
---

## 2026-09-24 — Phase 1: 100-Event Channel Inventory

### Objective

Expand the initial single-event investigation to a larger exploratory sample to determine the availability and consistency of physiological modalities in VTaC.

A sample of 100 annotated VTaC events was selected from `event_labels.csv`.

Only waveform header files were retrieved for this investigation. Waveform `.dat` files were not downloaded.

### Waveform Structure

All 100 inspected events had:

- Sampling frequency: **250 Hz**
- Number of samples: **90,000**
- Duration: **360 seconds**

Therefore, the basic temporal structure was consistent across all 100 inspected events.

The number of signals varied:

| Number of signals | Events |
|---:|---:|
| 3 | 3 |
| 4 | 39 |
| 5 | 48 |
| 6 | 10 |
| **Total** | **100** |

### Physiological Modality Availability

| Modality | Events available |
|---|---:|
| ECG | 100/100 |
| PLETH | 97/100 |
| ABP | 40/100 |

The 100-event sample therefore demonstrates that the available physiological modalities are not identical across events.

### ECG Lead Availability

The observed ECG lead availability was:

| ECG lead | Events |
|---|---:|
| II | 100/100 |
| V | 96/100 |
| aVR | 63/100 |
| I | 37/100 |
| III | 28/100 |
| aVL | 0/100 |
| aVF | 0/100 |

Lead II was present in all 100 inspected events, while the other ECG leads varied.

### Combined Modality Availability

| ECG | PLETH | ABP | Events |
|---|---|---|---:|
| Yes | Yes | No | 57 |
| Yes | Yes | Yes | 40 |
| Yes | No | No | 3 |
| **Total** | | | **100** |

No event in this sample contained ABP without PLETH.

### CLARIS Design Implication

The 100-event inventory indicates that CLARIS should not assume a fixed waveform configuration for every alarm episode.

Instead, the pipeline should first identify which physiological modalities are available for each event.

Missing ABP should therefore be treated as **missing evidence**, rather than automatically treating the event as unusable.

Similarly, the ECG processing stage should accommodate variation in available ECG leads rather than assuming an identical lead configuration across all events.

The signal-quality stage will subsequently determine whether an available signal is sufficiently reliable to contribute physiological evidence.

### Scope of This Finding

These results describe an exploratory sample of **100 VTaC events**.

They are not yet treated as dataset-wide modality statistics.

A larger-scale inventory may be performed later if required before finalizing the CLARIS data-processing pipeline.
## 2026-09-27 — Phase 1: Episode Representation and Initial Signal-Quality Features

### Objective
Implement the first CLARIS alarm episode representation using a locally available VTaC waveform record and establish a reusable signal-integrity feature extraction pipeline.

### Episode used
- Record: `003c13`
- Event: `003c13_0115`
- VTaC reference decision: `False`
- Sampling frequency: 250 Hz
- Duration: 360 seconds
- Samples: 90,000
- Alarm sample: 75,000
- Alarm-centered time range: -300 to +59.996 seconds
- Signals: II, aVR, V, PLETH

### Episode representation
Implemented `CLARISEpisode` in `src/episode.py`.

The representation currently stores:
- record and event identity
- sampling frequency
- number of samples
- duration
- alarm sample
- signal names
- waveform values
- alarm-centered time axis
- signal units
- VTaC reference decision

The alarm-centered time axis was verified:
- Start: -300.0 s
- Alarm: 0.0 s
- End: 59.996 s

### Initial signal-integrity features

Implemented `calculate_signal_quality_features()` in `src/signal_quality.py`.

The current feature set includes:
- NaN count
- Inf count
- exact repeated-sample fraction
- longest repeated-sample run
- longest repeated-run duration
- local mean around the alarm
- local standard deviation around the alarm
- local range around the alarm
- minimum-value count
- maximum-value count

A 1-second window before and after the alarm was used for the initial local features.

### Findings for the first episode

All four available signals contained:
- 0 NaN samples
- 0 infinite samples

The signal-specific measurements were generated for:
- II
- aVR
- V
- PLETH

The PLETH signal showed substantially more repeated adjacent samples than the ECG signals. This was recorded as an observed property rather than interpreted as evidence of poor signal quality.

### Interpretation boundary

No signal was classified as reliable, unreliable, supporting, or contradicting based on these initial measurements.

These measurements establish a reusable feature-extraction layer. Quality thresholds and evidence interpretation will be developed and evaluated across multiple episodes rather than inferred from a single event.

### Output

Generated locally:

`outputs/003c13_0115_signal_quality.csv`

The `outputs/` directory remains ignored by Git except for `.gitkeep`.

## 2026-09-27 — Phase 1: Batch Episode Loading and Signal-Quality Integration

### Objective

Extend the Phase 1 episode pipeline from a single manually constructed VTaC episode to a reusable batch-loading workflow.

The batch workflow should:

1. Read VTaC event metadata from `event_labels.csv`.
2. Identify waveform records that are available locally.
3. Construct `CLARISEpisode` objects using the reusable episode loader.
4. Track unavailable waveform records explicitly.
5. Apply the existing signal-integrity feature calculation to each available signal.

### Batch Episode Loading

A reusable function, `load_available_claris_episodes()`, was added to `src/episode.py`.

The function accepts:

- the VTaC event table
- the local VTaC raw-data directory

It returns:

- successfully loaded `CLARISEpisode` objects
- a list of event IDs whose waveform files are not locally available

The full VTaC event table contains 5,037 annotated events. At this stage, only one waveform event (`003c13_0115`) is locally available.

The batch loader therefore successfully loaded:

- 1 waveform episode

and identified:

- 5,036 events without locally available waveform files.

This is expected because the full VTaC waveform archive has not been downloaded.

### Episode Structure Validation

Automated structural checks were applied to the loaded episode.

The checks verified that:

- waveform sample count matches `n_samples`
- waveform channel count matches the signal list
- time-axis length matches `n_samples`
- alarm sample corresponds to `t = 0`
- duration matches `n_samples / sampling_frequency`

All checks passed for the locally available episode.

### Signal-Quality Feature Integration

The existing `calculate_signal_quality_features()` function from `src/signal_quality.py` was applied to every signal in the loaded episode.

The current episode contains:

- II
- aVR
- V
- PLETH

The calculated features include:

- NaN count
- Inf count
- repeated-sample fraction
- longest repeated run
- longest repeated duration
- local mean around the alarm
- local standard deviation around the alarm
- local range around the alarm
- minimum-value count
- maximum-value count

These outputs remain descriptive signal-integrity measurements. They do not constitute a clinical signal-quality classification or an alarm credibility decision.

### Interpretation Boundary

At this stage, CLARIS can:

- represent an alarm-centered physiological episode
- preserve available multimodal waveform data
- distinguish locally available from unavailable waveform records
- calculate basic signal-integrity features

CLARIS does not yet assign:

- signal quality labels
- physiological evidence labels
- alarm credibility
- SUPPORTS / CONTRADICTS / INSUFFICIENT decisions

Those components remain part of later phases.

### Current Status

The Phase 1 ingestion pathway is now validated for the locally available VTaC waveform.

Next work will focus on systematic batch validation and preprocessing across a larger set of locally available waveform records.
### Alarm-Window Visualization

A synchronized ±5-second visualization was generated for the locally available VTaC episode `003c13_0115`.

The visualization displayed all available signals on a shared alarm-centered time axis:

- ECG II
- ECG aVR
- ECG V
- PLETH

The alarm onset was represented at `t = 0`.

The visualization confirms that the episode representation preserves synchronized multimodal waveform context while retaining the individual signal scales and units.

No clinical alarm-credibility conclusion was made from visual inspection. The visualization is being used for data inspection and pipeline validation only.
### Conservative Preprocessing Contract

A first preprocessing validation layer was implemented in `src/preprocessing.py`.

The current preprocessing layer performs structural validation without modifying the waveform.

Validation checks include:

- waveform is represented as a 2D samples × signals array
- waveform sample count matches the episode metadata
- sampling frequency is greater than zero
- waveform values are finite
- NaN and Inf counts are reported

The validation function returns measurable properties and does not assign a clinical signal-quality label.

No filtering, normalization, resampling, artifact removal, or waveform modification is currently performed.

This conservative approach preserves the original VTaC waveform as the primary physiological evidence while allowing derived processing to be introduced later when justified by the requirements of physiological evidence extraction.
### Batch Episode Validation

The structural validation layer was applied to all CLARIS episodes currently available locally.

For each loaded episode, the validation records:

- record and event identity
- final VTaC decision
- sample count
- signal count
- sampling frequency
- waveform shape validity
- finite-value status
- NaN count
- Inf count

The resulting validation table was saved locally as:

`outputs/batch_episode_validation.csv`

At the current development stage, the local waveform collection contains one VTaC event, so the validation table currently contains one episode.

The generated CSV is treated as a derived local output and is excluded from version control.

### Phase 1 Ingestion Status

The current Phase 1 ingestion pipeline has been tested through:

VTaC event metadata → local waveform availability check → CLARIS episode construction → structural validation → signal-integrity feature calculation.

The pipeline preserves the original waveform and does not currently perform destructive preprocessing.