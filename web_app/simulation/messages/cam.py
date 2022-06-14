from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


class PublicTransportContainer:
    embarkation_status: bool

    def __init__(self, embarkation_status: bool) -> None:
        self.embarkation_status = embarkation_status

    @staticmethod
    def from_dict(obj: Any) -> "PublicTransportContainer":
        assert isinstance(obj, dict)
        embarkation_status = from_bool(obj.get("embarkationStatus"))
        return PublicTransportContainer(embarkation_status)

    def to_dict(self) -> dict:
        result: dict = {}
        result["embarkationStatus"] = from_bool(self.embarkation_status)
        return result


class SpecialVehicle:
    public_transport_container: PublicTransportContainer

    def __init__(self, public_transport_container: PublicTransportContainer) -> None:
        self.public_transport_container = public_transport_container

    @staticmethod
    def from_dict(obj: Any) -> "SpecialVehicle":
        assert isinstance(obj, dict)
        public_transport_container = PublicTransportContainer.from_dict(
            obj.get("publicTransportContainer")
        )
        return SpecialVehicle(public_transport_container)

    def to_dict(self) -> dict:
        result: dict = {}
        result["publicTransportContainer"] = to_class(
            PublicTransportContainer, self.public_transport_container
        )
        return result


class CAM:
    acc_engaged: bool
    acceleration: float
    altitude: float
    altitude_conf: int
    brake_pedal: bool
    collision_warning: bool
    cruise_control: bool
    curvature: int
    drive_direction: str
    emergency_brake: bool
    gas_pedal: bool
    heading: float
    heading_conf: float
    latitude: float
    length: float
    longitude: float
    semi_major_conf: int
    semi_major_orient: int
    semi_minor_conf: int
    special_vehicle: SpecialVehicle
    speed: float
    speed_conf: float
    speed_limiter: bool
    station_id: int
    station_type: int
    width: float
    yaw_rate: float

    def __init__(
        self,
        acc_engaged: bool,
        acceleration: float,
        altitude: float,
        altitude_conf: int,
        brake_pedal: bool,
        collision_warning: bool,
        cruise_control: bool,
        curvature: int,
        drive_direction: str,
        emergency_brake: bool,
        gas_pedal: bool,
        heading: float,
        heading_conf: float,
        latitude: float,
        length: float,
        longitude: float,
        semi_major_conf: int,
        semi_major_orient: int,
        semi_minor_conf: int,
        special_vehicle: SpecialVehicle,
        speed: float,
        speed_conf: float,
        speed_limiter: bool,
        station_id: int,
        station_type: int,
        width: float,
        yaw_rate: float,
    ) -> None:
        self.acc_engaged = acc_engaged
        self.acceleration = acceleration
        self.altitude = altitude
        self.altitude_conf = altitude_conf
        self.brake_pedal = brake_pedal
        self.collision_warning = collision_warning
        self.cruise_control = cruise_control
        self.curvature = curvature
        self.drive_direction = drive_direction
        self.emergency_brake = emergency_brake
        self.gas_pedal = gas_pedal
        self.heading = heading
        self.heading_conf = heading_conf
        self.latitude = latitude
        self.length = length
        self.longitude = longitude
        self.semi_major_conf = semi_major_conf
        self.semi_major_orient = semi_major_orient
        self.semi_minor_conf = semi_minor_conf
        self.special_vehicle = special_vehicle
        self.speed = speed
        self.speed_conf = speed_conf
        self.speed_limiter = speed_limiter
        self.station_id = station_id
        self.station_type = station_type
        self.width = width
        self.yaw_rate = yaw_rate

    @staticmethod
    def from_dict(obj: Any) -> "CAM":
        assert isinstance(obj, dict)
        acc_engaged = from_bool(obj.get("accEngaged"))
        acceleration = from_float(obj.get("acceleration"))
        altitude = from_float(obj.get("altitude"))
        altitude_conf = from_int(obj.get("altitudeConf"))
        brake_pedal = from_bool(obj.get("brakePedal"))
        collision_warning = from_bool(obj.get("collisionWarning"))
        cruise_control = from_bool(obj.get("cruiseControl"))
        curvature = from_int(obj.get("curvature"))
        drive_direction = from_str(obj.get("driveDirection"))
        emergency_brake = from_bool(obj.get("emergencyBrake"))
        gas_pedal = from_bool(obj.get("gasPedal"))
        heading = from_float(obj.get("heading"))
        heading_conf = from_float(obj.get("headingConf"))
        latitude = from_float(obj.get("latitude"))
        length = from_float(obj.get("length"))
        longitude = from_float(obj.get("longitude"))
        semi_major_conf = from_int(obj.get("semiMajorConf"))
        semi_major_orient = from_int(obj.get("semiMajorOrient"))
        semi_minor_conf = from_int(obj.get("semiMinorConf"))
        special_vehicle = SpecialVehicle.from_dict(obj.get("specialVehicle"))
        speed = from_float(obj.get("speed"))
        speed_conf = from_float(obj.get("speedConf"))
        speed_limiter = from_bool(obj.get("speedLimiter"))
        station_id = from_int(obj.get("stationID"))
        station_type = from_int(obj.get("stationType"))
        width = from_float(obj.get("width"))
        yaw_rate = from_float(obj.get("yawRate"))
        return CAM(
            acc_engaged,
            acceleration,
            altitude,
            altitude_conf,
            brake_pedal,
            collision_warning,
            cruise_control,
            curvature,
            drive_direction,
            emergency_brake,
            gas_pedal,
            heading,
            heading_conf,
            latitude,
            length,
            longitude,
            semi_major_conf,
            semi_major_orient,
            semi_minor_conf,
            special_vehicle,
            speed,
            speed_conf,
            speed_limiter,
            station_id,
            station_type,
            width,
            yaw_rate,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["accEngaged"] = from_bool(self.acc_engaged)
        result["acceleration"] = from_float(self.acceleration)
        result["altitude"] = from_float(self.altitude)
        result["altitudeConf"] = from_int(self.altitude_conf)
        result["brakePedal"] = from_bool(self.brake_pedal)
        result["collisionWarning"] = from_bool(self.collision_warning)
        result["cruiseControl"] = from_bool(self.cruise_control)
        result["curvature"] = from_int(self.curvature)
        result["driveDirection"] = from_str(self.drive_direction)
        result["emergencyBrake"] = from_bool(self.emergency_brake)
        result["gasPedal"] = from_bool(self.gas_pedal)
        result["heading"] = from_float(self.heading)
        result["headingConf"] = from_float(self.heading_conf)
        result["latitude"] = to_float(self.latitude)
        result["length"] = from_float(self.length)
        result["longitude"] = to_float(self.longitude)
        result["semiMajorConf"] = from_int(self.semi_major_conf)
        result["semiMajorOrient"] = from_int(self.semi_major_orient)
        result["semiMinorConf"] = from_int(self.semi_minor_conf)
        result["specialVehicle"] = to_class(SpecialVehicle, self.special_vehicle)
        result["speed"] = from_float(self.speed)
        result["speedConf"] = from_float(self.speed_conf)
        result["speedLimiter"] = from_bool(self.speed_limiter)
        result["stationID"] = from_int(self.station_id)
        result["stationType"] = from_int(self.station_type)
        result["width"] = from_float(self.width)
        result["yawRate"] = from_float(self.yaw_rate)
        return result


def cam_from_dict(s: Any) -> CAM:
    return CAM.from_dict(s)


def cam_to_dict(x: CAM) -> Any:
    return to_class(CAM, x)
