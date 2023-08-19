# Package Release Rates

XXXXXX REWRITE
- number are from Alpine packages *available*, not necessarily included in default image
- list packages *used* in image
- who cares about release rates?

## XX
- reasons why the releases look like this?
- release notes? Why is ruby-bundler released so often?

## totals

Alpine Linux has XX 1600 packages, of which XX 250 are in GitHub.
XX of those have Releases
XX more than five releases
XX TBD


## frequent releases -- under two weeks average

In startup land, deployments are every 2-4 weeks, with pressure to release faster. A release is expected to be meaningful to users, so often it is delayed for a cycle to allow more features to accumulate before a production deployment is made.

Another model is Kanban, where production deployments are much smaller but more frequent. It appears no Alpine packages follow this model, which is surprising.

The only package to release weekly is `ruby-bundler`.

    package	        first_release	latest_release		num_releases	days_per_release
        
    protobuf            	2019-10-24	2023-08-01	100	13	biweekly
    pspg                	2019-07-24	2023-08-02	100	14	biweekly
    ruby-bundler        	2021-11-08	2023-08-02	100	6	biweekly

## monthly

A lot of languages release monthly or faster (often 18 days). `clang16` is C, `cython` is a Python compiler for extentions, and `llvm16` is a common language backend. `harfbuzz` is an amazingly-named common text formatter. `hwdata` contains data files to help Linux get devices detected and run correctly. `dhcpcd` allows a computer to setup networking correctly. `icu` is for Unicode support.

It's not clear why some language-level libraries are distributed as system packages. Probably they have C extensions or other binaries, or are used by many other system-level packages.

`ghi` is for interacting with GitHub Issues. Perhaps the Alpine developers use this internally, or maybe Alpine is able to create an Issue when a package crashes unexpectedly.

    clang14             	2019-04-11	2023-07-29	87	18	monthly
    clang15             	2019-04-11	2023-07-29	87	18	monthly
    clang16             	2019-04-11	2023-07-29	87	18	monthly
    cython              	2021-12-06	2023-07-17	20	29	monthly
    dhcpcd              	2023-04-13	2023-07-19	6	16	monthly
    ghi                 	2015-10-16	2016-04-20	8	23	monthly
    harfbuzz            	2017-01-05	2023-08-02	100	24	monthly
    hwdata              	2017-03-06	2023-08-03	80	29	monthly
    icu                 	2016-11-01	2023-07-20	99	24	monthly
    libclc              	2019-04-11	2023-07-29	87	18	monthly
    libpaper            	2022-05-10	2023-06-30	20	20	monthly
    lld                 	2019-04-11	2023-07-29	87	18	monthly
    llvm-runtimes       	2019-04-11	2023-07-29	87	18	monthly
    llvm14              	2019-04-11	2023-07-29	87	18	monthly
    llvm15              	2019-04-11	2023-07-29	87	18	monthly
    llvm16              	2019-04-11	2023-07-29	87	18	monthly
    meson               	2017-08-14	2023-07-16	100	21	monthly
    nvme-cli            	2022-01-14	2023-06-30	19	27	monthly
    py3-sphinx          	2021-11-27	2023-08-02	30	20	monthly
    py3-xmlschema       	2018-09-27	2023-07-27	60	29	monthly
    ruby-rbs            	2022-06-22	2023-07-31	21	19	monthly
    scudo-malloc        	2019-04-11	2023-07-29	87	18	monthly
    wasi-compiler-rt    	2019-04-11	2023-07-29	87	18	monthly

## quarterly

