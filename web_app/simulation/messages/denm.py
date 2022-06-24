# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = denm_from_dict(json.loads(json_string))

from typing import Any, TypeVar, Type, cast
from enum import Enum

T = TypeVar("T")


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class CauseCode(Enum):
    merge_event = 31
    breaking = 32
    speeding_up = 33
    maintaining_velocity = 34
    intersection = 35


class SubCauseCode(Enum):
    start_merge = 36
    merge_location = 37
    finished_merge = 38
    not_involved = 39
    helped_merge = 40


class ActionID:
    originating_station_id: int
    sequence_number: int

    def __init__(self, originating_station_id: int, sequence_number: int) -> None:
        self.originating_station_id = originating_station_id
        self.sequence_number = sequence_number

    @staticmethod
    def from_dict(obj: Any) -> "ActionID":
        assert isinstance(obj, dict)
        originating_station_id = from_int(obj.get("originatingStationID"))
        sequence_number = from_int(obj.get("sequenceNumber"))
        return ActionID(originating_station_id, sequence_number)

    def to_dict(self) -> dict:
        result: dict = {}
        result["originatingStationID"] = from_int(self.originating_station_id)
        result["sequenceNumber"] = from_int(self.sequence_number)
        return result


class Altitude:
    altitude_value: int
    altitude_confidence: int

    def __init__(self, altitude_value: int, altitude_confidence: int) -> None:
        self.altitude_value = altitude_value
        self.altitude_confidence = altitude_confidence

    @staticmethod
    def from_dict(obj: Any) -> "Altitude":
        assert isinstance(obj, dict)
        altitude_value = from_int(obj.get("altitudeValue"))
        altitude_confidence = from_int(obj.get("altitudeConfidence"))
        return Altitude(altitude_value, altitude_confidence)

    def to_dict(self) -> dict:
        result: dict = {}
        result["altitudeValue"] = from_int(self.altitude_value)
        result["altitudeConfidence"] = from_int(self.altitude_confidence)
        return result


