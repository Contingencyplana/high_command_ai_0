"""Generate the Level-0 noun tone palette for the audio motif experiment.

The script synthesizes simple sine-wave stems (WAV) for each noun from the
emoji language, writes them to `audio/motifs/nouns/`, and produces an index
file containing metadata required by the composer prototype. Running this
script is an easy way to seed realistic assets before higher-fidelity
recordings are produced.
"""

from __future__ import annotations

import json
import math
import struct
import wave
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable

SAMPLE_RATE = 44_100
DURATION_SECONDS = 0.5  # One beat at 120 BPM
AMPLITUDE = 0.45  # Scaled 0..1 (to avoid clipping)


@dataclass(frozen=True)
class ToneDefinition:
    emoji: str
    name: str
    note: str
    frequency_hz: float
    instrument: str
    duration_seconds: float = DURATION_SECONDS


TONE_DEFINITIONS: Iterable[ToneDefinition] = (
    ToneDefinition("🛠️", "forge", "C4", 261.63, "warm-marimba"),
    ToneDefinition("🌾", "field", "D4", 293.66, "warm-marimba"),
    ToneDefinition("🌌", "dream", "E4", 329.63, "celesta-pad"),
    ToneDefinition("🌊", "river", "F4", 349.23, "glass-harmonics"),
    ToneDefinition("🧱", "wall", "G4", 392.00, "low-brass-mute"),
    ToneDefinition("🔥", "ember", "A4", 440.00, "choir-aah"),
    ToneDefinition("🌱", "seed", "B4", 493.88, "plucked-harp"),
    ToneDefinition("🤖", "ally", "C5", 523.25, "synth-bell"),
)


def _find_repo_root(start: Path) -> Path:
    for parent in [start] + list(start.parents):
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Unable to locate repository root (missing .git directory)")


def _synthesize_tone(frequency_hz: float, duration_seconds: float) -> bytes:
    frame_count = int(SAMPLE_RATE * duration_seconds)
    frames = bytearray()
    for index in range(frame_count):
        time = index / SAMPLE_RATE
        sample = math.sin(2 * math.pi * frequency_hz * time)
        value = int(sample * AMPLITUDE * 32767)
        frames.extend(struct.pack("<h", value))
    return bytes(frames)


def _write_wav(path: Path, frames: bytes) -> None:
    with wave.open(str(path), "w") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)  # 16-bit samples
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(frames)


def _build_index(definitions: Iterable[ToneDefinition], relative_dir: Path) -> Dict[str, Dict[str, object]]:
    index: Dict[str, Dict[str, object]] = {}
    for definition in definitions:
        filename = f"{definition.name}.wav"
        index[definition.name] = {
            "emoji": definition.emoji,
            "note": definition.note,
            "frequency_hz": definition.frequency_hz,
            "instrument": definition.instrument,
            "duration_seconds": definition.duration_seconds,
            "file": str(relative_dir / filename),
        }
    return index


def main() -> None:
    script_path = Path(__file__).resolve()
    repo_root = _find_repo_root(script_path.parent)

    output_dir = repo_root / "audio" / "motifs" / "nouns"
    output_dir.mkdir(parents=True, exist_ok=True)

    for definition in TONE_DEFINITIONS:
        wav_path = output_dir / f"{definition.name}.wav"
        frames = _synthesize_tone(definition.frequency_hz, definition.duration_seconds)
        _write_wav(wav_path, frames)

    index = _build_index(TONE_DEFINITIONS, Path("audio/motifs/nouns"))
    index_path = output_dir / "index.json"
    with index_path.open("w", encoding="utf-8") as handle:
        json.dump(
            {
                "schema": "emoji-level-0-tone-index@1.0",
                "sample_rate": SAMPLE_RATE,
                "amplitude": AMPLITUDE,
                "tones": index,
            },
            handle,
            ensure_ascii=False,
            indent=2,
        )
        handle.write("\n")

    print(f"Generated noun tone palette in {output_dir}")


if __name__ == "__main__":
    main()