`conky` is a light-weight system monitor. `elinks` is a text-mode browser. I'm surprised these are in the base Alpine distribution. Elinks is tiny and can be used directly, or bootstrap a real browser, so it's good for emergencies.
`s390-tools` is for working with IBM IBM System/390 mainframes. I'm surprised it changes quarterly :) Why is this in the base Alpine distro: are its functions re-used in other tools, or is it useful to have mainframe support in the base distribution?
`cups fuse ghostscript glslang mbedtls strace syslog-ng zfs` and others are system-level tools. They support printers, networking, filesystems, monitoring, and filesystems.
`nghttp2` is a limited-use web server, probably for an admin use in exporting data vs running apps.

    abseil-cpp          	2020-02-25	2023-08-02	21	59	quarterly
    apache2-mod-wsgi    	2014-05-21	2022-09-12	83	36	quarterly
    asciidoc            	2019-11-29	2022-05-22	20	45	quarterly
    atf                 	2012-02-26	2014-10-23	21	46	quarterly
    cjson               	2016-11-11	2023-07-05	46	52	quarterly
    conky               	2015-05-23	2023-05-16	33	88	quarterly
    cups                	2020-11-27	2023-06-22	11	85	quarterly
    docbook-xsl         	2016-11-03	2020-06-03	20	65	quarterly
    elinks              	2019-12-27	2023-05-01	20	61	quarterly
    fmt                 	2014-04-15	2023-05-09	42	78	quarterly
    fuse                	2015-05-22	2023-07-05	49	60	quarterly
    fuse3               	2015-05-22	2023-07-05	49	60	quarterly
    gc                  	2011-12-20	2023-05-26	51	81	quarterly
    ghostscript         	2016-01-26	2023-06-21	51	52	quarterly
    glslang             	2016-08-23	2023-08-02	35	72	quarterly
    haveged             	2018-07-18	2022-04-09	17	80	quarterly
    inotify-tools       	2020-12-01	2022-06-07	13	42	quarterly
    intel-ucode         	2019-09-18	2023-06-13	21	64	quarterly
    jbig2dec            	2016-01-26	2023-06-21	51	52	quarterly
    lcms2               	2020-05-17	2023-02-28	14	72	quarterly
    libavif             	2020-03-30	2022-10-20	19	49	quarterly
    libbpf              	2019-05-23	2023-07-11	23	65	quarterly
    libeconf            	2019-09-03	2023-03-24	22	59	quarterly
    libnvme             	2022-01-14	2023-06-30	16	33	quarterly
    libsodium           	2013-01-22	2019-05-30	32	72	quarterly
    libva               	2017-03-06	2023-07-04	40	57	quarterly
    mbedtls             	2018-07-26	2023-08-03	56	32	quarterly
    musl-fts            	2015-09-01	2017-01-13	8	62	quarterly
    nghttp2             	2015-01-06	2023-07-14	100	31	quarterly
    oniguruma           	2015-09-06	2022-04-15	42	57	quarterly
    py3-cairo           	2017-04-06	2023-06-19	57	39	quarterly
    py3-elementpath     	2018-09-01	2023-07-25	52	34	quarterly
    py3-mimeparse       	2016-05-02	2016-10-16	5	33	quarterly
    py3-more-itertools  	2017-01-07	2023-08-03	41	58	quarterly
    py3-urllib3         	2019-04-22	2023-07-19	38	40	quarterly
    rdiff-backup        	2020-03-15	2023-07-27	18	68	quarterly
    ruby-debug          	2021-12-17	2023-05-09	10	50	quarterly
    ruby-net-imap       	2020-03-26	2023-07-26	14	86	quarterly
    ruby-rake           	2007-04-21	2021-07-09	76	68	quarterly
    ruby-test-unit      	2022-12-14	2023-06-24	6	31	quarterly
    s390-tools          	2017-08-21	2023-08-04	32	67	quarterly
    sofia-sip           	2020-10-27	2023-07-13	14	70	quarterly
    strace              	2016-12-14	2023-06-26	37	64	quarterly
    syslog-ng           	2014-06-06	2023-07-28	65	51	quarterly
    zfs                 	2013-03-26	2023-07-27	91	41	quarterly
    zfs-lts             	2013-03-26	2023-07-27	91	41	quarterly
    zfs-rpi             	2013-03-26	2023-07-27	91	41	quarterly
    zstd                	2015-08-24	2023-04-05	66	42	quarterly

### inactive (releases take more than a year)

These packages don't get updates except every **year** or more.

`bwm-ng` (show bandwidth) and `distcc` (distributed C compiler) I guess are harmless. `dosfstools` is useful on  rare occasions, like extracting firmware updates maybe. `mt-st` is odd: it supports magnetic tapes? Proxies (`rtpproxy tinyproxy`) are nice to have and probably don't have enough features to warrant many updates.

