""" Classes for interfacing with host hardware. """

import logging
import os
import re

from typing import Optional

_LOGGER = logging.getLogger(__name__)


class HostFactory:
    """ Detect and create interface for corresponding system. """

    @staticmethod
    def get_host_interface():
        """ Return the correct interface for the host system. """
        if HostFactory._is_rpi():
            _LOGGER.debug("Found RPI interface")
            return RPI()

        _LOGGER.debug("No compatible device interface found")

    @staticmethod
    def _is_rpi():
        # Info comes from: https://www.raspberrypi.org/documentation/faqs/
        RPI_IDs = ["BCM2835", "BCM2836", "BCM2837", "BCM2711"]

        try:
            with open("/proc/cpuinfo", "r") as ifh:
                cpuinfo = ifh.read()

            m = re.search(
                r"^Hardware\s+:\s+(\w+)$", cpuinfo, flags=re.MULTILINE | re.IGNORECASE
            )
            return m and m.group(1) in RPI_IDs

        except FileNotFoundError:
            pass

        return False


class RPI:
    """ RPI device interface class. """

    def get_temperature(self, logger):
        from sarge import run, Capture

        logger.info("Running command to get temp")
        p = run("/opt/vc/bin/vcgencmd measure_temp", stdout=Capture())
        o = o.stdout.text

        m = re.search("=(.*).([C,F])")
        if m:
            logger.info("Current temperature %s, %s", m.group(1), m.group(2))
            val = float(m.group(1))
            if m.group(2) == "F":
                val = (val - 32) * (5 / 9)
            return val

        logger.info("Temperature not matched")
