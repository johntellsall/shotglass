# GOAL

Show packages changes between major Debian releases.
Example: core (100-ish) packages, release 13 "Trixie" vs 12 "Bookworm"

## NOTES

    Priority: essential or Priority: important, which together number around 100-110 packages in a standard minimal system. 

* list installed

    For a comprehensive list of all installed packages, you can use dpkg-query: 

    dpkg-query -f '${binary:Package}\n' -W

* installed essential

    dpkg-query -Wf '${Package} ${Essential} ${installed-size}\n' | awk '$2=="yes" {print $1}'

~ 23 packages; XX why not 100?

* package sizes

installed size

smallest
* hostname=46 KB
* sysvinit-utils=100 KB

largest
* coreutils 18062 KB

also
* bash 7164 KB
