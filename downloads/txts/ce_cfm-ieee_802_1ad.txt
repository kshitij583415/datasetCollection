IEEE 802.1ad Support on Provider Bridges
First Published: April 19, 2010
Last Updated: May 26, 2011
Service provider bridges (also called provider bridges) allow devices in a service provider network to
transparently carry the Layer 2 control frames of a customer. Spanning Tree Protocol (STP) bridge protocol
data units (BPDUs) or Cisco Discovery Protocol frames are carried separately from the service provider
traffic and from other customer traffic in the network of a service provider.
User network interface (UNI) ports of a provider bridge interface with customer devices have a specific set
of requirements defined by the IEEE 802.1ad standard. These requirements enable provider bridges to have
the same functionality as Layer 2 protocol tunneling and Q-in-Q (QnQ) bridges.
This document describes the IEEE 802.1ad implementation on Cisco devices using Layer 2 switch ports.
• Finding Feature Information, page 1
• Restrictions for IEEE 802.1ad Support on Provider Bridges, page 2
• Information About IEEE 802.1ad Support on Provider Bridges, page 2
• How to Configure IEEE 802.1ad Support on Provider Bridges, page 8
• Configuration Examples for IEEE 802.1ad Support on Provider Bridges, page 10
• Additional References for IEEE 802.1ad Support on Provider Bridges, page 11
• Feature Information for IEEE 802.1ad Support on Provider Bridges, page 11
• Glossary, page 12
Finding Feature Information
Your software release may not support all the features documented in this module. For the latest caveats and
feature information, see Bug Search Tool and the release notes for your platform and software release. To
find information about the features documented in this module, and to see a list of the releases in which each
feature is supported, see the feature information table.
Use Cisco Feature Navigator to find information about platform support and Cisco software image support.
To access Cisco Feature Navigator, go to www.cisco.com/go/cfn. An account on Cisco.com is not required.
Carrier Ethernet Configuration Guide, Cisco IOS XE Release 3E
1
Restrictions for IEEE 802.1ad Support on Provider Bridges
• The IEEE 802.1ad Support on Provider Bridges feature is not supported on the Cisco ME3400 series
switch.
• In Cisco IOS Release 12.2(54)SE, the Cisco ME 3400E and Catalyst 3750 Metro switch platforms
support this feature. The Cisco ME3400 switch platform does not support this feature.
Information About IEEE 802.1ad Support on Provider Bridges
Service Provider Bridges
Provider bridges pass the network traffic of multiple customers. The traffic flow of each customer must be
isolated from one another. For Layer 2 protocols within customer domains to function properly, geographically
separated customer sites must appear to be connected via a LAN and the provider network must be transparent.
The IEEE has reserved 33 Layer 2 MAC addresses for customer devices that operate Layer 2 protocols. If a
provider bridge uses these standard MAC addresses for its Layer 2 protocols, the Layer 2 traffic of the customer
devices and the service provider is mixed together. Provider bridges solve this traffic-mixing issue by providing
Layer 2 protocol data unit (PDU) tunneling when a provider bridge (S-bridge) component and a provider edge
bridge (C-bridge) component are used. The figure below shows the topology.
Figure 1: Layer 2 PDU Tunneling
S-Bridge Component
The S-bridge component is capable of inserting or removing a service provider VLAN (S-VLAN) for all
traffic on a particular port. IEEE 802.1ad adds a new tag called a Service tag (S-tag) to all ingress frames
traveling from the customer to the service provider.
Carrier Ethernet Configuration Guide, Cisco IOS XE Release 3E
2
IEEE 802.1ad Support on Provider Bridges
Restrictions for IEEE 802.1ad Support on Provider Bridges
The VLAN in the S-tag is used for forwarding the traffic in the service provider network. Different customers
use different S-VLANs, which results in isolation of traffic of each customer. In the S-tag, provider bridges
do not understand the standard Ethertype. Hence, they use an Ethertype value that is different from the standard
802.1Q Ethertype value. This difference makes customer traffic that is tagged with the standard Ethertype
appear as untagged in the provider network. The customer traffic is tunneled in the port VLAN of the provider
port. 802.1ad service provider user network interfaces (S-UNIs) and network-network interfaces (NNIs)
implement the S-bridge component.
For example, a VLAN tag has a VLAN ID of 1, the C-tag Ethertype has a value of 8100 0001, the S-tag
Ethertype has a value of 88A8 0001, and the class of service (CoS) has a value of zero.
C-tag S-tag
------------------------------------------------------- --------------------------------------------------
0x8100 | Priority bits | CFI | C-VLAN-ID 0x88A8 | Priority bits | 0 | S-VLAN-ID
------------------------------------------------------- --------------------------------------------------
C-Bridge Component
All customer VLANs (C-VLANs) that enter a user network interface (UNI) port in an S-bridge component
receive the same service (marked with the same S-VLAN). C-VLAN components are not supported, but a
customer may want to tag a particular C-VLAN packet separately to differentiate between services. Provider
bridges allow C-VLAN packet tagging with a provider edge bridge, called the C-bridge component of the
provider bridge. C-bridge components are C-VLAN aware and can insert or remove a C-VLAN 802.1Q tag.
The C-bridge UNI port is capable of identifying the customer 802.1Q tag and inserting or removing an S-tag
on the packet on a per-service instance or C-VLAN basis. A C-VLAN tagged service instance allows service
instance selection and identification by C-VLAN. The 801.1ad customer user network interfaces (C-UNIs)
implement the C-component.
MAC Addresses for Layer 2 Protocols
Layer 2 protocol data units (PDUs) of customers that are received by a provider bridge are not forwarded.
Hence, Layer 2 protocols running at customer sites do not know the complete network topology. By using
different set of addresses for the Layer 2 protocols running on provider bridges, IEEE 802.1ad causes Layer
2 PDUs of the customers device that enter the provider bridge to appear as unknown multicast traffic and
forwards it on customer ports (on the same service provider VLAN (S-VLAN)). Layer 2 protocols of customer
device can then run transparently.
The table below shows Layer 2 MAC addresses that are reserved for the C-VLAN component.
Table 1: Reserved Layer 2 MAC Addresses for the C-VLAN Component
Value
Assignment
01-80-C2-00-00-00
Bridge Group Address
01-80-C2-00-00-01
IEEE 802.3 Full Duplex PAUSE Operation
01-80-C2-00-00-02
IEEE 802.3 Slow\_Protocols\_Multicast\_Address
01-80-C2-00-00-03
IEEE 802.1X PAE Address
Carrier Ethernet Configuration Guide, Cisco IOS XE Release 3E
3
IEEE 802.1ad Support on Provider Bridges
MAC Addresses for Layer 2 Protocols
Value
Assignment
01-80-C2-00-00-08
Provider Bridge Group Address
01-80-C2-00-00-0D
Provider Bridge GVRP Address
01-80-C2-00-00-0E
IEEE 802.1AB Link Layer Discovery Protocol
Multicast Address
01-80-C2-00-00-04
01-80-C2-00-00-05
01-80-C2-00-00-06
01-80-C2-00-00-07
01-80-C2-00-00-09
01-80-C2-00-00-0A
01-80-C2-00-00-0B
01-80-C2-00-00-0C
01-80-C2-00-00-0F
Reserved for future standardization
The table below shows Layer 2 MAC addresses that are reserved for the S-VLAN component. These addresses
are a subset of the C-VLAN component addresses, and the C-bridge does not forward the bridge protocol data
units (BPDUs) of a provider to a customer network.
Table 2: Reserved Layer 2 MAC Addresses for the S-VLAN Component
Value
Assignment
01-80-C2-00-00-01
IEEE 802.3 Full Duplex PAUSE Operation
01-80-C2-00-00-02
IEEE 802.3 Slow\_Protocols\_Multicast\_Address
01-80-C2-00-00-03
IEEE 802.1X PAE Address
01-80-C2-00-00-08
Provider Bridge Group Address
01-80-C2-00-00-04
01-80-C2-00-00-05
01-80-C2-00-00-06
01-80-C2-00-00-07
01-80-C2-00-00-09
01-80-C2-00-00-0A
Reserved for future standardization
Carrier Ethernet Configuration Guide, Cisco IOS XE Release 3E
4
IEEE 802.1ad Support on Provider Bridges
MAC Addresses for Layer 2 Protocols
Overview of IEEE 802.1ad Support on Provider Bridges
The IEEE 802.1ad Support on Provider Bridges feature is implemented on switch ports and supports the
following IEEE 802.1ad specified functions:
• Operation of individual provider bridges
• Configuration and management of individual provider bridges
• Management of spanning tree and VLAN topologies within a provider network
Layer 2 PDU Destination MAC Addresses for Customer-Facing C-Bridge UNI Ports
The table below shows the Layer 2 protocol data unit (PDU) destination MAC addresses for customer-facing
C-bridge user network interface (UNI) ports and how the frames are processed.
Table 3: Layer 2 PDU Destination MAC Addresses for Customer-Facing C-Bridge UNI Ports
Default Action
Significance on the
C-Bridge UNI Port
Protocol
MAC Address
BPDU
Data, BPDU (based on
the CLI configuration of
the l2protocol command)
Bridge Group Address
(end-to-end BPDUs)
01-80-C2-00-00-00
MAC address processes
BPDU
802.3X Pause Protocol
01-80-C2-00-00-01
BPDU
BPDU
Slow protocol address:
802.3ad LACP, 802.3ah
OAM, Cisco Discovery
Protocol, DTP, PagP,
UDLD, VTP
01-80-C2-00-00-02
BPDU
BPDU
802.1x
01-80-C2-00-00-03
Drop
Drop
Reserved for future media
access method
01-80-C2-00-00-04
Drop
Drop
Reserved for future media
access method
01-80-C2-00-00-05
Drop
Drop
Reserved for future bridge
use
01-80-C2-00-00-06
BPDU
BPDU
Ethernet Local
Management Interface
01-80-C2-00-00-07
Drop
Drop
Provider STP (BPDU)
01-80-C2-00-00-08
Carrier Ethernet Configuration Guide, Cisco IOS XE Release 3E
5
IEEE 802.1ad Support on Provider Bridges
Overview of IEEE 802.1ad Support on Provider Bridges
Default Action
Significance on the
C-Bridge UNI Port
Protocol
MAC Address
Drop
Drop
Reserved for future bridge
use
01-80-C2-00-00-09
Drop
Drop
Reserved for future bridge
use
01-80-C2-00-00-0A
Drop
Drop
Reserved for future
S-bridge purposes
01-80-C2-00-00-0B
Drop
Drop
Reserved for future
S-bridge purposes
01-80-C2-00-00-0C
Drop
Drop
Provider bridge GVRP
address
01-80-C2-00-00-0D
BPDU
Data, BPDU (based on
the CLI configuration of
the l2protocol command)
802.1ab LLDP
01-80-C2-00-00-0E
Drop
Drop
Reserved for future C-
bridge or Q-bridge use
01-80-C2-00-00-0F
Peer
BPDU
All bridges address
01-80-C2-00-00-10
Data
Data
GMRP
01-80-C2-00-00-20
Data
Data
GVRP
01-80-C2-00-00-21
Data
Data
Other GARP addresses
01-80-C2-00-00-22-2F
BPDU
Data, BPDU (based on
the CLI configuration of
the l2protocol command)
Cisco Discovery Protocol,
DTP, PagP, UDLD, VTP
(end-to-end)
01-00-0C-CC-CC-CC
BPDU
Data, BPDU (based on
the CLI configuration of
the l2protocol command)
PVST (end-to-end)
01-00-0C-CC-CC-CD
Layer 2 PDU Destination MAC Addresses for Customer-Facing S-Bridge UNI Ports
If a port is operating as a customer-facing S-bridge user network interface (UNI), the destination MAC
addresses shown in the below table are used for defining the Layer 2 protocol protocol data unit (PDU)
processing at the S-bridge UNI.
Carrier Ethernet Configuration Guide, Cisco IOS XE Release 3E
6
IEEE 802.1ad Support on Provider Bridges
Overview of IEEE 802.1ad Support on Provider Bridges
Table 4: Layer 2 PDU Destination MAC Addresses for Customer-Facing S-Bridge UNI Ports
Default Action
Significance on the
S-Bridge UNI Port
Protocol
MAC Address
Data
Data, BPDU (based on
the CLI configuration of
the l2protocol command)
Bridge Protocol Data
Units (BPDUs)
01-80-C2-00-00-00
MAC address processes
BPDU
802.3X Pause Protocol
01-80-C2-00-00-01
BPDU
BPDU
Slow protocol address:
802.3ad LACP, 802.3ah
OAM
01-80-C2-00-00-02
BPDU
BPDU
802.1x
01-80-C2-00-00-03
Drop
Drop
Reserved for future media
access method
01-80-C2-00-00-04
Drop
Drop
Reserved for future media
access method
01-80-C2-00-00-05
Drop
Drop
Reserved for future bridge
use
01-80-C2-00-00-06
BPDU (drop on NNI)
BPDU
Ethernet Local
Management Interface
01-80-C2-00-00-07
BPDU
BPDU
Provider STP (BPDU)
01-80-C2-00-00-08
Drop
Drop
Reserved for future bridge
use
01-80-C2-00-00-09
Drop
Drop
Reserved for future bridge
use
01-80-C2-00-00-0A
Data
Data
Reserved for future
S-bridge use
01-80-C2-00-00-0B
Data
Data
Reserved for future
S-bridge use
01-80-C2-00-00-0C
Data
Data
Provider bridge Generic
VLAN Registration
Protocol (GVRP) address
01-80-C2-00-00-0D
Data
Data, BPDU (based on
the CLI configuration of
the l2protocol command)
802.1ab Link Layer
Discovery Protocol
(LLDP)
01-80-C2-00-00-0E
Carrier Ethernet Configuration Guide, Cisco IOS XE Release 3E
7
IEEE 802.1ad Support on Provider Bridges
Overview of IEEE 802.1ad Support on Provider Bridges
Default Action
Significance on the
S-Bridge UNI Port
Protocol
MAC Address
Data
Data
Reserved for future C-
bridge or Q-bridge use
01-80-C2-00-00-0F
Data
Data
All bridges address
01-80-C2-00-00-10
Data
Data
GARP Multicast
Registration Protocol
(GMRP)
01-80-C2-00-00-20
Data
Data
Generic VLAN
Registration Protocol
(GVRP)
01-80-C2-00-00-21
Data
Data
Other Generic Attribute
Registration Protocol
(GARP) addresses
01-80-C2-00-00-22-2F
Data
Data, BPDU (based on
the CLI configuration of
the l2protocol command)
Cisco Discovery Protocol,
Dynamic Trunking
Protocol (DTP), Port
Aggregation Protocol
(PagP), UniDirectional
Link Detection (UDLD),
and VLAN Trunk
Protocol (VTP)
01-00-0C-CC-CC-CC
Data
Data, BPDU (based on
the CLI configuration of
the l2protocol command)
Per-VLAN Spanning Tree
(PVST)
01-00-0C-CC-CC-CD
How to Configure IEEE 802.1ad Support on Provider Bridges
Configuring a Switch Port to Process 802.1ad BPDUs
In an 802.1ad network, the default behavior for Layer 2 protocol data units (PDUs) on an interface depends
on the 802.1ad interface type. If the interface type is an S-bridge user network interface (UNI), all Layer 2
PDUs are tunneled. If the interface type is a C-bridge UNI, all Layer 2 PDUs are processed (peered).
PDU processing on the S-bridge UNI is the same as on an 802.1ad network-network interface (NNI). Both
types of interfaces have the same scope of MAC addresses. Perform the tasks in this section to configure
switch port-to-peer (process) BPDUs:
Carrier Ethernet Configuration Guide, Cisco IOS XE Release 3E
8
IEEE 802.1ad Support on Provider Bridges
How to Configure IEEE 802.1ad Support on Provider Bridges
Configuring a Switch Port to Process BPDUs
SUMMARY STEPS
1. enable
2. configure terminal
3. interface type number
4. switchport mode {access | trunk}
5. ethernet dot1ad {nni | uni {c-port | s-port}}
6. l2protocol peer [protocol]
7. end
DETAILED STEPS
Purpose
Command or Action
Enables privileged EXEC mode.
enable
Step 1
Example:
Device> enable
• Enter your password if prompted.
Enters global configuration mode.
configure terminal
Example:
Device# configure terminal
Step 2
Configures the interface and enters interface configuration
mode.
interface type number
Example:
Device(config)# interface gigabitethernet 0/3
Step 3
Sets the interface type.
switchport mode {access | trunk}
Example:
Device(config-if)# switchport mode trunk
Step 4
Configures a dot1ad network-network interface (NNI) or
user network interface (UNI) port.
ethernet dot1ad {nni | uni {c-port | s-port}}
Example:
Device(config-if)# ethernet dot1ad uni c-port
Step 5
Processes or forwards Layer 2 bridge protocol data units
(BPDUs).
l2protocol peer [protocol]
Example:
Device(config-if)# l2protocol peer vtp
Step 6
• In this example, only VLAN Trunk Protocol (VTP)
BPDUs are processed.
Carrier Ethernet Configuration Guide, Cisco IOS XE Release 3E
9
IEEE 802.1ad Support on Provider Bridges
Configuring a Switch Port to Process 802.1ad BPDUs
Purpose
Command or Action
Returns to privileged EXEC mode.
end
Example:
Device(config-if)# end
Step 7
Configuration Examples for IEEE 802.1ad Support on Provider
Bridges
Example: Configuring an 802.1ad S-Bridge UNI
The following example shows how to configure GigabitEthernet interface 0/2 of a provider edge (PE) as an
802.1ad S-bridge user network interface (UNI). In this example, only Cisco Discovery Protocol protocol data
units (PDUs) will be forwarded (tunneled). Cisco Discovery Protocol PDUs are forwarded between the PE
and a customer device.
Device# configure terminal
Device(config)# interface GigabitEthernet 0/2
Device(config-if)# switchport access vlan 500
Device(config-if)# ethernet dot1ad uni s-port
Device(config-if)# l2protocol forward cdp
Device(config-if)# end
Example: Configuring an 802.1ad C-Bridge UNI
The following example shows how to configure interface GigabitEthernet 0/3 of a PE as an 802.1ad C-bridge
user network interface (UNI). In this example, only Cisco Discovery Protocol protocol data units (PDUs) are
processed.
Device# configure terminal
Device(config)# interface GigabitEthernet 0/3
Device(config-if)# switchport mode trunk
Device(config-if)# ethernet dot1ad uni c-port
Device(config-if)# l2protocol peer cdp
Device(config-if)# end
Carrier Ethernet Configuration Guide, Cisco IOS XE Release 3E
10
IEEE 802.1ad Support on Provider Bridges
Configuration Examples for IEEE 802.1ad Support on Provider Bridges
Additional References for IEEE 802.1ad Support on Provider
Bridges
Related Documents
Document Title
Related Topic
Cisco IOS Master Command List, All Releases
Cisco IOS commands
Cisco IOS Carrier Ethernet Command Reference
Cisco IOS Carrier Ethernet commands
Standards and RFCs
Title
Standard
Provider Bridges
IEEE 802.1ad
Technical Assistance
Link
Description
http://www.cisco.com/cisco/web/support/index.html
The Cisco Support and Documentation website
provides online resources to download documentation,
software, and tools. Use these resources to install and
configure the software and to troubleshoot and resolve
technical issues with Cisco products and technologies.
Access to most tools on the Cisco Support and
Documentation website requires a Cisco.com user ID
and password.
Feature Information for IEEE 802.1ad Support on Provider Bridges
The following table provides release information about the feature or features described in this module. This
table lists only the software release that introduced support for a given feature in a given software release
train. Unless noted otherwise, subsequent releases of that software release train also support that feature.
Use Cisco Feature Navigator to find information about platform support and Cisco software image support.
To access Cisco Feature Navigator, go to . An account on Cisco.com is not required.
Carrier Ethernet Configuration Guide, Cisco IOS XE Release 3E
11
IEEE 802.1ad Support on Provider Bridges
Additional References for IEEE 802.1ad Support on Provider Bridges
Table 5: Feature Information for IEEE 802.1ad Support on Provider Bridges.
Feature Information
Releases
Feature Name
The IEEE 802.1ad Support on
Provider Bridges feature is the
IEEE 802.1ad implementation on
Cisco devices using Layer 2 switch
ports.
In Cisco IOS XE Release 3.6E, this
feature is supported on Cisco
Catalyst 3850 Series Switches.
The following commands were
introduced or modified: ethernet
dot1ad, l2protocol, and show
ethernet dot1ad.
Cisco IOS XE Release 3.6E
IEEE 802.1ad Support on Provider
Bridges
Glossary
DTP—Dynamic Trunking Protocol.
GARP—Generic Attribute Registration Protocol.
GMRP—GARP Multicast Registration Protocol.
GVRP—Generic VLAN Registration Protocol.
LLDP—Link Layer Discovery Protocol.
OAM—Operations, Administration, and Maintenance.
PagP—Port Aggregation Protocol.
PVST—Per-VLAN Spanning Tree.
UDLD—UniDirectional Link Detection.
VTP—VLAN Trunk Protocol.
Carrier Ethernet Configuration Guide, Cisco IOS XE Release 3E
12
IEEE 802.1ad Support on Provider Bridges
Glossary