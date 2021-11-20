# NOTES

## number of symbols per file

    select path from files
    inner join symbols on symbols.file_id = files.id
    limit 3;
