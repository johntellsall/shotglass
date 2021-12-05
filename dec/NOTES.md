# NOTES

## number of symbols per file

    select path from files
    inner join symbols on symbols.file_id = files.id
    limit 3;

## visualization docs

* https://pandas.pydata.org/pandas-docs/version/0.18.1/visualization.html#visualization-hist
* 
