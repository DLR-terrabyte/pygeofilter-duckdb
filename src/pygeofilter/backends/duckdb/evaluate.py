from typing import Dict, Optional

import shapely.geometry

from ... import ast, values
from ..evaluator import handle
from ..sql.evaluate import SQLEvaluator

class DuckDBEvaluator(SQLEvaluator):
    @handle(ast.Attribute)
    def attribute(self, node: ast.Attribute):
        if node.name == "geometry":
            return f'ST_GeomFromWKB({node.name})'
        return f'"{self.attribute_map[node.name]}"'

    @handle(values.Geometry)
    def geometry(self, node: values.Geometry):
        wkb_hex = shapely.geometry.shape(node).wkb_hex
        return f"ST_GeomFromHEXEWKB('{wkb_hex}')"

    @handle(values.Envelope)
    def envelope(self, node: values.Envelope):
        wkb_hex = shapely.geometry.box(node.x1, node.y1, node.x2, node.y2).wkb_hex
        return f"ST_GeomFromHEXEWKB('{wkb_hex}')"


def to_sql_where(
    root: ast.Node,
    field_mapping: Dict[str, str],
    function_map: Optional[Dict[str, str]] = None,
) -> str:
    return DuckDBEvaluator(field_mapping, function_map or {}).evaluate(root)
