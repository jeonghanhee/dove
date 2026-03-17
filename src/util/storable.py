import json
import keyring
from datetime import datetime
from src.config_loader import APP_ID

class Storable:
    def save(self, name: str = None) -> str:
        """Saves the current instance's state to keyring."""
        key = name or self.__class__.__name__

        payload = {
            "__class__": self.__class__.__name__,
            "__saved_at__": datetime.utcnow().isoformat(),
            "data": self._to_dict(),
        }

        keyring.set_password(APP_ID, key, json.dumps(payload, ensure_ascii=False, default=str))
        return key

    @classmethod
    def overwrite(cls, data: dict, name: str = None) -> str:
        key = name or cls.__name__
        
        payload = {
            "__class__": cls.__name__,
            "__saved_at__": datetime.utcnow().isoformat(),
            "data": data,
        }
        
        keyring.set_password(APP_ID, key, json.dumps(payload, ensure_ascii=False, default=str))
        return key

    def update_attributes(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    @classmethod
    def load(cls, name: str = None) -> "Storable | None":
        key = name or cls.__name__
        raw = keyring.get_password(APP_ID, key)

        if raw is None:
            return None

        try:
            payload = json.loads(raw)
            obj = cls.__new__(cls)
            obj._from_dict(payload["data"])
            return obj
        except Exception as e:
            print(f"Failed to load {key}: {e}")
            return None

    @classmethod
    def delete(cls, name: str = None) -> None:
        key = name or cls.__name__
        try:
            keyring.delete_password(APP_ID, key)
        except keyring.errors.PasswordDeleteError:
            pass

    @classmethod
    def exists(cls, name: str = None) -> bool:
        key = name or cls.__name__
        return keyring.get_password(APP_ID, key) is not None

    def _to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def _from_dict(self, data: dict) -> None:
        self.__dict__.update(data)