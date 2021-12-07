class FastAPIUsersException(Exception):
    pass


class UserAlreadyExists(FastAPIUsersException):
    pass


class UsernameAlreadyRegistered(FastAPIUsersException):
    pass


class EmailAlreadyRegistered(FastAPIUsersException):
    pass


class DniAlreadyRegistered(FastAPIUsersException):
    pass


class LicenseAlreadyRegistered(FastAPIUsersException):
    pass


class UserNotExists(FastAPIUsersException):
    pass


class UserInactive(FastAPIUsersException):
    pass


class StudyAlreadyWithSample(FastAPIUsersException):
    pass


class StudyAlreadyWithAppointment(FastAPIUsersException):
    pass


class StudyAlreadyWithReport(FastAPIUsersException):
    pass


class AppointmentOverlap(FastAPIUsersException):
    pass


class SampleBatchAlreadyProccesed(FastAPIUsersException):
    pass


class SampleAlreadyPickedUp(FastAPIUsersException):
    pass


class SampleAlreadyPaid(FastAPIUsersException):
    pass
