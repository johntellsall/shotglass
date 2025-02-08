# First, install the required tools if you haven't already
apk add alpine-sdk doas

# Create and enter a directory for the source
mkdir -p ~/aports
cd ~/aports

# Clone the aports repository if you haven't already
git clone https://gitlab.alpinelinux.org/alpine/aports.git
cd aports

# Navigate to the Dnsmasq package directory
cd main/dnsmasq

# Fetch the source
abuild fetch