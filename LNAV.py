# -*- coding: utf-8 -*-
# Copyright 2023 Sonardyne International Limited
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
# Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import struct
from enum import Enum

class StatusFlags(Enum):
    """
    Enum contining the bit numbers of the Status Flags for the LNAV message
    """
    OrientationStatusNotOkOrUnsettled = 0,
    PositionStatusInvalid = 1,
    AltitudeStatusOldOrInvalid = 2,
    DepthStatusOldOrInvalid = 3,
    OrientationSourceINS = 4,
    SubseaUSBL_NotUsed = 5,
    Depth_NotUsed = 6,
    DVL_NotUsed = 7,
    LBL_NotUsed = 8,  
    ZUPT_NotUsed = 9,
    XPOS_NotUsed = 10,
    GPS_NotUsed = 11,
    ZMD_NotUsed = 12,
    USBL_NotUsed = 13,
    Euler = 14

class LNAV:
    """
    Class to decode LNAV messages
    
    Properties
    ----------
    TimeOfValidity
    LatitudeDegrees 
    LongitudeDegrees   
    DepthMetres 
    AltitudeMetres 
    RollDegrees 
    PitchDegrees 
    HeadingDegrees 
    VelocityNorthMetresPerSecond 
    VelocityEastMetresPerSecond 
    VelocityDownMetresPerSecond 
    AngularRateForwardDegreesPerSecond 
    AngularRateStarboardDegreesPerSecond 
    AngularRateDownDegreesPerSecond 
    AccelerationForwardMetresPerSecondPerSecond 
    AccelerationStarboardMetresPerSecondPerSecond 
    AccelerationDownMetresPerSecondPerSecond 
    HorizontalPositionErrorSemiMajorMetres 
    HorizontalPositionErrorSemiMinorMetres 
    HorizontalPositionErrorSemiMajorDirectionDegrees 
    VerticalPositionErrorMetres 
    LevelErrorNorthDegrees 
    LevelErrorEastDegrees 
    ErrorHeadingDegrees 
    HorizontalVelocityErrorSemiMajorMetresPerSecond 
    HorizontalVelocityErrorSemiMinorMetresPerSecond 
    HorizontalVelocityErrorSemiMajorDirectionDegrees 
    VerticalVelocityErrorMetresPerSecond 
    StatusFlags 
    
    Methods
    -------
    (static) Decode(byte array) returns LNAV object
    GetStatus(StatusFlags) returns bool
    ToString() returns string
    
    """
    TimeOfValidity = None
    LatitudeDegrees = None 
    LongitudeDegrees = None  
    DepthMetres = None
    AltitudeMetres = None
    RollDegrees = None
    PitchDegrees = None
    HeadingDegrees = None
    VelocityNorthMetresPerSecond = None
    VelocityEastMetresPerSecond = None
    VelocityDownMetresPerSecond = None
    AngularRateForwardDegreesPerSecond = None
    AngularRateStarboardDegreesPerSecond = None
    AngularRateDownDegreesPerSecond = None
    AccelerationForwardMetresPerSecondPerSecond = None
    AccelerationStarboardMetresPerSecondPerSecond = None
    AccelerationDownMetresPerSecondPerSecond = None
    HorizontalPositionErrorSemiMajorMetres = None
    HorizontalPositionErrorSemiMinorMetres = None
    HorizontalPositionErrorSemiMajorDirectionDegrees = None
    VerticalPositionErrorMetres = None
    LevelErrorNorthDegrees = None
    LevelErrorEastDegrees = None
    ErrorHeadingDegrees = None
    HorizontalVelocityErrorSemiMajorMetresPerSecond = None
    HorizontalVelocityErrorSemiMinorMetresPerSecond = None
    HorizontalVelocityErrorSemiMajorDirectionDegrees = None
    VerticalVelocityErrorMetresPerSecond = None
    StatusFlags = None
    
    def __ExtractUnsignedInt(msgBytes):
        """
        __ExtractUnsignedInt takes a byte array and converts it into an unsigned integer (littleendian)

        Parameters
        ----------
        msgBytes : bytes to convert

        Returns
        -------
        unsigned integer result

        """
        return int.from_bytes( msgBytes, "little", signed=False)

    def __ExtractSignedInt(msgBytes):
        """
        __ExtractSignedInt takes a byte array and converts it into a signed integer (littleendian)

        Parameters
        ----------
        msgBytes : bytes to convert

        Returns
        -------
        signed integer result

        """        
        return int.from_bytes( msgBytes, "little", signed=True)

    def __ExtractFloat(msgBytes):
        """
        __ExtractFloat takes a byte array and converts it into a float

        Parameters
        ----------
        msgBytes : bytes to convert

        Returns
        -------
        float result

        """         
        return (struct.unpack('f', msgBytes)[0])
    
    def Decode(message):
        """
        Decode() Takes a byte array containing LNAV data, and returns an LNAV object

        Parameters
        ----------
        message : byte array to decode

        Returns
        -------
        lnav : LNAV object result
        """
        lnav = LNAV()
        lnav.TimeOfValidity = LNAV.__ExtractUnsignedInt(message[0:6])
        lnav.LatitudeDegrees = LNAV.__ExtractSignedInt(message[6:10]) * 90.0 / (1<<31)
        lnav.LongitudeDegrees = LNAV.__ExtractSignedInt(message[10:14]) * 180.0 / (1<<31)
        lnav.DepthMetres = LNAV.__ExtractSignedInt(message[14:18]) / (1e3)
        lnav.AltitudeMetres = LNAV.__ExtractUnsignedInt(message[18:20]) / (1e2)
        lnav.RollDegrees = LNAV.__ExtractSignedInt(message[20:22]) * 180.0 / (1<<15)
        lnav.PitchDegrees = LNAV.__ExtractSignedInt(message[22:24]) * 180.0 / (1<<15)
        lnav.HeadingDegrees = LNAV.__ExtractUnsignedInt(message[24:26]) * 180.0 / (1<<15)
        lnav.VelocityNorthMetresPerSecond = LNAV.__ExtractSignedInt(message[26:28]) / (1e3)       
        lnav.VelocityEastMetresPerSecond = LNAV.__ExtractSignedInt(message[28:30]) / (1e3)
        lnav.VelocityDownMetresPerSecond = LNAV.__ExtractSignedInt(message[30:32]) / (1e3)
        lnav.AngularRateForwardDegreesPerSecond = LNAV.__ExtractSignedInt(message[32:34]) / (1e2)
        lnav.AngularRateStarboardDegreesPerSecond = LNAV.__ExtractSignedInt(message[34:36]) / (1e2)
        lnav.AngularRateDownDegreesPerSecond = LNAV.__ExtractSignedInt(message[36:38]) / (1e2)
        lnav.AccelerationForwardMetresPerSecondPerSecond = LNAV.__ExtractSignedInt(message[38:40]) / (1e3)
        lnav.AccelerationStarboardMetresPerSecondPerSecond = LNAV.__ExtractSignedInt(message[40:42]) / (1e3)
        lnav.AccelerationDownMetresPerSecondPerSecond = LNAV.__ExtractSignedInt(message[42:44]) / (1e3)
        lnav.HorizontalPositionErrorSemiMajorMetres = LNAV.__ExtractFloat(message[44:48])
        lnav.HorizontalPositionErrorSemiMinorMetres = LNAV.__ExtractFloat(message[48:52])
        lnav.HorizontalPositionErrorSemiMajorDirectionDegrees = LNAV.__ExtractFloat(message[52:56])
        lnav.VerticalPositionErrorMetres = LNAV.__ExtractFloat(message[56:60])
        lnav.LevelErrorNorthDegrees = LNAV.__ExtractFloat(message[60:64])
        lnav.LevelErrorEastDegrees = LNAV.__ExtractFloat(message[64:68])
        lnav.ErrorHeadingDegrees = LNAV.__ExtractFloat(message[68:72])
        lnav.HorizontalVelocityErrorSemiMajorMetresPerSecond = LNAV.__ExtractFloat(message[72:76])
        lnav.HorizontalVelocityErrorSemiMinorMetresPerSecond = LNAV.__ExtractFloat(message[76:80])
        lnav.HorizontalVelocityErrorSemiMajorDirectionDegrees = LNAV.__ExtractFloat(message[80:84])
        lnav.VerticalVelocityErrorMetresPerSecond = LNAV.__ExtractFloat(message[84:88])
        lnav.StatusFlags = LNAV.__ExtractUnsignedInt(message[88:90])

        return lnav

    def GetStatus(self, statusFlag):
        """
        GetStatus(StatusFlag) takes a statusFlags enum value and returns it state.

        Parameters
        ----------
        statusFlag : StatusFlags enum value

        Returns
        -------
        Boolean : state of corresponding status bit
        """
        return (self.StatusFlags & (1<<(statusFlag.value[0]))) > 0

    def ToString(self):
        """
        ToString() Returns a string representation of this LNAV object        

        Returns
        -------
        string : string representation of this LNAV object            
        """
        string = ""
        string += "Time of Validity : {}\n".format(self.TimeOfValidity)
        string += "Latitude (deg) : {:.6f}\n".format(self.LatitudeDegrees) 
        string += "Longitude (deg) : {:.6f}\n".format(self.LongitudeDegrees)
        string += "Depth (m) : {:.3f}\n".format(self.DepthMetres)
        string += "Altitude (m) : {:.3f}\n".format(self.AltitudeMetres)
        string += "Roll (deg) : {:.2f}\n".format(self.RollDegrees)
        string += "Pitch (deg) : {:.2f}\n".format(self.PitchDegrees)
        string += "Heading (deg) : {:.2f}\n".format(self.HeadingDegrees)
        string += "Velocity North (m/s) : {:.3f}\n".format(self.VelocityNorthMetresPerSecond)
        string += "Velocity East (m/s) : {:.3f}\n".format(self.VelocityEastMetresPerSecond)
        string += "Velocity Down (m/s) : {:.3f}\n".format(self.VelocityDownMetresPerSecond) 
        string += "Angular Rate Forward (deg/s) : {:.3f}\n".format(self.AngularRateForwardDegreesPerSecond)
        string += "Angular Rate Starboard (deg/s) : {:.3f}\n".format(self.AngularRateStarboardDegreesPerSecond)
        string += "Angular Rate Down (deg/s) : {:.3f}\n".format(self.AngularRateDownDegreesPerSecond)
        string += "Acceleration Forward (m/s/s) : {:.3f}\n".format(self.AccelerationForwardMetresPerSecondPerSecond)
        string += "Acceleration Starboard (m/s/s) : {:.3f}\n".format(self.AccelerationStarboardMetresPerSecondPerSecond)
        string += "Acceleration Down (m/s/s) : {:.3f}\n".format(self.AccelerationDownMetresPerSecondPerSecond)
        string += "Horizontal Position Error Semi-Major (m) : {:.3f}\n".format(self.HorizontalPositionErrorSemiMajorMetres)
        string += "Horizontal Position Error Semi-Minor (m) : {:.3f}\n".format(self.HorizontalPositionErrorSemiMinorMetres)
        string += "Horizontal Position Error Direction (deg) : {:.3f}\n".format(self.HorizontalPositionErrorSemiMajorDirectionDegrees)
        string += "Vertical Position Error (m) : {:.3f}\n".format(self.VerticalPositionErrorMetres)
        string += "Level Error North (deg) : {:.3f}\n".format(self.LevelErrorNorthDegrees)
        string += "Level Error East (deg) : {:.3f}\n".format(self.LevelErrorEastDegrees)
        string += "Heading Error (deg) : {:.3f}\n".format(self.ErrorHeadingDegrees)
        string += "Horizontal Velocity Error Semi-Major (m/s) : {:.3f}\n".format(self.HorizontalVelocityErrorSemiMajorMetresPerSecond)
        string += "Horizontal Velocity Error Semi-Minor (m/s) : {:.3f}\n".format(self.HorizontalVelocityErrorSemiMinorMetresPerSecond)
        string += "Horizontal Velocity Error Direction (deg): {:.3f}\n".format(self.HorizontalVelocityErrorSemiMajorDirectionDegrees)
        string += "Vertical Velocity Error (m/s) : {:.3f}\n".format(self.VerticalVelocityErrorMetresPerSecond)
        string += "Status Flags : 0x{:02X}\n".format(self.StatusFlags)
        
        if (self.GetStatus(StatusFlags.OrientationStatusNotOkOrUnsettled)):
            string += "Orientation Status : Not OK or Unsettled\n"
        else:
            string += "Orientation Status : OK\n"
            
        if (self.GetStatus(StatusFlags.PositionStatusInvalid)):
            string += "Position Status : Invalid\n"
        else:
            string += "Position Status : OK\n"
        
        return string