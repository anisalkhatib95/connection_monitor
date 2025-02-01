import logging
import schedule
import time
import os

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[
                        logging.FileHandler("connection_monitor.log",
                                            mode="a",
                                            encoding="utf-8",
                                            delay=False),
                        logging.StreamHandler()
                    ]
                    )

file_handler = logging.FileHandler("connection_monitor.log",
                                   mode='a',
                                   encoding="utf-8")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
file_handler.terminator = "\n"
file_handler.flush = lambda: file_handler.stream.flush()
logging.getLogger().addHandler(file_handler)

servers_ips = {
    # Examples:
    # "Shaalan Internal ATM": "192.168.1.1",
    # "Aleppo Branch": "192.168.1.2"
    "Google DNS Server": "8.8.8.8"  # test
}


def ping_ip(ip_address):
    # linux
    # response = os.system(f"ping -c 1 {ip_address} > /dev/null 2>&1")
    # windows
    response = os.system(f"ping -n 1 {ip_address} > nul 2>&1")
    return response == 0


def check_connection():
    logging.debug("Running connection check...")

    for server_name, ip_address in servers_ips.items():
        if not ping_ip(ip_address):
            error_message = (
                f"ERROR: {server_name} ({ip_address}) is unreachable.")
            logging.error(error_message)
            prepare_sms_alert(error_message)
        else:
            logging.info(f"{server_name} ({ip_address}) Connection OK.")

        # Flush the logs after each message
        for handler in logging.getLogger().handlers:
            handler.flush()


def prepare_sms_alert(message):
    # I don't know how to send the SMS
    logging.info(f"Prepared SMS alert: {message}")


schedule.every(5).seconds.do(check_connection)

if __name__ == "__main__":
    logging.info("Connection Monitoring Service started")

    while True:
        logging.debug("Running service...")
        schedule.run_pending()
        time.sleep(1)
