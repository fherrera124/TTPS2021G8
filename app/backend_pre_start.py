import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed


import sys

sys.path.append(".")

from app.db.session import SessionLocal, just_created

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        db = SessionLocal()
        # Try to create session to check if DB is awake
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(e)
        raise e


def main() -> bool:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")
    # manera de avisar al script ppal si la db fue creada
    import sys
    if just_created:
        sys.exit(1)
    else:
        sys.exit()
    return just_created


if __name__ == "__main__":
    main()
