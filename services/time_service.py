import os
import json
from datetime import datetime, timezone, timedelta
from typing import Optional

STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "_server_time_offset.json")

class TimeService:
    def __init__(self):
        self._offset_seconds: float = 0.0
        self._load_state()

    def _load_state(self):
        try:
            if os.path.exists(STATE_FILE):
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._offset_seconds = float(data.get("offset_seconds", 0.0))
        except Exception as e:
            print(f"[TimeService] Warning loading state: {e}")
            self._offset_seconds = 0.0

    def _save_state(self):
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump({
                    "offset_seconds": self._offset_seconds,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                    "game_time_preview": self.get_game_time().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"[TimeService] Warning saving state: {e}")

    def get_real_utc(self) -> datetime:
        return datetime.now(timezone.utc)

    def get_game_time(self) -> datetime:
        return self.get_real_utc() + timedelta(seconds=self._offset_seconds)

    def get_offset_seconds(self) -> float:
        return self._offset_seconds

    def is_shifted(self) -> bool:
        return abs(self._offset_seconds) > 0.001

    def set_offset_seconds(self, offset_seconds: float) -> datetime:
        self._offset_seconds = float(offset_seconds)
        self._save_state()
        return self.get_game_time()

    def shift_by(self, days: float = 0.0, hours: float = 0.0, minutes: float = 0.0, seconds: float = 0.0) -> datetime:
        delta = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        self._offset_seconds += delta.total_seconds()
        self._save_state()
        return self.get_game_time()

    def set_target_time(self, target_iso_or_dt) -> datetime:
        if isinstance(target_iso_or_dt, str):
            # Parse ISO 8601 string
            clean_str = target_iso_or_dt.replace("Z", "+00:00")
            target_dt = datetime.fromisoformat(clean_str)
        else:
            target_dt = target_iso_or_dt

        if target_dt.tzinfo is None:
            target_dt = target_dt.replace(tzinfo=timezone.utc)
        else:
            target_dt = target_dt.astimezone(timezone.utc)

        real_utc = self.get_real_utc()
        self._offset_seconds = (target_dt - real_utc).total_seconds()
        self._save_state()
        return self.get_game_time()

    def reset(self) -> datetime:
        self._offset_seconds = 0.0
        self._save_state()
        return self.get_game_time()

    def get_status_dict(self) -> dict:
        real_utc = self.get_real_utc()
        game_time = self.get_game_time()
        return {
            "status": "ok",
            "real_utc": real_utc.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "game_time": game_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "offset_seconds": self._offset_seconds,
            "is_shifted": self.is_shifted()
        }

# Global singleton instance
time_service = TimeService()
