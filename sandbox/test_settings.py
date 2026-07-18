from backend.core.config import settings


def main() -> None:
    for field in type(settings).model_fields:
        print(f"{field:22s} = {getattr(settings, field)!r}")
    print(f"{'POSTGRES_DSN':22s} = {settings.POSTGRES_DSN!r}")


if __name__ == "__main__":
    main()