# language-agnostic complexity

* https://github.com/thoughtbot/complexity

# Rendering with Bokeh
- Use "color bars" in Bokeh to do 2D color render
https://bokeh.pydata.org/en/latest/docs/user_guide/annotations.html#color-bars

- "box annotations" to colorize different directories https://bokeh.pydata.org/en/latest/docs/user_guide/annotations.html#box-annotations
    - or spans https://bokeh.pydata.org/en/latest/docs/user_guide/annotations.html#spans

- labels https://bokeh.pydata.org/en/latest/docs/user_guide/annotations.html#labels


# Linux Kernel Source
```
git clone git://git.kernel.org/pub/scm/linux/kernel/git/stable/linux-stable.git
 1557  cd linux-stable/
git checkout v3.0
```
XX doesn't have v2.0 and before


## Needs Upgrading

Following files are Python 2!

make_ver_iproute2.py
make_ver_ansible.py
make_versions.py
app/grid.py
app/management/commands/age.py
app/management/commands/evolve.py
app/management/commands/callscan.py
app/management/commands/label.py
app/management/commands/adjust_index.py
app/management/commands/make_versions.py
app/management/commands/make_ver_postgres.py
app/management/commands/spark.py
app/management/commands/pygdex.py
app/management/commands/sizeplot.py
app/management/commands/words.py
app/management/commands/funcsize.py
app/management/commands/bokplot.py
app/management/commands/draw.py
