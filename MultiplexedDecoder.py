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

from enum import Enum
from LNAV import LNAV

# This could be expanded to decode other types of message
class _MessageId(Enum):
    """
    An Enum of multiplexed message IDs
    """
    LNAV = 224

class MultiplexedDecoder:    
    """
    A Class which decodes Sonardyne Multiplexed Packets
    
    Methods
    -------
    DecodeBytes(byte array of bytes to be decoded)
    
    AddLnavCallback(function to provide callback when an LNAV is received)
    """
    
    def __init__(self):
        self.__inMessage = False
        self.__dleReceived = False
        self.__currentMessage = b''
        self.__LnavCallback = None

    def __DecodeMessage(self, message):
        """
        __DecodeMessage takes a message (where the DLE+STX / DLE+ETX and any DLE+DLE have already been removed) checks it's checksum, 
        and then calls the appropriate decoder based on the message ID.  If the checksum fails or the message is the 
        wrong number of bytes it exits without attempting to decode anything.

        Parameters
        ----------
        message : byte array - contains the message to be decoded with the DLE STX and DLE ETX removed
            
        Returns
        -------
        None.
        """
        
        # XOR all the bytes, if the result is zero then the checksum is OK
        checksum = 0
        for byte in message:
            checksum ^= byte
        if checksum != 0:
            # Checksum error
            return

        # 'hasTime' not used here - but included for reference
        hasTime = message[0] & 0x80 == 0x80
        messageId = ((message[0] & 0x03) << 8) + message[1]
        
        # subtract 3 off for the 2 bytes header and the 1 byte checksum to get the message length
        # This could be extended to decode other message ids
        if (messageId == _MessageId.LNAV.value and (len(message) -3) == 90):
            lnav = LNAV.Decode(message[2:92]) 
            if self.__LnavCallback is not None:
                self.__LnavCallback(lnav)
    
    # Un-byte-stuffs the multiplexed packets.  Packets start with DLE STX, and finish with DLE ETX.  
    # Any DLE characters within the message are escaped with another DLE
    def DecodeBytes(self, multiplexedBytes):
        """
        DecodeBytes takes an array of bytes and unbyte-stuffs and demultiplexes the message it contains.
        it keeps a buffer of bytes received, so may be called repeatedly with bytes as they are received

        Parameters
        ----------
        multiplexedBytes : byte array - bytes to be decoded.

        Returns
        -------
        None.
        """
        
        DLE = b"\x10"
        STX = b"\x02"
        ETX = b"\x03"
            
        for dbyte in multiplexedBytes:
            dbyte = dbyte.to_bytes(1,byteorder='big')
            if dbyte != '':
                # stop the buffer getting indefinately large - if it's more than 4K, then it's not a valid message
                if len(self.__currentMessage) > 4096:
                    self.__dleReceived = False
                    self.__inMessage = False
                    self.__currentMessage = b""                       
                
                if dbyte == DLE: 
                    if self.__dleReceived:
                        # DLE escaping by other DLE - so add a DLE to the message
                        self.__dleReceived = False
                        if (self.__inMessage):
                            self.__currentMessage += dbyte
                    else:
                        # otherwise record that a DLE has been received
                        self.__dleReceived = True

                elif dbyte == STX:
                    if self.__dleReceived:
                        # if a STX is received after a DLE then clear down and start a new message
                        self.__dleReceived = False
                        self.__inMessage = True
                        self.__currentMessage = b""   
                    else:
                        # otherwise if it's just an STX on it's own just add the STX to the message
                        if (self.__inMessage):
                            self.__currentMessage += dbyte
                        
                elif dbyte == ETX:
                    if self.__dleReceived:
                        # if a ETX is received after a DLE and we are in a message, then we have a complete message to pass to DecodeMessage()
                        self.__dleReceived = False
                        if (self.__inMessage):
                            self.__inMessage = False
                            self.__DecodeMessage(self.__currentMessage)
                    else:
                        # otherwise if it's just an ETX on it's own just add the ETX to the message                        
                        if (self.__inMessage):
                            self.__currentMessage += dbyte           
                else:
                    if self.__dleReceived:
                        # This shouldn't happen - DLE Should always be followed by STX, ETX or DLE
                        # error unescaped DLE
                        # So start listing for a new DLE
                        self.__dleReceived = False
                        self.__inMessage = False
                        self.__currentMessage = b""                       
                    else:               
                        # otherwise add the byte to the message                        
                        if (self.__inMessage):
                            self.__currentMessage += dbyte

                                            

    def AddLnavCallback(self, func):
        """
        AddLnavCallback

        Parameters
        ----------
        func : function - A callback to be called when an LNAV message is decoded.  The callback takes one parmeter, which is
        an LNAV object

        Returns
        -------
        None.

        """
        self.__LnavCallback = func
