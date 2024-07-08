# pygeofilter-duckdb

This is an extension for [pygeofilter](https://github.com/geopython/pygeofilter) to support SQL queries in DuckDB based on Geoparquet files. 

pygeofilter allows to parse several filter encoding standards (e.g., CQL JSON, CQL Text) and to convert them to queries for several backends (e.g., SQL, Django, Pandas). 

In DuckDB the geometry is currently stored as BLOB, which needs to be considered in the filter conversion. This extension is based on the following issue: https://github.com/geopython/pygeofilter/issues/90. 

## Usage

```python
from pygeofilter.parsers.cql2_json import parse as json_parse
from pygeofilter.backends.duckdb import to_sql_where
from pygeofilter.util import IdempotentDict

start = '2023-02-01T00:00:00Z'
end = '2023-02-28T23:59:59Z'

cql2_filter = {
  "op": "and",
  "args": [
    {
      "op": "between",
      "args": [
        {
          "property": "eo:cloud_cover"
        },
        [0, 21]
      ]
    },
      {
      "op": "between",
      "args": [
        {
          "property": "datetime"
        },
        [start, end]
      ]
    },
    {
        "op": "s_intersects",
        "args": [
          { "property": "geometry" } ,
          {
            "type": "Polygon", # Baden-Württemberg
            "coordinates": [[
                [7.5113934084, 47.5338000528],
    			[10.4918239143, 47.5338000528],
    			[10.4918239143, 49.7913749328],
    			[7.5113934084, 49.7913749328],
    			[7.5113934084, 47.5338000528]
            ]]
          }
        ]
      }
  ]
}

sql_where = to_sql_where(json_parse(cql2_filter), IdempotentDict())
print(sql_where)
```

This results in the following output

```
((("eo:cloud_cover" BETWEEN 0 AND 21) AND ("datetime" BETWEEN '2023-02-01T00:00:00Z' AND '2023-02-28T23:59:59Z')) AND ST_Intersects(ST_GeomFromWKB(geometry),ST_GeomFromHEXEWKB('0103000000010000000500000034DFB1B6AA0B1E4085B0648F53C44740509E1658D0FB244085B0648F53C44740509E1658D0FB244006A017C64BE5484034DFB1B6AA0B1E4006A017C64BE5484034DFB1B6AA0B1E4085B0648F53C44740')))
```
