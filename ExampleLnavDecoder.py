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

import MultiplexedDecoder as md

# Create a callback for when a LNAV Message has been decoded.
def LnavReceived(lnav):
    print(lnav.ToString())

testMessage = bytearray([0x10, 0x02, 0x00, 0xe0, 0xe9, 0x22, 0x64, 0x39, 0x00, 0x00, \
                         0x11, 0x11, 0x11, 0x11, 0xb0, 0x05, 0x5b, 0x10, 0x10, 0xd0, \
                         0x84, 0x00, 0x00, 0xe8, 0x03, 0xaa, 0x0a, 0xc7, 0x11, 0xe3, \
                         0x18, 0xd0, 0x07, 0xb8, 0x0b, 0xa0, 0x0f, 0xf4, 0x01, 0x58, \
                         0x02, 0xbc, 0x02, 0x40, 0x1f, 0x28, 0x23, 0x10, 0x10, 0x27, \
                         0x00, 0x00, 0x30, 0x41, 0x00, 0x00, 0x40, 0x41, 0x00, 0x00, \
                         0x50, 0x41, 0x00, 0x00, 0x60, 0x41, 0x00, 0x00, 0x70, 0x41, \
                         0x00, 0x00, 0x80, 0x41, 0x00, 0x00, 0x88, 0x41, 0x00, 0x00, \
                         0x90, 0x41, 0x00, 0x00, 0x98, 0x41, 0x00, 0x00, 0xa0, 0x41, \
                         0x00, 0x00, 0xa8, 0x41, 0x00, 0x00, 0x7a, 0x10, 0x03 
])
    
# Create a multiplexed decoder
multiplexedDecoder = md.MultiplexedDecoder()

# Give the deocoder a callback for when an LNAV message has been decoded
multiplexedDecoder.AddLnavCallback(LnavReceived)

# Pass the received bytes to the decoder - the MultiplexDecoder class keeps a bufer of bytes received so far
# so bytes may be passed to the multiplex decoder as they arrive, and will be kept until they form a valid messaage
multiplexedDecoder.DecodeBytes(testMessage)


