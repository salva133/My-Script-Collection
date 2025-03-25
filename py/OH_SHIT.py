import os
import shutil
import logging

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Adjust log level as needed

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def oh_shit(target_directory, TEST_MODE=True):
    """
    Deletes all files and subdirectories in the target_directory.
    If TEST_MODE=True, only displays what would be deleted.
    If TEST_MODE=False, performs the actual deletions.
    """
    path = os.path.abspath(target_directory)

    if not os.path.exists(path):
        logger.error(f"ERROR: '{path}' does not exist! Operation aborted.")
        return

    if TEST_MODE:
        logger.info("TEST MODE ACTIVE (only displaying what would be deleted)")
    else:
        logger.warning("LETHAL MODE ACTIVE (entries will be deleted!)")

    for entry in os.listdir(path):
        entry_path = os.path.join(path, entry)

        # Check if it's a directory
        if os.path.isdir(entry_path):
            if TEST_MODE:
                logger.info(f"Would delete directory: {entry_path}")
            else:
                logger.warning(f"Deleting directory: {entry_path}")
                shutil.rmtree(entry_path, ignore_errors=True)
        else:
            # It's a file
            if TEST_MODE:
                logger.info(f"Would delete file: {entry_path}")
            else:
                logger.warning(f"Deleting file: {entry_path}")
                os.remove(entry_path)

    logger.info("Operation finished.")
