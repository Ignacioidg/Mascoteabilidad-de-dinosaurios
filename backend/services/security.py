# -*- coding: utf-8 -*-
"""
Módulo de Seguridad y Hashing de Contraseñas
DinoMascota Dashboard - Bases de Datos Aplicada (UAI)

Implementa:
- Hashing SHA-256 con Salt criptográfico individual (secrets.token_hex)
- Formato de almacenamiento: sha256$<salt>$<hash_hex>
- Compatibilidad retroactiva con hashes Bcrypt existentes ($2b$...)
"""

import hashlib
import secrets
from typing import Tuple, Optional
import bcrypt

def generate_salt(length: int = 16) -> str:
    """Genera un salt criptográfico seguro en formato hexadecimal."""
    return secrets.token_hex(length)

def hash_password_sha256(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
    """
    Hashea una contraseña usando SHA-256 con salt.
    Retorna: (hash_completo, salt)
    El hash_completo tiene el formato 'sha256$<salt>$<hash_hex>'
    """
    if not salt:
        salt = generate_salt()
    
    # Combinar salt + password y calcular digest SHA-256
    raw = (salt + password).encode('utf-8')
    digest = hashlib.sha256(raw).hexdigest()
    formatted_hash = f"sha256${salt}${digest}"
    return formatted_hash, salt

def verify_password(plain_password: str, stored_hash: str, salt: Optional[str] = None) -> bool:
    """
    Verifica una contraseña en texto plano contra el hash almacenado.
    Soporta:
    1. Formato SHA-256 con salt ('sha256$<salt>$<hash_hex>' o usando la columna salt)
    2. Hashes Bcrypt existentes ('$2b$...')
    3. SHA-256 plano (fallback)
    """
    if not stored_hash or not plain_password:
        return False
        
    try:
        # 1. Caso Bcrypt (hashes legacy)
        if stored_hash.startswith("$2b$") or stored_hash.startswith("$2a$"):
            return bcrypt.checkpw(plain_password.encode('utf-8'), stored_hash.encode('utf-8'))
            
        # 2. Caso SHA-256 con formato 'sha256$<salt>$<digest>'
        if stored_hash.startswith("sha256$"):
            parts = stored_hash.split("$")
            if len(parts) == 3:
                expected_salt = parts[1]
                expected_digest = parts[2]
                computed = hashlib.sha256((expected_salt + plain_password).encode('utf-8')).hexdigest()
                return secrets.compare_digest(computed, expected_digest)
                
        # 3. Caso SHA-256 donde el salt viene en una columna separada
        if salt:
            computed = hashlib.sha256((salt + plain_password).encode('utf-8')).hexdigest()
            return secrets.compare_digest(computed, stored_hash)
            
        # 4. Caso SHA-256 plano (por si existiese sin salt)
        computed_plain = hashlib.sha256(plain_password.encode('utf-8')).hexdigest()
        return secrets.compare_digest(computed_plain, stored_hash)
        
    except Exception as e:
        print(f"[SECURITY ERROR] Error al verificar contraseña: {e}")
        return False
