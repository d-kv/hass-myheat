"""Sensor platform for MyHeat."""

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

import logging

from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON
from .const import SENSOR
from .entity import MhEntity

from homeassistant.const import UnitOfPressure

_logger = logging.getLogger(__package__)


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        [
            MhSensor(coordinator, entry, heater)
            for heater in coordinator.data.get("data", {}).get("heaters", [])
        ]
    )


class MhSensor(MhEntity, SensorEntity):
    _attr_device_class = SensorDeviceClass.PRESSURE
    _attr_unit_of_measurement = UnitOfPressure.BAR

    def __init__(self, coordinator, config_entry, heater):
        super().__init__(coordinator, config_entry)
        self.heater = heater
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}_pressure"

    async def async_update(self) -> None:
        """Update the state of the sensor."""
        heaters = self.coordinator.data.get("data", {}).get("heaters", [])
        _logger.info(f"Updating pressure sensor entries: {heaters}")
        for heater in heaters:
            if heater["id"] == self.heater["id"]:
                self.native_value = heater["pressure"]
