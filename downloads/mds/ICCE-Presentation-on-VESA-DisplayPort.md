DisplayPort Technical Overview
IEEE International Conference on Consumer Electronics (ICCE)
Advances & Challenges in HD Interconnects
Advances & Challenges in HD Interconnects
January 10, 2011 | Las Vegas
Craig Wiley
Sr. Director of Marketing of Parade Technologies, Inc.
VESA Board of Directors Vice Chair
VESA Board of Directors Vice Chair
VESA Task Group Chair; Marketing, Notebook and 3D Task Groups
DisplayPort Topics
• Quick Overview of Standard
• DisplayPort vs. existing standards
• Layered Protocol Approach
• Layered Protocol Approach
• Physical and Protocol Layers
• System Capabilities
• Usage Examples
g
p
• Future Developments
DisplayPort Quick Overview
Next Generation Display Interface for Personal Computer Products
•
VGA and DVI are to be replaced by DisplayPort
•
The PC industry plans to phase out VGA and DVI over the next
few years – DisplayPort will serve as the new interface for PC
few years
DisplayPort will serve as the new interface for PC
monitors and projectors
•
Now integrated into all main-stream GPU’s and integrated GPU
chip sets – DP receptacles appearing on new PC’s and
notebooks
•
Being applied to other interface applications
•
Embedded DisplayPort (eDP) is the new interface for internal
display panels, replacing LVDS
•
DisplayPort is being enabled in hand-held applications
•
The scalable electrical interface serves small and large
devices and displays
•
DisplayPort is included in the PDMI (CE 2017-A) standard
DisplayPort Quick Overview
DisplayPort Advantages for the Consumer
p
y
g
•
Higher display performance
•
Resolution (up to 4K x 2K at 60 FPS and 24 bpp)
•
Refresh rate (up to 240 FPS for 1080p at 24 bpp)
•
Color Depth (up to 48 bpp, even at 2560 x 1600 at 60 FPS)
C l
A
(
id
i
b
d
l
fil
d t )
•
Color Accuracy (provides in-band color profile data)
•
Multiple display support (up to 63 separate A/V streams supported)
•
Integrated support for legacy video adapters
g
pp
g
y
p
•
Power included at connector, protocol support included
•
Power reduction, increased battery live
•
Cable Consolidation
•
Auxiliary channel can be used for other data traffic
DisplayPort Quick Overview
DisplayPort Advantages for the Industry
p
y
g
y
•
Future extensible
•
Expandable packet-based protocol and link operation rates
p
p
p
p
•
Provides addition data services and display control options
•
Scalable for large and small devices, displays, and cables
•
Single-lane (twisted pair) can support 1680 x 1050 at 18 bpp
•
Easier chip integration, simpler physical interface
L
d
t
l
t
t l
l
k
d
i
•
Leads to lower system cost, lower power, sleeker designs
•
Adaptable to other data interfaces (transport) types
•
Isosynchronous packet stream and control protocols can be
Isosynchronous packet stream and control protocols can be
embedded into other multi-use transport streams
DisplayPort vs. Existing Display Interfaces
The First Consumer Video Interface
NTSC (Introduced in 1941)
-
Used directly as a display interface or as a baseband signal for
Used directly as a display interface, or as a baseband signal for
carrier modulation
-
Consists of a single analog waveform that includes display
synchronization (H-sync, V-sync) and pixel content
y
(
y
y
)
p
-
Keeps display genlocked with video source
Physical interface includes A/V stream data and timing
DisplayPort vs. Existing Display Interfaces
Existing Interfaces use Similar Approach
CGA (Introduced in 1981)
VGA (Introduced in 1987)
U
H
d V
i
li
g
pp
- Use Hsync and Vsync signaling
- Use 3 analog video signals (RGB)
DVI (I t
d
d i
1999)
DVI (Introduced in 1999)
HDMI™ (Introduced in 2003)
-
Use dedicated pixel clock signal (variable frequency)
-
Use Hsync and Vync symbols embedded in digital video stream
y
y
y
g
DisplayPort vs. Existing Display Interfaces
DisplayPort
p
y
DisplayPort™(Introduced in 2008)
-
Unlike other uncompressed data display interfaces, data packet
utilization is similar to communication standards such Ethernet PCI
utilization is similar to communication standards such Ethernet, PCI
Express, USB, SATA
-
Scalable interface fits a variety of system and display applications
-
Future extensible to address new applications and system topologies
pp
y
p
g
-
Transport-adaptable display protocol
-
Designed for DisplayPort transport and (scalable) physical
interface, but can be extended through other transport standards
Fixed data rate packet transport
(choice of link rates and interface lane count)
Overview of DisplayPort Transport Layers
DisplayPort uses a layered protocol for Isochronous AV
DisplayPort uses a layered protocol for Isochronous AV
Stream Transport
Source Device
Sink Device
Source Device
(such as GPU)
Sink Device
(such as Display)
Stream and Link
Policy Layers
Link (Protocol)
and Transport
Layers
Physical Layer
Overview of DisplayPort Transport Layers
•
A/V Streams are received by the Source and regenerated by the Sink
•
The Stream Policy Maker manages the transport of the stream
•
The Link Policy Maker is responsible for establishing the data path
and keeping the link synchronized.
•
The Transport Layer is the Source-to-Sink data interface including
A/V data packetization and inclusion of other data
•
The Physical Layer involves the electrical interface
•
The Physical Layer involves the electrical interface
S
S
DP
Packet
Li k 1
Li k 2
Stream
Sink
Li k 3
DP
Packet
DP
Packet
DP
Packet
DP
Packet
Branch Device
Branch Device
Source Device
Sink Device
Stream
Source
DP
Packet
1
Packet
Source
Link 1
Link 2
Link 3
Packet
Sink
Packet
Source
Packet
Sink
Packet
Source
S
Packet
Sink
Overview of DisplayPort Transport Layers
•
The layered architecture of DisplayPort allows it to be extensible to other transport
types
•
The Isochronous AV Stream can sent be within a dedicated or shared transport
•
VESA and the WiGig Alliance are currently working on the protocol adapter layer
for DisplayPort over the WiGig interface
DisplayPort Transport Options
MST Example
•
DisplayPort 1.1a defined
Single Stream Transport
(SST) for use between a
single Source and Sink
single Source and Sink
Device.
•
DisplayPort 1.2 added the
Multi-Stream Transport
(MST) option, allowing
transport of up to 63
separate A/V streams across
a single DisplayPort
Connection.
•
MST mode allows multiple
•
MST mode allows multiple
Source and/or Sink devices
to share a single connection
Multi-Stream Transport Application
•
One useful MST application is multiple display support from a
single connector
•
This is particularly suited for portable devices that have limited
connector space
DP V1.1a Monitors
DP V1 2 Monitor
DP V1.1a Monitors
DP V1.2 Monitor
DP V1 2 PC
DP1.2 Hub
DP V1.2 PC
DisplayPort Physical Layer Overview
Here we will review the DisplayPort Cable signals:
Lane 0
Lane 1
Main Link
Lane 2
Lane 3
Main Link
Auxiliary (AUX) Channel
Power
Power
Hot Plug Detect
.and other connector configuration pins
DisplayPort Physical Layer Overview
Main Link Signaling Characteristics
g
g
U
l
lt
AC
l d diff
t
i
l
•
Uses a low-voltage, AC coupled different signal
•
Default signal amplitude at Source 400mV p-p
•
Default signal pre-emphasis 0dB
Si
l
li
d
d/
h
i
b
i
d
•
Signal amplitude and/or pre-emphasis can be increased as
a result of link training (as directed by the Sink device)
•
Link training occurs during initial operation, or can be
re-initiated after data errors detected
re initiated after data errors detected.
•
Link training compensates for various connector / cable
losses to assure an error-free data transport
DisplayPort Physical Layer Overview
Main Link Signal coding and data rate
g
g
•
Each main link lane uses 8B/10B encoding which provides
an embedded clock
Uses pseudo random code for EMI mitigation
•
Uses pseudo random code for EMI mitigation
•
One of three fixed rates can be selected
•
1 62 Gbps per lane (1 296 Gbps payload)
•
1.62 Gbps per lane (1.296 Gbps payload)
•
2.7 Gbps per lane (2.16 Gbps payload)
•
5.4 Gbps per lane (4.32 Gbps payload)\*
\*Enable with DP 1 2
Enable with DP 1.2
•
Spread-spectrum clocking can be enabled for further EMI
mitigation
g
•
All DP Source devices are designed to accept SSC
•
1, 2, or 4 lanes can be enabled depending on A/V stream
requirements
DisplayPort Physical Layer Overview
Main Link Bit Rate Selections
Main Link
Configuration
Raw Bit Rate (incl.
coding overhead)
Application Bandwidth
Throughput
1 lane
1.62, 2.7, 5.4\* Gbps
1.296, 2.16, 4.32\* Gbps
2 lanes
3.24, 5.4, 10.8\* Gbps
2.592, 4.32, 8.64\* Gbps
4 lanes
6.48, 10.8, 21.6\* Gbps
5.184, 8.64, 17.28\* Gbps
\*New speed option Enabled by DisplayPort 1.2 Specification
DisplayPort Physical Layer Overview
Resolution Support vs. Interface Data Rate
20 Gbps
120 Hz
DP v1.2
(17.28 Gbps)
60 Hz
pp
15 Gbps
120 Hz
24 bpp
30 bpp
24 bpp
Digital
Display
Interface
Examples
Data Rate
Requirements for
Example Display
Configurations
10 Gbps
120 Hz
120 Hz
36 bpp
60 Hz
30 bpp
DP v1.1a
(8.64 Gbps)
HDMI 340 MHz Clock
(8.16 Gbps)
DL-DVI
120 Hz
30 bpp
120 Hz
120 Hz
36 bpp
Configurations
Standard VESA pixel
5 Gbps
60 Hz
24 bpp
24 bpp
60 Hz
60 Hz
24 bpp
(7.92 Gbps)
HDMI 225 MHz Clock
(5.4 Gbps)
SL-DVI
(3.96 Gbps)
120 Hz
24 bpp
30 bpp
60 Hz
36 bpp
24 Hz
24 bpp
clock rates assumed
n Hz = refresh rate
120 Hz commonly
24 bpp
1080p
1920x1080
WQXGA
2560x1600
24 bpp
WSXGA
1680x1050
4k x 2K
4096x2160
Display Interface Video Data Rate
(actual data payload rate)
used for 3D gaming
bpp = bits per pixel
1920x1080
2560x1600
1680x1050
4096x2160
DP assumes four lane operation
DisplayPort Physical Layer Overview
Number of Monitors Supported vs. Interface Rate
pp
20 Gbps
DP v1.2
(17.28 Gbps)
10
1
Digital
Display
Interface
Examples
Only DP 1.2
Supports
Multiple Displays
15 Gbps
2
4
5
8
7
9
1
Number of Displays
Supported for
Various Display
Configurations
10 Gbps
DP v1.1a
(8.64 Gbps)
HDMI 340 MHz Clock
(8.16 Gbps)
DL-DVI
2
3
3
4
5
6
7
g
Assumptions:
- 1.6% packet overhead
5 Gbps
(7.92 Gbps)
HDMI 225 MHz Clock
(5.4 Gbps)
SL-DVI
(3.96 Gbps)
1
1
2
1
2
2
3
4
1.6% packet overhead
- 60 Hz refresh
- 24 bits-per-pixel
- Standard VESA pixel
clock rates
WQXGA
2560x1600
Full HD
1920x1080
WSXGA
1680x1050
1
WXGA
1280x768
1
4k x 2K
4096x2160
Display Interface Video Data Rate
(actual data payload rate)
2560x1600
1920x1080
1680x1050
1280x768
4096x2160
DP assumes four lane operation
DisplayPort Physical Layer Overview
AUX Channel Signaling Method
~1Vpk-pk differential signal, AC coupled
Bi-directional signal path
g
g
Default “AUX” mode:
1 Mbps transfer rate (either direction)
1 Mbps transfer rate (either direction)
Manchester encoded
“F
t AUX”
d
(
ti
d fi
d b
DP 1 2)
“Fast AUX” mode (option defined by DP 1.2)
720 Mbps transfer rate (either direction)
8B/10B encoded
Includes link training
DisplayPort Physical Layer Overview
Hot Plug Detect Signal Description
g
g
p
Signal provided by the Sink (display) to the Source (GPU)
Typically 0V or 3.3V signal (bi-level).
“High” signal (3.3V) indicates Sink presence.
“Low” signal (0V) > 2 msec indicates Sink absence
Low signal (0V) > 2 msec indicates Sink absence
“Low” signal of 0.5 to 1ms indicates “interrupt” from Sink
(request to read Sink DPCD registers)
DisplayPort Physical Layer Overview
DisplayPort Power Pin
p
y
DisplayPort Source and Sink receptacle includes a power pin
Provides 3.3V at 500 mA (1.5W)
May include higher power option in the future
y
g
p
p
Used to power:
Display Adapters (such as DP to VGA DVI HDMI)
Display Adapters (such as DP to VGA, DVI, HDMI)
Active cables (for greater distance)
Hybrid cables (Fiber optics, etc.)
Display Hubs (for multi-monitor connection)
Pico projectors?
DisplayPort Physical Layer Overview
Connector Interface Pins Showing Power Pin Use
g
DisplayPort Physical Layer Overview
Interface Using Dual-mode adapter
g
p
Cable and Connectors
St
d
d “hi h b
d
idth”
bl
i ti
DP 1 1
Standard “high bandwidth” cables serve existing DP 1.1a
and future DP 1.2 systems
“reduced bandwidth” passive cables (1.62 Gbps) are
available in greater lengths to serve projector and digital
signage applications
Higher bandwidth active cables and hybrid cables also
available (utilize DP power pin)
Two connector types:
Standard DisplayPort connector (USB size)
Standard DisplayPort connector (USB size)
Mini DisplayPort connector (introduced by Apple)
Cable adapter, and adapter cables available
DisplayPort Link Layer Overview
Link Layer = Protocol Layer
y
y
Here we will review:
• Main Stream packet structure
• Auxiliary (AUX) Channel Operation
Auxiliary (AUX) Channel Operation
DisplayPort Link Layer Overview
Micro-Packet “Transfer Unit” (TU)
(
)

