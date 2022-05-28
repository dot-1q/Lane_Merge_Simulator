class PublicTransportContainer:
    embarkation_status: bool

    def __init__(self, embarkation_status: bool) -> None:
        self.embarkation_status = embarkation_status


class SpecialVehicle:
    public_transport_container: PublicTransportContainer

    def __init__(self, public_transport_container: PublicTransportContainer) -> None:
        self.public_transport_container = public_transport_container


class CAM:
    acc_engaged: bool
    acceleration: int
    altitude: int
    altitude_conf: int
    brake_pedal: bool
    collision_warning: bool
    cruise_control: bool
    curvature: int
    drive_direction: str
    emergency_brake: bool
    gas_pedal: bool
    heading: int
    heading_conf: int
    latitude: int
    length: int
    longitude: int
    semi_major_conf: int
    semi_major_orient: int
    semi_minor_conf: int
    special_vehicle: SpecialVehicle
    speed: int
    speed_conf: int
    speed_limiter: bool
    station_id: int
    station_type: int
    width: int
    yaw_rate: int

    def __init__(
        self,
        acc_engaged: bool,
        acceleration: int,
        altitude: int,
        altitude_conf: int,
        brake_pedal: bool,
        collision_warning: bool,
        cruise_control: bool,
        curvature: int,
        drive_direction: str,
        emergency_brake: bool,
        gas_pedal: bool,
        heading: int,
        heading_conf: int,
        latitude: int,
        length: int,
        longitude: int,
        semi_major_conf: int,
        semi_major_orient: int,
        semi_minor_conf: int,
        special_vehicle: SpecialVehicle,
        speed: int,
        speed_conf: int,
        speed_limiter: bool,
        station_id: int,
        station_type: int,
        width: int,
        yaw_rate: int,
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
