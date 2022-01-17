
#  Polyglot v3 node server OpenSprinkler Copyright (C) 2021 Javier Refuerzo

A simple node server gets data from open sprinkler at every short poll interval.

## Installation
PG3 Node Server Store
Please reboot ISY before synchronization with UD Moble or human readable values may be shown as numbers. 

## Help
https://forum.universal-devices.com/forum/323-opensprinkler/

### Node Settings
The settings for this node Short Poll, password, url, and manualRunTimeSeconds. All defined below. With the exception of Short Poll all items are set in custom params.

#### Short Poll
   * How often to get data from open sprinkler. Default is 5 seconds, the same as OpenSprinkler Apps. changing this to a lower value may cause communication issues. changing to a higher value will delay status updats to ISY.

#### Long Poll
   * Not used

#### password
   * OpenSprinkler password. This will be converted to MD5 before transmittion

#### url
   * The local IP Address of Open Sprinkler, this should be fully qualified starting with "http://". OpenSprinkler does not broadcast its location so the address should be reserved in the users router.

#### manualRunTimeSeconds
   * The default runtime when an OpenSprinkler station is triggered manually. This can be changed in ISY but will reset on Polisy restart/reboot.

## Requirements

1. Polyglot V3.
2. ISY firmware 5.3.x or later
3. Opensprinkler firmware 2.1.9 (2019) or later. Please be sure to backup open sprinkler before upgrading firmware as you settings will be removed! https://openthings.freshdesk.com/support/home see User Manuals and select your hardware 3.x or 2.x

## Known Issues and limitations

1. Please allow upto one minuite after credentials and URL are saved before opeining the Admin consloe as it may take time to populate sprinkler Station and Program Nodes.
2. OpenSprinkler idetifies Stations and Programs by index, so moving a program up or down from the OpenSprinkler Web or App interface will cause the Node Server to trigger the wrong program. If this is done please rename nodes in ISY or move back to previous position.
3. When manually triggering a progarm from ISY it will not show as "Running". This is because OpenSprinkler assigns manually triggered programs to is 254 which is out of range of available programs.  The Node Server will still show as running in both the Parent Station Node ("Stations Queued") and the Main Parent Node ("Running Program")

# Release Notes

- 2022.1.16 01/16/2022
   - Initial version published to github
