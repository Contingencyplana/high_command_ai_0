from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass(frozen=True)
class FunFlags:
    fun_core: bool = False
    balance_toggles: bool = False
    xp_rate_limit: bool = False
    loot_governor: bool = False

    def as_dict(self) -> Dict[str, bool]:
        return {
            "fun_core": self.fun_core,
            "balance_toggles": self.balance_toggles,
            "xp_rate_limit": self.xp_rate_limit,
            "loot_governor": self.loot_governor,
        }


def _env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return str(raw).strip().lower() not in {"0", "false", "no", "off", ""}


def load_fun_flags(repo_root: Path) -> FunFlags:
    """Load FUN feature flags from exchange/config.json, overridable by env.

    Env overrides (bool-like): FUN_CORE, BALANCE_TOGGLES, XP_RATE_LIMIT, LOOT_GOVERNOR
    """

    cfg_path = repo_root / "exchange" / "config.json"
    base = {
        "fun_core": False,
        "balance_toggles": False,
        "xp_rate_limit": False,
        "loot_governor": False,
    }
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            ff = data.get("fun_flags")
            if isinstance(ff, dict):
                base.update({
                    "fun_core": bool(ff.get("fun_core", base["fun_core"])),
                    "balance_toggles": bool(ff.get("balance_toggles", base["balance_toggles"])),
                    "xp_rate_limit": bool(ff.get("xp_rate_limit", base["xp_rate_limit"])),
                    "loot_governor": bool(ff.get("loot_governor", base["loot_governor"])),
                })
    except Exception:
        # Config optional; default-safe posture
        pass

    # Env overrides
    fun_core = _env_bool("FUN_CORE", base["fun_core"])
    balance_toggles = _env_bool("BALANCE_TOGGLES", base["balance_toggles"])
    xp_rate_limit = _env_bool("XP_RATE_LIMIT", base["xp_rate_limit"])
    loot_governor = _env_bool("LOOT_GOVERNOR", base["loot_governor"])

    return FunFlags(
        fun_core=fun_core,
        balance_toggles=balance_toggles,
        xp_rate_limit=xp_rate_limit,
        loot_governor=loot_governor,
    )

