from stem.control import Controller
import socks
import socket
import logging

def renew_tor_ip(tor_control_port=9051):
    """Renews the Tor IP address.

    Args:
        tor_control_port (int): The control port for the Tor service (default: 9051).
    """
    try:
        with Controller.from_port(port=tor_control_port) as controller:
            controller.authenticate()
            if controller.is_authenticated():
                controller.signal("NEWNYM")
                logging.info("Successfully renewed Tor IP address.")
            else:
                logging.error("Authentication with Tor controller failed.")
    except Exception as e:
        logging.error(f"Error renewing Tor IP: {e}")

def use_tor(tor_port=9050, tor_host="127.0.0.1"):
    """Sets up the socket to use Tor.

    Args:
        tor_port (int): The SOCKS port for the Tor service (default: 9050).
        tor_host (str): The host address for the Tor service (default: 127.0.0.1).
    """
    socks.set_default_proxy(socks.SOCKS5, tor_host, tor_port)
    socket.socket = socks.socksocket
    logging.info(f"Using Tor on {tor_host}:{tor_port} for requests.")
