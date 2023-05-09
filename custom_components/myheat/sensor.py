"""Sensor platform for MyHeat."""

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.core import HomeAssistant, callback

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
        self.heater_id = heater["id"]
        _logger.info(f"Setup up pressure sensor for heater id {self.heater_id}")

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}_pressure"

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{super().unique_id}_heater_{self.heater_id}"

    async def async_update(self) -> None:
        """Update the state of the sensor."""
        self._update_heater_pressure()

    @callback
    def _handle_coordinator_update(self):
        """Get the latest state from the thermostat."""

        self._update_heater_pressure()

        self.async_write_ha_state()

    def _update_heater_pressure(self):
        heater = self._heater()
        if heater is None:
            _logger.error(f"Heater with id {self.heater_id} is missing")
            return
        _logger.info(f"Updating pressure sensor entries: {heater}")
        self._attr_native_value = heater["pressure"]

    def _heater(self) -> dict | None:
        heaters = self.coordinator.data.get("data", {}).get("heaters", [])
        for heater in heaters:
            if heater["id"] == self.heater_id:
                return heater
        return None
