import pytest
from pygeofilter.parsers.cql2_json import parse as json_parse
from pygeofilter.backends.duckdb import to_sql_where
from pygeofilter.util import IdempotentDict

def test_duckdb():
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
              "type": "Polygon",
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

    assert sql_where == '((("eo:cloud_cover" BETWEEN 0 AND 21) AND ("datetime" BETWEEN \'2023-02-01T00:00:00Z\' AND \'2023-02-28T23:59:59Z\')) AND ST_Intersects(ST_GeomFromWKB(geometry),ST_GeomFromHEXEWKB(\'0103000000010000000500000034DFB1B6AA0B1E4085B0648F53C44740509E1658D0FB244085B0648F53C44740509E1658D0FB244006A017C64BE5484034DFB1B6AA0B1E4006A017C64BE5484034DFB1B6AA0B1E4085B0648F53C44740\')))'
