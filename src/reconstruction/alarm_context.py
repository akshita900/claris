from pathlib import Path
import json
import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EPISODE_DIR = PROJECT_ROOT / "data" / "episodes"


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def calculate_rr_features(ecg_peaks):
    """
    Calculate RR interval features from detected ECG peaks.

    Heart rate is only reported when at least 5 RR intervals
    are available.
    """

    ecg_peaks = np.asarray(ecg_peaks, dtype=float)

    if len(ecg_peaks) < 2:
        return {
            "rr_count": 0,
            "mean_rr_seconds": None,
            "rr_std_seconds": None,
            "mean_heart_rate_bpm": None,
            "heart_rate_available": False
        }

    rr_intervals = np.diff(ecg_peaks)

    mean_rr = float(np.mean(rr_intervals))
    rr_std = float(np.std(rr_intervals))

    if len(rr_intervals) >= 5:
        heart_rate = float(60.0 / mean_rr)
        heart_rate_available = True
    else:
        heart_rate = None
        heart_rate_available = False

    return {
        "rr_count": int(len(rr_intervals)),
        "mean_rr_seconds": mean_rr,
        "rr_std_seconds": rr_std,
        "mean_heart_rate_bpm": heart_rate,
        "heart_rate_available": heart_rate_available
    }


def match_ecg_to_pleth(ecg_peaks, pleth_peaks):
    """
    Match each ECG peak to the next PLETH peak occurring
    0.10 to 1.00 seconds later.

    This reproduces the temporal matching concept used
    in multimodal_alignment.py.
    """

    ecg_peaks = np.asarray(ecg_peaks, dtype=float)
    pleth_peaks = np.asarray(pleth_peaks, dtype=float)

    matches = []

    for ecg_time in ecg_peaks:

        future_pleth = pleth_peaks[
            pleth_peaks >= ecg_time + 0.10
        ]

        if len(future_pleth) == 0:
            continue

        pleth_time = future_pleth[0]

        delay = pleth_time - ecg_time

        if delay <= 1.00:
            matches.append({
                "ecg_time": float(ecg_time),
                "pleth_time": float(pleth_time),
                "delay_seconds": float(delay)
            })

    return matches


def calculate_window_features(
    ecg_peaks,
    pleth_peaks,
    start_time,
    end_time,
    multimodal_matches
):
    """
    Calculate measurable evidence within one temporal window.
    """

    ecg_window = [
        peak for peak in ecg_peaks
        if start_time <= peak < end_time
    ]

    pleth_window = [
        peak for peak in pleth_peaks
        if start_time <= peak < end_time
    ]

    window_matches = [
        match for match in multimodal_matches
        if start_time <= match["ecg_time"] < end_time
    ]

    ecg_count = len(ecg_window)
    pleth_count = len(pleth_window)
    matched_count = len(window_matches)

    if ecg_count > 0:
        matching_fraction = matched_count / ecg_count
    else:
        matching_fraction = None

    delays = [
        match["delay_seconds"]
        for match in window_matches
    ]

    if delays:
        delay_mean = float(np.mean(delays))
        delay_std = float(np.std(delays))
        delay_min = float(np.min(delays))
        delay_max = float(np.max(delays))
    else:
        delay_mean = None
        delay_std = None
        delay_min = None
        delay_max = None

    rr_features = calculate_rr_features(ecg_window)

    duration = end_time - start_time

    return {
        "start_offset_seconds": start_time,
        "end_offset_seconds": end_time,
        "window_duration_seconds": duration,

        "ecg_peak_count": ecg_count,
        "pleth_pulse_count": pleth_count,

        "ecg_events_per_second": (
            ecg_count / duration
            if duration > 0 else None
        ),

        "pleth_events_per_second": (
            pleth_count / duration
            if duration > 0 else None
        ),

        "matched_event_count": matched_count,
        "matching_fraction": matching_fraction,

        "ecg_pleth_delay_mean_seconds": delay_mean,
        "ecg_pleth_delay_std_seconds": delay_std,
        "ecg_pleth_delay_min_seconds": delay_min,
        "ecg_pleth_delay_max_seconds": delay_max,

        "rr_count": rr_features["rr_count"],
        "mean_rr_seconds": rr_features["mean_rr_seconds"],
        "rr_std_seconds": rr_features["rr_std_seconds"],
        "mean_heart_rate_bpm": rr_features["mean_heart_rate_bpm"],
        "heart_rate_available": rr_features["heart_rate_available"]
    }


