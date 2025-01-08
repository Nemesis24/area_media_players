import logging
from homeassistant.components.sensor import SensorEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.const import STATE_ON, STATE_OFF
from homeassistant.core import callback
from homeassistant.helpers import entity_registry, area_registry, device_registry
from .const import DOMAIN, ATTR_COUNT, ATTR_TOTAL, ACTIVE_STATES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    excluded = entry.data.get("excluded_entities", [])
    
    _LOGGER.debug("Starting Area Media Players configuration")
    _LOGGER.debug(f"Excluded entities: {excluded}")
    
    area_reg = area_registry.async_get(hass)
    entity_reg = entity_registry.async_get(hass)
    device_reg = device_registry.async_get(hass)
    
    areas = area_reg.async_list_areas()
    _LOGGER.debug(f"Found areas: {[area.name for area in areas]}")
    
    switches = []
    all_players = set()
    
    for area in areas:
        area_players = set()
        area_excluded = set()
        
        for entity in entity_reg.entities.values():
            if entity.entity_id.startswith("media_player.") and entity.area_id == area.id:
                if entity.entity_id not in excluded:
                    area_players.add(entity.entity_id)
                    _LOGGER.debug(f"Media player {entity.entity_id} found directly in {area.name}")
                else:
                    area_excluded.add(entity.entity_id)
        
        for device_id in device_reg.devices:
            device = device_reg.async_get(device_id)
            if device and device.area_id == area.id:
                for entity in entity_reg.entities.values():
                    if entity.device_id == device_id and entity.entity_id.startswith("media_player."):
                        if entity.entity_id not in excluded:
                            area_players.add(entity.entity_id)
                            _LOGGER.debug(f"Media player {entity.entity_id} found via device in {area.name}")
                        else:
                            area_excluded.add(entity.entity_id)
        
        if area_players:
            _LOGGER.debug(f"Area {area.name}: {len(area_players)} media players found: {area_players}")
            switches.append(RoomMediaPlayersSwitch(area.name, list(area_players), list(area_excluded)))
            all_players.update(area_players)

    if all_players:
        _LOGGER.debug(f"Total media players found: {len(all_players)}")
        switches.append(AllMediaPlayersSwitch(list(all_players), excluded)) 
    
    _LOGGER.debug(f"Creating {len(switches)} switches")
    async_add_entities(switches)

class RoomMediaPlayersSwitch(SensorEntity, SwitchEntity):
    def __init__(self, room_name, players, excluded_players):
        self._room = room_name
        self._players = players
        self._excluded_players = excluded_players
        self._attr_name = f"Media Players {room_name}"
        self._attr_unique_id = f"area_media_players_{room_name.lower().replace(' ', '_')}"
        self._state = STATE_OFF
        self._count = 0
        self._total = len(players)
        self._players_active = []
        self._players_inactive = []
        _LOGGER.debug(f"Initializing switch {self._attr_name} with {self._total} media players: {self._players}")

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        return "mdi:monitor-speaker" if self._state == STATE_ON else "mdi:monitor-speaker-off"

    @property
    def extra_state_attributes(self):
        return {
            "count": self._count,
            "of": self._total,
            "count_of": f"{self._count}/{self._total}",
            "players_active": self._players_active,
            "players_inactive": self._players_inactive,
            "excluded_players": self._excluded_players, 
        }

    @property
    def is_on(self):
        return self._state == STATE_ON

    async def async_turn_on(self, **kwargs):
        for player_id in self._players:
            await self.hass.services.async_call(
                "media_player", "turn_on", {"entity_id": player_id}
            )
        self._state = STATE_ON
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        for player_id in self._players:
            await self.hass.services.async_call(
                "media_player", "turn_off", {"entity_id": player_id}
            )
        self._state = STATE_OFF
        self.async_write_ha_state()

    async def async_added_to_hass(self):
        @callback
        def async_state_changed(*_):
            self.async_schedule_update_ha_state(True)

        for player in self._players:
            self.async_on_remove(
                self.hass.helpers.event.async_track_state_change(
                    player, async_state_changed
                )
            )
        
        self.async_schedule_update_ha_state(True)

    async def async_update(self):
        self._count = 0
        self._players_active = []
        self._players_inactive = []
        
        for player_id in self._players:
            state = self.hass.states.get(player_id)
            if state and state.state in ACTIVE_STATES:
                self._count += 1
                self._players_active.append(player_id)
            else:
                self._players_inactive.append(player_id)
        
        self._state = STATE_ON if self._count > 0 else STATE_OFF
        _LOGGER.debug(f"Updating {self._attr_name}: {self._count}/{self._total} media players active")

class AllMediaPlayersSwitch(RoomMediaPlayersSwitch):
    def __init__(self, players, excluded_players):
        super().__init__("All", players, excluded_players)
        self._attr_name = "All Area Media Players"
        self._attr_unique_id = "area_media_players_all"

    async def async_turn_on(self, **kwargs):
        for player_id in self._players:
            await self.hass.services.async_call(
                "media_player", "turn_on", {"entity_id": player_id}
            )
        self._state = STATE_ON
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        for player_id in self._players:
            await self.hass.services.async_call(
                "media_player", "turn_off", {"entity_id": player_id}
            )
        self._state = STATE_OFF
        self.async_write_ha_state()
