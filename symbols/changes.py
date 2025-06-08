# changes.py -- show file changes over time
# - Dnsmasq, 20 samples over 90 releases

PROJ = '../SOURCE/dnsmasq'

import run

def main():
    tags = run.git_tag_list(PROJ)
    print(tags)

if __name__ == '__main__':
    main()