The DisplayPort transport layer is operated at a data rate above the stream data rate

Stuffing symbols are used between valid data symbols

When sending video display data (which is the usual application) the transfer units
are stuffed in a means to distribute the video packets evenly over a display line
interval

This means of data system distribution minimizes data buffering in the display

This is referred to Isochronous timing

The Vertical and Horizontal Blanking periods are used to send other packet types
DisplayPort Link Layer Overview
DisplayPort Data Types in Main Link
p
y
yp

The Main Link is the high-speed forward data path

DisplayPort 1.1a defined the use of a single main content stream, normally used
DisplayPort 1.1a defined the use of a single main content stream, normally used
for video

SST = Single Stream Transport

DisplayPort 1.2 adds the option for multiple data stream (up to 53) within the
Main Link
Main Link

MST = Multi Stream Transport
PacketTypes,fora givenstream
Description
Main ContentStream
Transportformatforsendingasinglestreamofvideo oraudio(whichcanbe
l i h
l)
multiͲchannel)
SecondaryDataPacket(SDP)
SecondarydatatransportpacketforavideostreamusedforAudio,CEA861
InfoFrames,mainstream attributedata,andothertypesofdata.
Framingsymbols
UsedtoIdentifybeginningandendof videoframe
VerticalBlankID(VBͲID)
Blankingintervalidentificationandstatusofaudioandvideochannel
CopyProtectionsymbols
Usedbyvideocopyprotectionprotocol.
VideoStreamConfiguration(VSC)
AtypeofSDPthatcontainsadditional3Dformatinformationnotdeclarable
intheMSAfield (introducedinDisplayPortv1.2)
DisplayPort Link Layer Overview
Secondary Data Packet (SDP) Types
y
(
)
yp

