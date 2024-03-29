# Shotglass

## WHY

Shotglass is an experimental platform for letting humans
visually analyze large codebases over time.

Computers are useful, but they can only answer questions. The goal of this project is to render source code visually, and let a human brain interpret the results.

Computers answer "what" and "when" but never "why".

## Example: Packages Release Faster over Time

    Warning: this is a prelimiary result [August 2023],
    data and code needs to be checked.

Recently we scanned _an entire Linux distro_ for package data.
Specifically, the minimal [Alpine distribution](https://www.alpinelinux.org/), often used for containers.

Result: packages tend to release faster over time.

That is, across ~250 of 1600 packages in Alpine Linux, the number of monthly updates goes **up 8x** from ~10 to ~80 releases per month.

Alternate explanations:
- bugs in data or plotting layers
- packages take a while to enable GitHub Releases
- packages exist for a while, then have more official Releases when they're added to Linux distros, like Alpine or others
- new packages are created later, then added to Alpine

![Alpine GitHub Releases](alpine/images/github_releases-2.png)


## Example: Flask: hires rendering of codebase at present

Shotglass displays information about all source files in a large
project. For each file, it renders a single dot per line of code. 

Overall workflow:

- get source tree
- store symbols in database index for quick processing

```
    $ apt source python-flask
    $ mv flask-0.10.1 flask
    $ ./manage.py make_index flask

    $ ./manage.py show flask
    project              symbols   max  avg    total
    flask                    463   196    9    4,208

    $ ./manage.py render flask
    $ firefox flask_path.png
```


![Flask](images/flask_path.png)


### Compare: Django = 12x Flask

Django's larger than Flask, so it's a good point of comparison.

```
    $ apt source python-django

    $ ./manage.py make_index django
    19:01:46,708 DEBUG    finding source
    19:01:46,791 DEBUG    finding tags
    19:01:49,622 INFO     django: 6,049 tags
    19:01:49,622 DEBUG    calculating file sizes
    19:01:53,366 DEBUG    done

    $ ./manage.py show django
    project              symbols   max  avg    total
    django                 6,049   335    7   48,326

    $ ./manage.py render django
```

![Django](images/django_path.png)


## Example: Flask: important files over time


The `table` command shows how important files change over time. It scans through a Git repo, counting lines on important files.

```bash
./manage.py table --versions=0.6,0.8,0.10,0.12 ../SOURCE/flask/

                                0.6  0.8 0.10 0.12
flask/__init__.py                34   41   50   49
flask/__main__.py                               15
flask/_compat.py                           73   96
flask/app.py                    874 1518 1842 2000
flask/blueprints.py                  321  401  413
flask/cli.py                                   511
flask/config.py                 152  169  168  263
flask/ctx.py                     66  175  394  410
flask/debughelpers.py                 79   87  155
flask/ext/__init__.py                 29   29   29
flask/exthook.py                     119  120  143
flask/globals.py                 20   28   44   61
flask/helpers.py                463  649  849  960
flask/json.py                             228  269
flask/logging.py                 42   43   45   94
flask/sessions.py                    205  327  366
flask/signals.py                 50   51   55   56
flask/templating.py              96  138  143  149
flask/testing.py                 45  118  124  143
flask/views.py                       151  149  149
flask/wrappers.py                88  138  184  205
setup.py                         79  108  112  100
```

From the above, we can see:
- `app.py` has the vast majority of the code.
- `cli.py` appeared recently, with a moderate amount of code.
- `config.py`, `helpers.py` and others have existed for a while, and have gradually increased in size to roughly double.
- `signals.py` is old and hasn't really changed.

The `table` command lists files in the latest version, then tracks those files back in time. It doesn't visualize large files splitting into pieces.

### Questions

- what dates correspond to the listed versions?
- even if a file has the same line count, its contents can change over time -- `git diff` will show this.
- the column widths can easily become hard to read

Related: [redis-table.md](Redis codebase over time)

# Code over Time

An important consideration is analyzing how code changes over time. For each release, how has the code changed? Many small patches implies code fixes. If a new big feature was merged in it will appear as a big spike in one file, with smaller patches in other files.  A security release will have a couple patches in a couple files.

Here are the changes for manpages in the "iproute2" (aka "ip", the successor to "route").  A few things to note:

- each release notes how many total changes there were
- there's one char per manpage, showing num of patches
- space = no changes, "." = 1-9 changes, -=10-99, +=100+, *=1000+

For this specific project, iproute2:

- v3.2 brought substantial changes to 8 manpages
- the next release modifies those exact 8 manpages a bit
- 3.8 and 3.10 have many small changes, mostly grammatical
- 4.0, as befitting a major release, makes minor tweaks to nearly every manpage. Examination shows minor changes (changing from two to one space after a sentence), and a number of additions.
- 3.5.1 and 3.14.1 have very few changes, and none on the manpages. These were probably important bugfix/security releases. This makes sense considering these two are the only "point" (x.y.Z) versions.
- 3.2 has a rare 2,700 line change, shown here with "*".  Looking it more closesly shows the ip.8 manpage was split into many sub-manpages, like ip-link.8 and ip-route.8.  ("git diff --stat v3.1.0..v3.2.0 man/man8")
- there's a vertical line of small changes in the 10th file.  This makes sense, as it's the "ip-link.8.in" file, which has references to all the other manpages.
```
57 manpages
v3.1.0 :  15     +                                        -        + .
v3.2.0 :  73            -    ---+ -+ +  ++*                 +    +   .
v3.3.0 :  60     .  .   .    .... .. .  ..-                 -   - +   
v3.4.0 :  61 --    -  .+   ++       +     . ..  .    -       .        
v3.5.0 :  43      .. +                            .   +. +  .  .     +
v3.5.1 :   4       .                                                  
v3.6.0 :  45       - -      -       -     -      .   . .+            +
v3.7.0 :  52     . .       --     .   +   .                           
v3.8.0 : 131 - .-+ .--  -   ----.-- ..  - -             .            .
v3.9.0 :  55        .+ .   -.           .+-        ..   ..          --
v3.10.0:  52       . -      --  - - -- ----.     .      -          -  
v3.11.0:  36                -       -                                 
v3.12.0:  41         -      +        -  .  .  -                       
v3.14.0:  81       .        -   -                -         +  +      .
v3.14.1:   1                                                          
v3.15.0:  46         -      -                                  .    - 
v3.16.0:  30                -          -                              
v3.17.0:  50                -                                         
v3.18.0:  83             -. - -   .      ..                           
v3.19.0:  56         - -    -     - -     -      -                   -
v4.0.0 :  79       ..- -.  .+.... - --  . -    . . ....- .. . . .-. .-
```


## More Demos

* [Web frameworks](web-frameworks.md) from 4 - 60 KLOC
* [Databases](databases.md) from 1x to 20x
* Codebases over time: [Django framework, Python language](code-over-time.md)
* Shotglass [features](features.md)

## Related Projects

* [A Repository with 44 Years of Unix Evolution](https://www2.dmst.aueb.gr/dds/pubs/conf/2015-MSR-Unix-History/html/Spi15c.html)

* [tool that creates pretty visualisations of codebases](https://www.codeatlas.dev)

## Related Articles

* [Ask HN: Visualizing software designs, especially of large systems](https://news.ycombinator.com/item?id=31569646)

## Also

* [Ilograph: render service dependencies](https://app.ilograph.com/demo.ilograph.Ilograph/Request)
