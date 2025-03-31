# --- START OF MODIFIED watcher.py ---

import time
import os
import sys
import subprocess
import logging
import shutil  # For moving and copying files
from pathlib import Path # For easier path manipulation (especially home dir)
import psutil  # For process management
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
# No need for datetime, time.strftime is sufficient

# --- Configuration ---
# Directory to watch for the incoming code.py file
# Uses pathlib to reliably find the user's Downloads folder
DOWNLOADS_FOLDER = Path.home() / "Downloads"

# Directory where the game runs and where the main script should end up
# Set to "." if the watcher runs from the game's parent directory,
# otherwise use an absolute path like "/path/to/your/game/folder"
GAME_FOLDER = Path(".") # Or use Path("/path/to/your/game/folder")

TARGET_FILENAME = "code.py"
NEW_FILENAME = "main.py" # <--- CHANGED from "stickkick.py"
HISTORY_FOLDER_NAME = "history" # Name of the backup directory within GAME_FOLDER

# How to identify the game process to terminate (should match NEW_FILENAME)
GAME_SCRIPT_FILENAME = "main.py" # <--- CHANGED from "stickkick.py"

# Setup basic logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# --- Functions ---

def find_and_terminate_game_process(script_name_to_find):
    """Finds and terminates Python processes running the specified script."""
    terminated_count = 0
    # Ensure we're comparing against absolute paths if possible
    try:
        # Try to resolve the game script path relative to the GAME_FOLDER
        game_script_path = GAME_FOLDER.resolve() / script_name_to_find
    except OSError:
         # Fallback if GAME_FOLDER is invalid somehow
         game_script_path = Path(script_name_to_find) # Use relative path as fallback

    logging.info(f"Searching for processes running a script like: '{script_name_to_find}' or '{game_script_path}'")

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            p_info = proc.info
            if not p_info['cmdline']: # Skip processes with empty cmdline
                 continue

            # Check if it's a python process
            is_python_proc = ('python' in p_info.get('name','').lower() or
                              (sys.executable and p_info.get('exe','') and Path(p_info['exe']) == Path(sys.executable)))

            if is_python_proc:
                 # Check if the target script name or full path is in the command line arguments
                 cmdline_str = ' '.join(p_info['cmdline'])
                 script_found_in_cmd = False
                 for arg in p_info['cmdline'][1:]: # Skip the python executable itself
                      # Simple check first
                      if script_name_to_find in arg:
                          try:
                              arg_path = Path(arg)
                              if arg_path.name == script_name_to_find:
                                   try:
                                       if arg_path.resolve() == game_script_path:
                                           script_found_in_cmd = True
                                           break
                                   except: # Handle resolve errors
                                       if arg_path.name == script_name_to_find:
                                            script_found_in_cmd = True
                                            break
                          except: # Handle errors creating Path object from arg
                               if script_name_to_find in arg: # Basic string check as last resort
                                    script_found_in_cmd = True
                                    break

                 if script_found_in_cmd:
                    logging.info(f"Found game process: PID={proc.pid}, CmdLine='{cmdline_str}'")
                    try:
                        p = psutil.Process(proc.pid)
                        p.terminate() # Send SIGTERM (graceful shutdown)
                        logging.info(f"Sent terminate signal to PID {proc.pid}.")
                        try:
                            p.wait(timeout=3)
                            logging.info(f"Process PID {proc.pid} terminated gracefully.")
                        except psutil.TimeoutExpired:
                            logging.warning(f"Process PID {proc.pid} did not terminate gracefully after 3s. Forcing kill.")
                            p.kill()
                            p.wait()
                            logging.info(f"Process PID {proc.pid} killed.")
                        terminated_count += 1
                    except psutil.NoSuchProcess:
                        logging.warning(f"Process PID {proc.pid} already exited.")
                    except psutil.AccessDenied:
                        logging.error(f"Permission denied to terminate PID {proc.pid}. Try running watcher as administrator/root?")
                    except Exception as e:
                        logging.error(f"Error terminating PID {proc.pid}: {e}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass # Ignore processes that disappeared or we can't access
        except Exception as e:
            if 'cmdline' not in str(e):
                logging.error(f"Error inspecting process {proc.pid if proc else 'N/A'}: {e}")


    if terminated_count == 0:
        logging.warning(f"No running game process found matching script '{script_name_to_find}'.")
    return terminated_count > 0

def run_new_script(script_path, working_directory):
    """Runs the specified Python script."""
    try:
        script_path_str = str(script_path)
        working_dir_str = str(working_directory)

        if not script_path.exists():
             logging.error(f"Error: Script to run '{script_path_str}' does not exist.")
             return False

        logging.info(f"Attempting to run '{script_path_str}' in '{working_dir_str}'...")
        process = subprocess.Popen([sys.executable, script_path_str], cwd=working_dir_str)
        logging.info(f"Started '{script_path.name}' with PID {process.pid}.")
        return True
    except Exception as e:
        logging.error(f"Error running '{script_path.name}': {e}")
        return False

class CodeFileHandler(FileSystemEventHandler):
    """Handles file system events in the Downloads folder."""
    def __init__(self, target_filename, new_filename, game_folder, game_script, history_folder_name):
        self.target_filename = target_filename
        self.new_filename = new_filename # Will now be "main.py"
        self.game_folder = game_folder
        self.game_script = game_script # Will now be "main.py"
        self.history_folder = game_folder / history_folder_name
        self.final_script_path = self.game_folder / self.new_filename # Path to main.py
        self.last_processed_time = 0
        self.debounce_seconds = 3


    def on_created(self, event):
        """Called when a file or directory is created."""
        if event.is_directory:
            return

        current_time = time.time()
        if current_time - self.last_processed_time < self.debounce_seconds:
            return

        source_filepath = Path(event.src_path)
        filename = source_filepath.name

        if filename == self.target_filename: # Still watch for "code.py"
            logging.info(f"Detected target file: {source_filepath}")

            # --- Stability Check ---
            try:
                time.sleep(0.5)
                if not source_filepath.exists() or source_filepath.stat().st_size == 0:
                    if not source_filepath.exists():
                         logging.warning(f"'{filename}' disappeared before processing. Ignoring.")
                         return
                    else:
                         logging.warning(f"'{filename}' is empty, proceeding anyway.")

            except FileNotFoundError:
                 logging.warning(f"'{filename}' disappeared immediately after detection. Ignoring.")
                 return
            except Exception as e:
                 logging.error(f"Error checking file stability for {source_filepath}: {e}")
                 return

            # --- Define Paths ---
            final_dest_path = self.final_script_path # e.g., ./main.py

            # --- Backup, Move, Rename Logic ---
            try:
                self.game_folder.mkdir(parents=True, exist_ok=True)

                # --- Backup Step ---
                if final_dest_path.exists(): # Check if main.py exists
                    try:
                        self.history_folder.mkdir(parents=True, exist_ok=True)
                        timestamp_str = time.strftime("%Y-%m-%d %H-%M-%S")
                        # Backup filename will now be like "YYYY-MM-DD HH-MM-SS main.py"
                        backup_filename = f"{timestamp_str} {self.new_filename}"
                        backup_dest_path = self.history_folder / backup_filename

                        logging.info(f"Backing up existing '{final_dest_path.name}' to '{backup_dest_path}'")
                        shutil.copy2(str(final_dest_path), str(backup_dest_path))

                    except Exception as backup_error:
                        logging.error(f"Failed to backup '{final_dest_path.name}': {backup_error}")
                # --- End Backup Step ---


                # --- Move and Overwrite Step ---
                # Move code.py directly to main.py, overwriting
                logging.info(f"Moving '{source_filepath}' to '{final_dest_path}' (overwriting if exists)")
                shutil.move(str(source_filepath), str(final_dest_path))


                # --- Process Termination and Execution ---
                # 3. Terminate the old game (looking for main.py process)
                logging.info("Attempting to terminate the current game process...")
                terminated = find_and_terminate_game_process(self.game_script) # game_script is "main.py"
                if terminated:
                    time.sleep(1.5)
                else:
                    time.sleep(0.5)

                # 4. Run the new script (main.py)
                logging.info("Attempting to run the new script...")
                if run_new_script(final_dest_path, self.game_folder):
                    self.last_processed_time = time.time()
                else:
                    logging.error("Failed to start the new script.")


            except FileNotFoundError:
                 logging.error(f"Error: '{source_filepath.name}' was moved or deleted before processing.")
            except PermissionError as e:
                 logging.error(f"Permission error during file operations: {e}. Check permissions for Downloads, Game, and History folders.")
            except Exception as e:
                 logging.error(f"An error occurred during backup/move/run: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    # Resolve absolute paths
    watch_path = DOWNLOADS_FOLDER.resolve()
    game_path = GAME_FOLDER.resolve()
    history_path = game_path / HISTORY_FOLDER_NAME

    logging.info(f"Starting watcher for folder: {watch_path}")
    logging.info(f"Game folder set to: {game_path}")
    logging.info(f"Backup history folder set to: {history_path}")
    logging.info(f"Watching for file: '{TARGET_FILENAME}'") # Still watching for code.py
    logging.info(f"Will move to game folder as: '{NEW_FILENAME}'") # Now logs main.py
    logging.info(f"Existing '{NEW_FILENAME}' will be backed up before replacement.") # Now logs main.py
    logging.info(f"Will terminate processes running script like: '{GAME_SCRIPT_FILENAME}'") # Now logs main.py

    # Validate paths
    if not watch_path.is_dir():
        logging.error(f"Error: Watch folder does not exist or is not a directory: {watch_path}")
        sys.exit(1)

    # --- Initial run attempt ---
    initial_script_path = game_path / NEW_FILENAME # Path to main.py
    logging.info("-" * 20)
    if initial_script_path.exists():
        logging.info(f"Attempting initial run of '{initial_script_path.name}'...") # Logs main.py
        run_new_script(initial_script_path, game_path)
        time.sleep(1.0)
    else:
        logging.warning(f"Initial script '{initial_script_path.name}' not found in game folder. Skipping initial run.") # Logs main.py
    logging.info("-" * 20)

    event_handler = CodeFileHandler(
        target_filename=TARGET_FILENAME,
        new_filename=NEW_FILENAME, # Pass "main.py"
        game_folder=game_path,
        game_script=GAME_SCRIPT_FILENAME, # Pass "main.py"
        history_folder_name=HISTORY_FOLDER_NAME
    )
    observer = Observer()
    observer.schedule(event_handler, str(watch_path), recursive=False)

    observer.start()
    logging.info("Watcher started. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping watcher...")
        observer.stop()
    except Exception as e:
        logging.error(f"An unexpected error occurred in the main loop: {e}")
        observer.stop()

    observer.join()
    logging.info("Watcher stopped.")

# --- END OF MODIFIED watcher.py ---