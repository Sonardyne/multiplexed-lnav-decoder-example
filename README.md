# multiplexed-lnav-decoder-example
Simple example LNav message decoder.  It is written in Python (tested in version 3.8.10).  Run ExampleLnavDecoder.py
to try the example.  A sample message is 
constructed in ExampleLnavDecoder.py.  A decoder object is then created and a callback assigned to it to be called 
when a message is successfully decoded.  The sample message is then passed to the decoder.  The decoder is able to 
handle messages that don't arrive in their entirity at the same time, by simply passing the bytes into the decoder 
as they arrive.

# Sample Output
The sample data in the example should produce the following output:

	Time of Validity : 962863849
	Latitude (deg) : 12.000000
	Longitude (deg) : 23.000000
	Depth (m) : 34.000
	Altitude (m) : 10.000
	Roll (deg) : 15.00
	Pitch (deg) : 25.00
	Heading (deg) : 35.00
	Velocity North (m/s) : 2.000
	Velocity East (m/s) : 3.000
	Velocity Down (m/s) : 4.000
	Angular Rate Forward (deg/s) : 5.000
	Angular Rate Starboard (deg/s) : 6.000
	Angular Rate Down (deg/s) : 7.000
	Acceleration Forward (m/s/s) : 8.000
	Acceleration Starboard (m/s/s) : 9.000
	Acceleration Down (m/s/s) : 10.000
	Horizontal Position Error Semi-Major (m) : 11.000
	Horizontal Position Error Semi-Minor (m) : 12.000
	Horizontal Position Error Direction (deg) : 13.000
	Vertical Position Error (m) : 14.000
	Level Error North (deg) : 15.000
	Level Error East (deg) : 16.000
	Heading Error (deg) : 17.000
	Horizontal Velocity Error Semi-Major (m/s) : 18.000
	Horizontal Velocity Error Semi-Minor (m/s) : 19.000
	Horizontal Velocity Error Direction (deg): 20.000
	Vertical Velocity Error (m/s) : 21.000
	Status Flags : 0x00
	Orientation Status : OK
	Position Status : OK