Secondary Data Packets are sent during the vertical interval

They are used for a variety of data types including the
following:
InformationSentwithinSDP’s
Description
Audio Stream
Insertedwithinvideostreamblanking period
following:
g p
Maud,Naud (6Bytes),
Usedforaudiostreamclockregenerationinthe
display orotherSinkdevice
Audio TimeStamp
Sent oncepervideoframeforaudioͲaudioandaudioͲ
d
h
videosynchronization
AudioCopyManagement
Content protectionforaudio
Main StreamAttributeData
(MSA)(20Bytes)
Describes videodisplaytimingandpixelclockrateas
wellaspixelformatoncolorparameters
(
) (
y
)
p
p
CEAͲ861ͲEInfoFrames
Sent oncepervideoframeforeachInfoFrame packet
type
CompressedVideoData
Any typeofinformationcanbesentoverSDP’s
DisplayPort Link Layer Overview
Audio Data Transport Capabilities
p
p

A single stream can carry up to 8 LPCM channels at 192 KHz with 24 bit
resolution

This represents ~0 1 Gbps payload which is easily accommodated

This represents ~0.1 Gbps payload, which is easily accommodated

Supported compressed formats include DRA, Dolby MAT, DTS HD

Options Added by DP 1.2

Multi-Stream Transport can extend the number of audio channels

