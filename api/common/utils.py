# api/common/utils.py
import string

def cap(value):
    """
    Capitaliza la primera letra de cada palabra.
    'juan perez' → 'Juan Perez'
    Preserva mayúsculas ya existentes (no lowercasea todo).
    """
    if not value or not isinstance(value, str):
        return value
    return string.capwords(value.strip())

def cap_sentence(value):
    """
    Capitaliza sólo la primera letra de la oración (para notas/descripciones).
    'diagnóstico: tda' → 'Diagnóstico: tda'
    """
    if not value or not isinstance(value, str):
        return value
    v = value.strip()
    return v[0].upper() + v[1:] if v else v
