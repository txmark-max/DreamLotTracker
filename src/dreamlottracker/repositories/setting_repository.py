from dreamlottracker.database.models import Setting
from dreamlottracker.database.session import SessionLocal


class SettingRepository:
    def get_all(self) -> dict[str, str]:
        with SessionLocal() as session:
            settings = session.query(Setting).all()
            return {setting.key: setting.value for setting in settings}

    def get(self, key: str, default: str = "") -> str:
        with SessionLocal() as session:
            setting = session.query(Setting).filter(Setting.key == key).first()

            if not setting:
                return default

            return setting.value

    def set(self, key: str, value: str, description: str | None = None) -> None:
        with SessionLocal() as session:
            setting = session.query(Setting).filter(Setting.key == key).first()

            if setting:
                setting.value = value

                if description is not None:
                    setting.description = description
            else:
                setting = Setting(
                    key=key,
                    value=value,
                    description=description,
                )
                session.add(setting)

            session.commit()

    def ensure_defaults(self, defaults: dict[str, tuple[str, str]]) -> None:
        with SessionLocal() as session:
            for key, (value, description) in defaults.items():
                existing = session.query(Setting).filter(Setting.key == key).first()

                if not existing:
                    session.add(
                        Setting(
                            key=key,
                            value=value,
                            description=description,
                        )
                    )

            session.commit()
