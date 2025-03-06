from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from datetime import datetime
import json



class JsonModel(BaseModel):
    _key: int
    type: str
    properties__magnitude__value: float
    properties__magnitude__type: str
    properties__magnitude__uncertainty: float
    properties__magnitude__historical_values__0: float
    properties__magnitude__historical_values__1: float
    properties__magnitude__historical_values__2: float
    properties__magnitude__historical_values__3: float
    properties__magnitude__historical_values__4: float
    properties__location__description: str
    properties__location__coordinates__latitude: float
    properties__location__coordinates__longitude: float
    properties__location__coordinates__depth__value: float
    properties__location__coordinates__depth__unit: str
    properties__location__nearby_cities__0__name: str
    properties__location__nearby_cities__0__distance: int
    properties__location__nearby_cities__0__direction: str
    properties__location__nearby_cities__1__name: str
    properties__location__nearby_cities__1__distance: int
    properties__location__nearby_cities__1__direction: str
    properties__location__nearby_cities__2__name: str
    properties__location__nearby_cities__2__distance: int
    properties__location__nearby_cities__2__direction: str
    properties__time__occurrence: int
    properties__time__last_updated: int
    properties__impact__felt: int
    properties__impact__cdi: float
    properties__impact__mmi: Optional[Any]
    properties__impact__alert: Optional[Any]
    properties__impact__reports__0__location: str
    properties__impact__reports__0__intensity: str
    properties__impact__reports__0__reported_magnitudes__0: float
    properties__impact__reports__0__reported_magnitudes__1: float
    properties__impact__reports__0__reported_magnitudes__2: float
    properties__status__current: str
    properties__status__history__0__status: str
    properties__status__history__0__timestamp: int
    properties__status__history__1__status: str
    properties__status__history__1__timestamp: int
    properties__metadata__tsunami: int
    properties__metadata__sig: int
    properties__metadata__network_info__net: str
    properties__metadata__network_info__code: str
    properties__metadata__ids__0: str
    properties__metadata__sources__0: str
    properties__metadata__types__0: str
    properties__metadata__types__1: str
    properties__metadata__types__2: str
    properties__technical_info__nst: int
    properties__technical_info__dmin: float
    properties__technical_info__rms: float
    properties__technical_info__gap: int
    properties__technical_info__seismic_stations__0: int
    properties__technical_info__seismic_stations__1: int
    properties__technical_info__seismic_stations__2: int
    properties__technical_info__seismic_stations__3: int
    properties__technical_info__seismic_stations__4: int
    properties__technical_info__seismic_stations__5: int
    properties__technical_info__seismic_stations__6: int
    properties__technical_info__seismic_stations__7: int
    properties__technical_info__wave_arrivals__0__0: float
    properties__technical_info__wave_arrivals__0__1: float
    properties__technical_info__wave_arrivals__1__0: float
    properties__technical_info__wave_arrivals__1__1: float
    properties__technical_info__wave_arrivals__2__0: float
    properties__technical_info__wave_arrivals__2__1: float
    properties__technical_info__wave_arrivals__3__0: float
    properties__technical_info__wave_arrivals__3__1: float
    properties__technical_info__wave_arrivals__4__0: float
    properties__technical_info__wave_arrivals__4__1: float
    properties__technical_info__wave_arrivals__5__0: float
    properties__technical_info__wave_arrivals__5__1: float
    properties__technical_info__analysis__waveform__peak_ground_acceleration: float
    properties__technical_info__analysis__waveform__peak_ground_velocity: float
    properties__technical_info__analysis__waveform__peak_ground_displacement: float
    properties__technical_info__analysis__waveform__duration: float
    properties__technical_info__analysis__waveform__arias_intensity: float

    @validator('*', pre=True)
    def decode_json_strings(cls, v):
        if isinstance(v, str) and v.strip().startswith('{'):
            try: return json.loads(v)
            except json.JSONDecodeError: return v
        return v