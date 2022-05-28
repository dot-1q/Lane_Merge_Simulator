from enum import Enum


class CauseCode(Enum):
    MergeEvent = 31
    Breaking = 32
    SpeedingUp = 33
    MaintainingVelocity = 34


class SubCauseCode(Enum):
    MergeRequest = 31
    StartMerge = 32
    FinishedMerge = 33
    MergeDenied = 34
    NotInvolved = 35


class ActionID:
    originating_station_id: int
    sequence_number: int

    def __init__(self, originating_station_id: int, sequence_number: int) -> None:
        self.originating_station_id = originating_station_id
        self.sequence_number = sequence_number


class Altitude:
    altitude_value: int
    altitude_confidence: int

    def __init__(self, altitude_value: int, altitude_confidence: int) -> None:
        self.altitude_value = altitude_value
        self.altitude_confidence = altitude_confidence


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


class EventType:
    cause_code: int
    sub_cause_code: int

    def __init__(self, cause_code: int, sub_cause_code: int) -> None:
        self.cause_code = cause_code
        self.sub_cause_code = sub_cause_code


class Situation:
    information_quality: int
    event_type: EventType

    def __init__(self, information_quality: int, event_type: EventType) -> None:
        self.information_quality = information_quality
        self.event_type = event_type


class DENM:
    management: Management
    situation: Situation

    def __init__(self, management: Management, situation: Situation) -> None:
        self.management = management
        self.situation = situation
