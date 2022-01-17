
#  Polyglot v3 node server OpenSprinkler Copyright (C) 2021 Javier Refuerzo

A simple node server gets data from open sprinkler at every short poll interval.

## Installation
PG3 Node Server Store

### Node Settings
The settings for this node are:

#### Short Poll
   * How often to get data from open sprinkler. Default is 5 seconds, the same as OpenSprinkler Apps
#### Long Poll
   * Not used

#### password
   * OpenSprinkler password. This will be converted to MD5 before transmittion

#### ipAddress
   * The static local IP Address of Open Sprinkler


## Requirements

1. Polyglot V3.
2. ISY firmware 5.3.x or later

# Release Notes

- 1.0.0 01/11/2021
   - Initial version published to github
