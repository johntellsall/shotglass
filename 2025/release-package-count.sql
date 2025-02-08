-- CREATE TABLE sgalpinepackage (
--         id INTEGER NOT NULL, 
--         alpine_release VARCHAR NOT NULL, 
--         pkgname VARCHAR NOT NULL, 
--         pkgdesc VARCHAR NOT NULL, 
--         pkgver VARCHAR NOT NULL, 
--         pkgrel VARCHAR NOT NULL, 
--         sg_complexity INTEGER, 
--         sg_len_install INTEGER, 
--         sg_len_parse_funcs INTEGER, 
--         sg_len_subpackages INTEGER, 
--         PRIMARY KEY (id)
-- );

SELECT alpine_release, COUNT(*) AS package_count
FROM sgalpinepackage
GROUP BY alpine_release;