Audio copy protection
Audio copy protection

GTC (Global Time Code) provides very precise time control of audio
channel timing. Each audio channel can have an independent time
delay adjustment between 0 and 4.3 seconds relative to a given
Source in 100 nano second resolution
Used both for lip sync and
Source, in 100 nano-second resolution. Used both for lip sync and
speaker phase control.
DisplayPort Link Layer Overview
Main Stream Attribute (MSA) Data
(
)

MSA Data Packets are sent once per video frame during the vertical
interval

The MSA describes the format of the video with a given stream

The MSA describes the format of the video with a given stream

Some MSA data is optional
PacketTypes,fora givenstream
Description
M id (3 B t
)
U
d f
id
t
l
k
ti
i th di
l
Mvid (3Bytes)
Usedforvideostreamclockregenerationinthedisplay
Nvid (3Bytes)
Usedforvideostreamclockregenerationinthedisplay
Htotal (2Bytes)
Totalnumberofpixel inahorizontalline
Vtotal (2Bytes)
Totalnumberoflinesinthevideoframe
HSP/HSW (2Bytes)
Hsync polarity /Hsync width,inpixels
VSP/VSW (2Bytes)
Vsync polarity /Vsync width,inlines
Hstart (2Bytes)
Start ofactivevideopixelsrelativetheHsync
Vstart (2Bytes)
Start ofactivevideolinesrelativetheVsync
MISC1:0 (2Byte)
Indentifies pixelcolorcodingformat,numberofbitsperpixel,colorgamut,and
othercolorprofileinformation
DisplayPort Link Layer Overview
Framing Symbols
g
y

