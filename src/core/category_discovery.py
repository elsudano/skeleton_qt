"""Automatic discovery of logging categories from source code."""

import ast
from pathlib import Path


class CategoryDiscovery:
    """Discover logging categories automatically from Python source files."""
    
    @staticmethod
    def discover_from_source(src_path: str = "src") -> list[str]:
        """
        Discover automatically all the categories in the source code.
        
        Parameters
        ----------
        src_path : str
            Path to the source directory to scan for categories.
            
        Returns
        -------
        List[str]
            List of discovered category names.
        """
        categories = set()
        
        # Recorrer todos los archivos Python
        for py_file in Path(src_path).rglob("*.py"):
            if py_file.is_file() and "_CATEGORY" in py_file.read_text():
                try:
                    # Usar AST para análisis más seguro que regex
                    with open(py_file, encoding='utf-8') as f:
                        content = f.read()
                        
                    tree = ast.parse(content)
                    
                    # Buscar asignaciones de _CATEGORY
                    for node in ast.walk(tree):
                        if (isinstance(node, ast.Assign) and 
                            len(node.targets) == 1 and
                            isinstance(node.targets[0], ast.Name) and
                            node.targets[0].id == '_CATEGORY'):
                            
                            if isinstance(node.value, ast.Constant):
                                categories.add(node.value.value)
                            elif hasattr(node.value, 's'):  # Para versiones antiguas de Python
                                categories.add(node.value.s)
                except Exception as e:
                    print(f"Error analyzing {py_file}: {e}")
        
        return sorted(list(categories))