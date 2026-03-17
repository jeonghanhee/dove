import json
import keyring
from datetime import datetime
from typing import TYPE_CHECKING
from .config_loader import APP_ID

class Storable:
    def save(self, name: str = None) -> str:
        key = name or self.__class__.__name__

        payload = {
            "__class__": self.__class__.__name__,
            "__saved_at__": datetime.utcnow().isoformat(),
            "data": self._to_dict(),
        }

        keyring.set_password(APP_ID, key, json.dumps(payload, ensure_ascii=False, default=str))
        return key

    @classmethod
    def load(cls, name: str = None) -> "Storable | None":
        key = name or cls.__name__
        raw = keyring.get_password(APP_ID, key)

        if raw is None:
            return None

        payload = json.loads(raw)
        obj = cls.__new__(cls)
        obj._from_dict(payload["data"])

        saved_at = payload.get("__saved_at__", "Unknown")
        return obj

    @classmethod
    def delete(cls, name: str = None) -> None:
        key = name or cls.__name__
        try:
            keyring.delete_password(APP_ID, key)
        except keyring.errors.PasswordDeleteError:
            print(key)

    @classmethod
    def exists(cls, name: str = None) -> bool:
        key = name or cls.__name__
        return keyring.get_password(APP_ID, key) is not None

    def _to_dict(self) -> dict:
        return self.__dict__

    def _from_dict(self, data: dict) -> None:
        self.__dict__.update(data)