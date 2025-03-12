import os
import shutil
import logging
from datetime import datetime


def setup_logging(verbose):
    """Configure logging with both file and console handlers"""
    log_format = "%(asctime)s [%(levelname)s] %(message)s"

    # Clear existing loggers
    logging.root.handlers = []

    # Create handlers
    file_handler = logging.FileHandler("file_organizer.log")
    console_handler = logging.StreamHandler()

    # Set logging levels
    file_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Create formatter and add to handlers
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])

    logging.info("File organizer started")
    logging.debug(f"Verbose mode {'enabled' if verbose else 'disabled'}")


def organize_files(path, verbose=False):
    """
    Organizes files in the specified directory into categorized folders.

    Args:
        path (str): The directory path to organize.
        verbose (bool): If True, shows detailed logs of file movements.
    """
    categories = {
        "Images": ["jpg", "jpeg", "png", "gif"],
        "Documents": ["pdf", "doc", "docx", "txt", "csv", "xlsx", "pptx"],
        "Archives": ["zip", "rar", "7z", "tar", "gz"],
        "Videos": ["mp4", "avi", "mkv", "mov", "wmv"],
        "Audio": ["mp3", "wav"],
        "Programs": ["exe", "msi", "bat"],
        "Code": ["py", "ipynb"],
    }

    try:
        if not os.path.isdir(path):
            logging.critical(f"Invalid directory: {path}")
            raise NotADirectoryError(f"Invalid Directory: {path}")

        logging.info(f"Starting organization of: {path}")
        total_files = 0
        moved_files = 0

        for item in os.listdir(path):
            item_path = os.path.join(path, item)

            if os.path.isfile(item_path):
                total_files += 1
                try:
                    ext = os.path.splitext(item)[1][1:].lower()
                    folder_name = "Others"

                    for category, exts in categories.items():
                        if ext in exts:
                            folder_name = category
                            break

                    dest_folder = os.path.join(path, folder_name)
                    if not os.path.exists(dest_folder):
                        logging.info(f"Creating directory: {dest_folder}")
                        os.makedirs(dest_folder, exist_ok=True)

                    dest_path = os.path.join(dest_folder, item)
                    shutil.move(item_path, dest_path)
                    moved_files += 1
                    logging.debug(f"Moved: {item} -> {folder_name}")

                except PermissionError as pe:
                    logging.error(f"Permission denied: {item} ({str(pe)})")
                except shutil.Error as se:
                    logging.warning(f"File already exists: {item} ({str(se)})")
                except Exception as e:
                    logging.error(f"Unexpected error with {item}: {str(e)}")

        logging.info(
            f"Organization complete. Processed {moved_files}/{total_files} files"
        )
        if total_files > moved_files:
            logging.warning(f"{total_files - moved_files} files could not be processed")

    except Exception as e:
        logging.critical(f"Fatal error during organization: {str(e)}")
        raise


def main():
    """Main entry point with error handling"""
    try:
        print("=== Windows File Organizer ===")
        path = input("Enter path to organize: ").strip()
        verbose = input("Show details? (y/n): ").lower() == "y"

        setup_logging(verbose)

        if not os.path.exists(path):
            logging.error("Path does not exist")
            print("Error: The specified path does not exist")
            return

        organize_files(path, verbose)
        print("Organization completed successfully. Check log file for details.")

    except KeyboardInterrupt:
        logging.warning("Operation cancelled by user")
        print("\nOperation cancelled by user!")
    except Exception as e:
        logging.critical(f"Critical failure: {str(e)}")
        print("A critical error occurred. See log file for details.")


if __name__ == "__main__":
    main()
