from enum import Enum

class IDType(str, Enum):
    AADHAAR = 'AADHAAR'
    LICENSE = 'LICENSE'
    PASSPORT = 'PASSPORT'
    OTHER = 'OTHER'