def calculate_temporal_changes(windows):

    window_names = list(windows.keys())
    changes = {}

    for first_name, second_name in zip(
        window_names[:-1],
        window_names[1:]
    ):

        first = windows[first_name]
        second = windows[second_name]

        change_name = f"{first_name}_to_{second_name}"

        changes[change_name] = {
            "ecg_peak_count": (
                second["ecg_peak_count"]
                - first["ecg_peak_count"]
            ),

            "pleth_pulse_count": (
                second["pleth_pulse_count"]
                - first["pleth_pulse_count"]
            ),

            "matching_fraction": (
                None
                if (
                    first["matching_fraction"] is None
                    or second["matching_fraction"] is None
                )
                else (
                    second["matching_fraction"]
                    - first["matching_fraction"]
                )
            ),

            "ecg_pleth_delay_mean_seconds": (
                None
                if (
                    first["ecg_pleth_delay_mean_seconds"] is None
                    or second["ecg_pleth_delay_mean_seconds"] is None
                )
                else (
                    second["ecg_pleth_delay_mean_seconds"]
                    - first["ecg_pleth_delay_mean_seconds"]
                )
            ),

            "rr_std_seconds": (
                None
                if (
                    first["rr_std_seconds"] is None
                    or second["rr_std_seconds"] is None
                )
                else (
                    second["rr_std_seconds"]
                    - first["rr_std_seconds"]
                )
            ),

            "mean_heart_rate_bpm": (
                None
                if (
                    first["mean_heart_rate_bpm"] is None
                    or second["mean_heart_rate_bpm"] is None
                )
                else (
                    second["mean_heart_rate_bpm"]
                    - first["mean_heart_rate_bpm"]
                )
            )
        }

    return changes


def build_alarm_context(event_name):

    episode_path = EPISODE_DIR / event_name

    physiological = load_json(
        episode_path / "physiological_features.json"
    )

    ecg_peaks = physiological[
        "II"
    ][
        "features"
    ][
        "peak_times_seconds"
    ]

    pleth_peaks = physiological[
        "PLETH"
    ][
        "features"
    ][
        "peak_times_seconds"
    ]

    # Reconstruct the actual ECG-PLETH temporal matches.
    multimodal_matches = match_ecg_to_pleth(
        ecg_peaks,
        pleth_peaks
    )

    windows_definition = {
        "pre_10_to_5": (-10, -5),
        "pre_5_to_0": (-5, 0),
        "post_0_to_5": (0, 5),
        "post_5_to_10": (5, 10)
    }

    alarm_reference_time = 300.0

    windows = {}

    for window_name, (
        start_offset,
        end_offset
    ) in windows_definition.items():

        start_time = (
            alarm_reference_time
            + start_offset
        )

        end_time = (
            alarm_reference_time
            + end_offset
        )

        windows[window_name] = calculate_window_features(
            ecg_peaks=ecg_peaks,
            pleth_peaks=pleth_peaks,
            start_time=start_time,
            end_time=end_time,
            multimodal_matches=multimodal_matches
        )

        windows[window_name][
            "start_offset_seconds"
        ] = start_offset

        windows[window_name][
            "end_offset_seconds"
        ] = end_offset

    temporal_changes = calculate_temporal_changes(
        windows
    )

    return {
        "event": event_name,
        "alarm_reference_time_seconds":
            alarm_reference_time,
        "windows": windows,
        "temporal_changes": temporal_changes
    }


def save_alarm_context(event_name, context):

    episode_path = EPISODE_DIR / event_name

    output_path = (
        episode_path / "alarm_context.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            context,
            file,
            indent=4
        )

    return output_path


def print_summary(context, output_path):

    print()
    print("=" * 40)
    print("CLARIS - Alarm Temporal Context")
    print("=" * 40)

    print(
        f"Event: {context['event']}"
    )

    print(
        f"Alarm reference: "
        f"{context['alarm_reference_time_seconds']:.3f} s"
    )

    print()

    print("----------------------------------------")
    print("TEMPORAL WINDOWS")
    print("----------------------------------------")

    for window_name, window in context[
        "windows"
    ].items():

        print()
        print(f"  {window_name}")

        print(
            f"    ECG events: "
            f"{window['ecg_peak_count']}"
        )

        print(
            f"    PLETH events: "
            f"{window['pleth_pulse_count']}"
        )

        print(
            f"    Matched events: "
            f"{window['matched_event_count']}"
        )

        print(
            f"    Matching fraction: "
            f"{window['matching_fraction']:.3f}"
        )

        print(
            f"    RR intervals: "
            f"{window['rr_count']}"
        )

        print(
            f"    HR available: "
            f"{window['heart_rate_available']}"
        )

        print(
            f"    Mean HR: "
            f"{window['mean_heart_rate_bpm']}"
        )

    print()

    print("----------------------------------------")
    print("TEMPORAL CHANGES")
    print("----------------------------------------")

    for change_name, change in context[
        "temporal_changes"
    ].items():

        print()
        print(f"  {change_name}")

        print(
            f"    ECG event change: "
            f"{change['ecg_peak_count']}"
        )

        print(
            f"    PLETH event change: "
            f"{change['pleth_pulse_count']}"
        )

        print(
            f"    Matching fraction change: "
            f"{change['matching_fraction']}"
        )

        print(
            f"    Delay change: "
            f"{change['ecg_pleth_delay_mean_seconds']}"
        )

        print(
            f"    RR variability change: "
            f"{change['rr_std_seconds']}"
        )

        print(
            f"    HR change: "
            f"{change['mean_heart_rate_bpm']}"
        )

    print()

    print("----------------------------------------")
    print("Saved to:")
    print(output_path)
    print("----------------------------------------")

    print()
    print("=" * 40)
    print("Alarm temporal context complete.")
    print("=" * 40)


def main():

    event_name = "003c13_0115"

    context = build_alarm_context(
        event_name
    )

    output_path = save_alarm_context(
        event_name,
        context
    )

    print_summary(
        context,
        output_path
    )


if __name__ == "__main__":
    main()