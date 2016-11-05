#Usage
Use this script for update a managed domain name by Gandi with your current external ip address.

#Use outside docker container
This script is made to update a gandi domain zone record with your current external ip from where the script is executed.

To work the script need the following variables define in environment or in single line file at the classpath root:
* API_KEY: Gandi api key in environment variable (or in a file api_key). This is required.
* API_URL: Gandi api url in environment variable (or in a file api_url). This is not required (by default, production url).
* RECORD: zone record to update in environment variable (or in a file record). This is required.
* ZONE: zone name in environment variable (or in a file zone). This is required.

For exemple to have the dns name alpha.betha.com to reference your ip, you need an existing Gandi account on the betha.com zone. Then the zone is 'betha.com.' (do not forget the remaining dot) and the record is 'alpha'.

#Use docker container 
Just define API_KEY, RECORD and ZONE environment variable as described earlier. Docker container is configured to executed update every 1800 seconds (12 hours).
Available on docker hub at https://hub.docker.com/r/jdfischer/gandi-dynamic-dns/.
 