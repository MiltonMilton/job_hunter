from models import Base, engine


def init_db() -> None:
    """Initialize the database tables."""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized")
