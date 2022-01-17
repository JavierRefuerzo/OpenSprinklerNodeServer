
#  Polyglot v3 node server OpenSprinkler Copyright (C) 2021 Javier Refuerzo

A simple node server gets data from open sprinkler at every short poll interval.

## Installation
PG3 Node Server Store
Please reboot ISY before synchronization with UD Moble or human readable values may be shown as numbers

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
3. Opensprinkler firmware 2.1.9 (2019) or later. Please be sure to backup open sprinkler before upgrading firmware as you settings will be removed! https://openthings.freshdesk.com/support/home see User Manuals and select your hardware 3.x or 2.x'

# Release Notes

- 2022.1.16 01/16/2021
   - Initial version published to github