class PositionConfidenceEllipse:
    semi_major_confidence: int
    semi_minor_confidence: int
    semi_major_orientation: int

    def __init__(
        self,
        semi_major_confidence: int,
        semi_minor_confidence: int,
        semi_major_orientation: int,
    ) -> None:
        self.semi_major_confidence = semi_major_confidence
        self.semi_minor_confidence = semi_minor_confidence
        self.semi_major_orientation = semi_major_orientation

    @staticmethod
    def from_dict(obj: Any) -> "PositionConfidenceEllipse":
        assert isinstance(obj, dict)
        semi_major_confidence = from_int(obj.get("semiMajorConfidence"))
        semi_minor_confidence = from_int(obj.get("semiMinorConfidence"))
        semi_major_orientation = from_int(obj.get("semiMajorOrientation"))
        return PositionConfidenceEllipse(
            semi_major_confidence, semi_minor_confidence, semi_major_orientation
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["semiMajorConfidence"] = from_int(self.semi_major_confidence)
        result["semiMinorConfidence"] = from_int(self.semi_minor_confidence)
        result["semiMajorOrientation"] = from_int(self.semi_major_orientation)
        return result


class EventPosition:
    latitude: float
    longitude: float
    position_confidence_ellipse: PositionConfidenceEllipse
    altitude: Altitude

    def __init__(
        self,
        latitude: float,
        longitude: float,
        position_confidence_ellipse: PositionConfidenceEllipse,
        altitude: Altitude,
    ) -> None:
        self.latitude = latitude
        self.longitude = longitude
        self.position_confidence_ellipse = position_confidence_ellipse
        self.altitude = altitude

    @staticmethod
    def from_dict(obj: Any) -> "EventPosition":
        assert isinstance(obj, dict)
        latitude = from_float(obj.get("latitude"))
        longitude = from_float(obj.get("longitude"))
        position_confidence_ellipse = PositionConfidenceEllipse.from_dict(
            obj.get("positionConfidenceEllipse")
        )
        altitude = Altitude.from_dict(obj.get("altitude"))
        return EventPosition(latitude, longitude, position_confidence_ellipse, altitude)

    def to_dict(self) -> dict:
        result: dict = {}
        result["latitude"] = to_float(self.latitude)
        result["longitude"] = to_float(self.longitude)
        result["positionConfidenceEllipse"] = to_class(
            PositionConfidenceEllipse, self.position_confidence_ellipse
        )
        result["altitude"] = to_class(Altitude, self.altitude)
        return result


class Management:
    action_id: ActionID
    detection_time: float
    reference_time: float
    event_position: EventPosition
    validity_duration: int
    station_type: int

    def __init__(
        self,
        action_id: ActionID,
        detection_time: float,
        reference_time: float,
        event_position: EventPosition,
        validity_duration: int,
        station_type: int,
    ) -> None:
        self.action_id = action_id
        self.detection_time = detection_time
        self.reference_time = reference_time
        self.event_position = event_position
        self.validity_duration = validity_duration
        self.station_type = station_type

    @staticmethod
    def from_dict(obj: Any) -> "Management":
        assert isinstance(obj, dict)
        action_id = ActionID.from_dict(obj.get("actionID"))
        detection_time = from_float(obj.get("detectionTime"))
        reference_time = from_float(obj.get("referenceTime"))
        event_position = EventPosition.from_dict(obj.get("eventPosition"))
        validity_duration = from_int(obj.get("validityDuration"))
        station_type = from_int(obj.get("stationType"))
        return Management(
            action_id,
            detection_time,
            reference_time,
            event_position,
            validity_duration,
            station_type,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["actionID"] = to_class(ActionID, self.action_id)
        result["detectionTime"] = to_float(self.detection_time)
        result["referenceTime"] = to_float(self.reference_time)
        result["eventPosition"] = to_class(EventPosition, self.event_position)
        result["validityDuration"] = from_int(self.validity_duration)
        result["stationType"] = from_int(self.station_type)
        return result


class EventType:
    cause_code: int
    sub_cause_code: int

    def __init__(self, cause_code: int, sub_cause_code: int) -> None:
        self.cause_code = cause_code
        self.sub_cause_code = sub_cause_code

    @staticmethod
    def from_dict(obj: Any) -> "EventType":
        assert isinstance(obj, dict)
        cause_code = from_int(obj.get("causeCode"))
        sub_cause_code = from_int(obj.get("subCauseCode"))
        return EventType(cause_code, sub_cause_code)

    def to_dict(self) -> dict:
        result: dict = {}
        result["causeCode"] = from_int(self.cause_code)
        result["subCauseCode"] = from_int(self.sub_cause_code)
        return result


class Situation:
    information_quality: int
    event_type: EventType

    def __init__(self, information_quality: int, event_type: EventType) -> None:
        self.information_quality = information_quality
        self.event_type = event_type

    @staticmethod
    def from_dict(obj: Any) -> "Situation":
        assert isinstance(obj, dict)
        information_quality = from_int(obj.get("informationQuality"))
        event_type = EventType.from_dict(obj.get("eventType"))
        return Situation(information_quality, event_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["informationQuality"] = from_int(self.information_quality)
        result["eventType"] = to_class(EventType, self.event_type)
        return result


class DENM:
    management: Management
    situation: Situation

    def __init__(self, management: Management, situation: Situation) -> None:
        self.management = management
        self.situation = situation

    @staticmethod
    def from_dict(obj: Any) -> "DENM":
        assert isinstance(obj, dict)
        management = Management.from_dict(obj.get("management"))
        situation = Situation.from_dict(obj.get("situation"))
        return DENM(management, situation)

    def to_dict(self) -> dict:
        result: dict = {}
        result["management"] = to_class(Management, self.management)
        result["situation"] = to_class(Situation, self.situation)
        return result


def denm_from_dict(s: Any) -> DENM:
    return DENM.from_dict(s)


def denm_to_dict(x: DENM) -> Any:
    return to_class(DENM, x)
