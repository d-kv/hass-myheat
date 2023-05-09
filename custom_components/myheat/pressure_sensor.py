"""Sensor platform for MyHeat."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import (SensorEntity, SensorDeviceClass, UnitOfPressure)

from .const import DEFAULT_NAME
from .const import DOMAIN
from .const import ICON
from .const import SENSOR
from .entity import MhEntity

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Setup climate platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    _logger.info(f"Setting up heaters: {coordinator.data}")

    async_add_entities(
        [
            MhPressureSensor(coordinator, entry, heater)
            for heater in coordinator.data.get("data", {}).get("heater", [])
        ]
    )

class MhPressureSensor(MhEntity, SensorEntity):
    """myheat Pressure Sensor class."""

    _attr_device_class = SensorDeviceClass.PRESSURE
    _attr_unit_of_measurement = UnitOfPressure.BAR

    def __init__(self, coordinator, config_entry, heater):
        super().__init__(coordinator, config_entry)
        self.heater = heater

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DEFAULT_NAME}_{SENSOR}_pressure"

    @property
    def state(self):
        """Return the state of the sensor."""
        heaters = self.coordinator.data.get("data", {}).get("heaters", [])
        for heater in heaters:
            if heater["id"] == self.heater["id"]:
                return heater["pressure"]
        return None

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return "myheat__custom_device_class"
