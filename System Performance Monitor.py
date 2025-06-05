import psutil
import time
import logging
from datetime import datetime

# --- Configuration ---
LOG_FILE = "system_performance.log"
MONITOR_INTERVAL_SECONDS = 5  # Log data every 5 seconds
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# --- Setup Logging ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=DATE_FORMAT,
)
# Add a console handler as well to see live output (optional)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
console_handler.setFormatter(formatter)
logging.getLogger().addHandler(console_handler)


def get_cpu_usage():
    """
    Retrieves the current system-wide CPU utilization percentage.

    Returns:
        float: CPU usage percentage, or None if an error occurs.
    """
    try:
        # interval=1 means it will compare CPU times over a 1-second interval.
        # This is a blocking call for that duration but gives a more accurate reading.
        cpu_percent = psutil.cpu_percent(interval=1)
        return cpu_percent
    except Exception as e:
        logging.error(f"Error getting CPU usage: {e}")
        return None


def get_memory_usage():
    """
    Retrieves the current system memory utilization percentage and used/total memory.

    Returns:
        tuple: (memory_percent, memory_used_mb, memory_total_mb) or (None, None, None) if an error occurs.
    """
    try:
        mem_info = psutil.virtual_memory()
        memory_percent = mem_info.percent
        # Convert bytes to megabytes for readability
        memory_used_mb = round(mem_info.used / (1024 * 1024), 2)
        memory_total_mb = round(mem_info.total / (1024 * 1024), 2)
        return memory_percent, memory_used_mb, memory_total_mb
    except Exception as e:
        logging.error(f"Error getting memory usage: {e}")
        return None, None, None


def log_system_performance():
    """
    Gets CPU and memory usage and logs them.
    """
    cpu_usage = get_cpu_usage()
    memory_percent, memory_used_mb, memory_total_mb = get_memory_usage()

    if cpu_usage is not None and memory_percent is not None:
        log_message = (
            f"CPU Usage: {cpu_usage}% | "
            f"Memory Usage: {memory_percent}% ({memory_used_mb}MB / {memory_total_mb}MB)"
        )
        logging.info(log_message)
    else:
        logging.warning("Could not retrieve complete performance data in this interval.")


def main():
    """
    Main function to start the monitoring loop.
    """
    logging.info(
        f"System Performance Monitor started. Logging to {LOG_FILE} every {MONITOR_INTERVAL_SECONDS} seconds."
    )
    print(
        f"Monitoring system performance... Press Ctrl+C to stop."
    )
    print(f"Logging data to: {LOG_FILE}")

    try:
        while True:
            log_system_performance()
            time.sleep(MONITOR_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        logging.info("System Performance Monitor stopped by user.")
        print("\nMonitoring stopped.")
    except Exception as e:
        logging.critical(f"An unexpected error occurred: {e}", exc_info=True)
        print(f"An unexpected error occurred: {e}")
    finally:
        logging.info("System Performance Monitor finished.")


if __name__ == "__main__":
    main()