Framing Symbols are used to identify the BEGINNING and END of:

Vertical Blanking (which thereby indentifies the beginning and end of each
video frame)

A series of stuffing symbols

A “Secondary Data Packet”, which can be used to transport and Audio
stream and other types of information
BasicDisplayPortFramingSymbols
Abbreviation
Description
Bl
ki
St
t
BS
B
i
i
f V
ti
l Bl
ki

Other Framing symbols are used for data scrambler synchronization and copy
protection
BlankingStart
BS
BeginningofVerticalBlanking
BlankingEnd
BE
EndofVerticalBlanking
FillStart
FS
Beginningofstuffingsymbols
FillEnd
FE
Endofstuffingsymbols
Secondary data Start
SS
Beginning of secondary data
SecondaryͲdataStart
SS
Beginningofsecondarydata
SecondaryͲdataEnd
SE
Endofsecondarydata
ScramblerReset
SR
UsedtosynchronizepseudoͲramdom mainlinkdatascrambler
/descramblerbetweenSourceandSink
CopyProtectionBS
CPBS
ForHDCPcopyprotectionuse
Copy Protection SR
CPSR
For HDCP copy protection use
CopyProtectionSR
CPSR
ForHDCPcopyprotectionuse
DisplayPort Link Layer Overview
Framing Symbols
g
y
Example
DisplayPort Link Layer Overview
AUX Channel – Data Formats
•
Standard AUX transport format (Defined by DP 1.1a)
– Manchester transport format
Manchester transport format
– 1Mbps, Burst transfer = 16 data bytes max
– Capable of establishing ~ 200Kbps full-duplex link
•
Fast AUX transport format (New option defined in DP 1.2)
– 720Mbps, Burst transfer = 64/1024 data bytes max
C
bl
f
t bli hi
200Mb
f ll d
l
li k
– Capable of establishing ~ 200Mbps full-duplex link
DisplayPort Link Layer Overview
AUX Channel – Functions used to establish Link
•
AUX is first used by the Source to Discover Sink Capabilities
–
Determines display rendering capabilities and preferences by reading
display EDID (uses special I2C-over-AUX protocol)
– The support of video content protection through HDCP key exchanges
– Determines DisplayPort link transport capabilities by reading DPCD
(DisplayPort Configuration Data) registers
•
AUX is also used to discover interface topology
– If MST is supported and what topology routing will be present
– HDPC support through the virtual channel
•
The stream and link policy makers use this information to
determine stream and link configuration
DisplayPort Link Layer Overview
AUX Channel Functions During Normal Link Operation
•
AUX is used to maintain the link
–
Sink can notify Source that main link data corruption has occurred
–
Data and symbol lock, and optional ECC (Error Correction Code) can be used
y
,
p
(
)
monitor link integrity
–
Source can reinitiate link training to re-establish link
•
AUX can be used to transport auxiliary data, such as:
–
Camera and Microphone A/V data from Sink to Source for teleconferencing
–
Fast AUX mode can be used for USB 2.0 data to support USB hub in Display
(cable consolidation)
(cable consolidation)
•
Display Control
–
AUX can be used to control display setting and operation
–
Can directly support MCCS using I2C-over-AUX protocol
–
Can also support dedicated display control DPCD registers as now used in
Embedded DisplayPort (eDP)
DisplayPort Link Layer Overview
Example System Application Utilizing AUX Data Transport
DP V1.1a monitors
DP V1.2 monitor with
USB Camera/Mic
DP1 2 H b
USB
DP V1.2 PC
DP1.2 Hub
USB Memory Stick
USB
Keyboard
/Mouse
State of Deployment
Many DP 1.1a devices are available from the top PC OEMs
•
GPU Cards, Desktop PCs, and portable PC’s
•
Cables, video adapters
•
Desktop displays
•
Desktop displays
More DP 1.2 devices appearing in 2011
•
GPU’s with 5.4 Gbps main link now on market
•
Used for high-refresh stereo 3D support
•
Existing cables can be used
•
Supporting 3D displays available
•
Multi-stream capable Source devices, hubs and monitors
expected later in year
•
Protocol layer for USB over Fast AUX in development
Other Resources
For more information about DisplayPort
di
l
t
www.displayport.org
www.vesa.org
Contact Information
Craig Wiley, Parade Technologies, Inc.
craig.wiley@paradetech.com
Thank You!
Q&A
Q&A