From the inclusion of the above packages in the "minimal" Alpine distro, we can assume it's intended to support disaster recovery and other emergency situations. I thought Alpine was mostly used for Docker-type containers in the cloud, but perhaps it's also used for bare-metal installations where the above packages would be handy.

XX describe container vs VM use cases
XX what's bare metal?

Special note: `jq`. Unlike all of the above-mentioned packages, this is a **very** commonly used Developer-level tool for picking out data from the XX universally-used JSON format. How can this package be only released every year or more? Probably it's reached a stable state, where the complexity of adding a new feature would not compensate for the potential confusion.


    bwm-ng              	2005-02-20	2021-01-10	5	1160	INACTIVE
    distcc              	2008-06-10	2021-05-11	12	393	INACTIVE
    dosfstools          	2014-11-12	2021-01-31	5	454	INACTIVE
    jq                  	2012-10-21	2023-07-30	10	393	INACTIVE
    libconfig           	2015-12-31	2021-06-20	5	399	INACTIVE
    libnet              	2009-05-12	2019-10-16	7	544	INACTIVE
    libusb-compat       	2015-10-09	2022-11-18	6	432	INACTIVE
    lua-expat           	2011-06-03	2022-08-26	5	820	INACTIVE
    lua-soap            	2013-08-21	2020-06-23	5	499	INACTIVE
    lua-unit            	2014-10-09	2021-03-03	6	389	INACTIVE
    mt-st               	2016-02-07	2023-04-20	6	438	INACTIVE
    musl-obstack        	2015-09-10	2022-03-28	6	398	INACTIVE
    rtpproxy            	2014-06-17	2023-07-18	6	552	INACTIVE
    tinyproxy           	2014-12-13	2022-05-27	5	544	INACTIVE

## Conclusion and Next Steps

Based on the above analysis, the Alpine distro is aimed at running minimal app containers locally or in the cloud, but also supports standalone and disaster usages as well. It contains support for the most common languages (C, Lua, Python, Ruby). It has printer support using CUPS. It also contains a number of admin-only tools helpful for data extraction or system recovery.

For strictly cloud use, the following changes are possible:
- remove printer support
  - Printer drivers change often, are chunky (100 MB+), and are never needed for a cloud container
- examine admin support
  - In a cloud container, do we need mainframe or disaster support? A terminal web browser?
  - Secure containers often remove even essential human-focused tools like Bash
- examine app usage
  - Which packages does our app need, now and in the future?
  - What packages are potentially useful (dev debugging) or present security concerns (same)
- discuss complexity
  - It's very easy to fire up a new standard Alpine container. A new one comes out every six months. Does the business get a return on investment if it has its own distro, even if it's "cheaper" by a few MB or hundreds of files?
  - Alpine's goals are [Simple, Small, and Secure](https://www.alpinelinux.org/about/). Does the business get a ROI by removing packages (creating its own distro), or adding a few packages (less risky)

Note this article is based on GitHub Releases from packages included in Alpine. This only accounts for 180 of over 1500 packages in full Alpine.

Another common minimal container image is Debian Slim. It would be interesting to do a similar comparison using that distribution.

## REFERENCE

Typical SQL:

    -- Packages tagged by Release Frequency
    .headers on
    .mode tabs
    
    with BLOB as (
        select
            printf('%-20s', package) as package,
            strftime('%Y-%m-%d', min(release_created_at)) as first_release,
            strftime('%Y-%m-%d', max(release_created_at)) as latest_release,
            count(*) as num_releases,

            cast(
            julianday(max(release_created_at)) - julianday(min(release_created_at))
            as integer) / count(*) as days_per_release
        from github_releases
        group by package
        having num_releases >= 5
    )
    select *,
    case when days_per_release <= 14 then 'biweekly'
    when days_per_release <= 30 then 'monthly'
    when days_per_release <= 90 then 'quarterly'
    when days_per_release <= 180 then 'semiannual'
    when days_per_release <= 365 then 'annual'
    else 'INACTIVE' end as release_frequency 
    from BLOB;
