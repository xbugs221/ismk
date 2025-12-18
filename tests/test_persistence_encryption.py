import pytest
from ismk.persistence_encryption import MetadataEncryptor

try:
    from cryptography.fernet import Fernet
    HAS_CRYPTOGRAPHY = True
except ImportError:
    HAS_CRYPTOGRAPHY = False

@pytest.mark.skipif(not HAS_CRYPTOGRAPHY, reason="cryptography not installed")
def test_encryption_init():
    key = Fernet.generate_key()
    encryptor = MetadataEncryptor(key)
    assert encryptor.enabled
    assert encryptor.cipher is not None
    assert "code" in encryptor.sensitive_fields

def test_encryption_disabled_init():
    encryptor = MetadataEncryptor(None)
    assert not encryptor.enabled
    assert encryptor.cipher is None
    assert encryptor.sensitive_fields == []

@pytest.mark.skipif(not HAS_CRYPTOGRAPHY, reason="cryptography not installed")
def test_encrypt_decrypt_record():
    key = Fernet.generate_key()
    encryptor = MetadataEncryptor(key)
    
    original_record = {
        "code": "print('hello')",
        "shellcmd": "echo hello",
        "params": {"param1": 123, "param2": "value"},
        "input": ["file1.txt"],
        "output": ["file2.txt"]
    }
    
    # Encrypt
    encrypted = encryptor.encrypt_record(original_record)
    
    # Verify sensitive fields are encrypted
    assert encrypted["code"]["_encrypted"] is True
    assert encrypted["shellcmd"]["_encrypted"] is True
    assert encrypted["params"]["_encrypted"] is True
    
    # Verify non-sensitive fields are untouched
    assert encrypted["input"] == original_record["input"]
    assert encrypted["output"] == original_record["output"]
    
    # Verify values are actually changed (not plain text)
    assert encrypted["code"]["_value"] != original_record["code"]
    
    # Decrypt
    decrypted = encryptor.decrypt_record(encrypted)
    
    # Verify complete restoration
    assert decrypted == original_record

@pytest.mark.skipif(not HAS_CRYPTOGRAPHY, reason="cryptography not installed")
def test_encrypt_partial_fields():
    key = Fernet.generate_key()
    encryptor = MetadataEncryptor(key)
    
    # Record with missing sensitive fields
    record = {
        "code": "print('hello')",
        # missing shellcmd and params
        "input": []
    }
    
    encrypted = encryptor.encrypt_record(record)
    assert encrypted["code"]["_encrypted"] is True
    assert "shellcmd" not in encrypted
    
    decrypted = encryptor.decrypt_record(encrypted)
    assert decrypted == record

@pytest.mark.skipif(not HAS_CRYPTOGRAPHY, reason="cryptography not installed")
def test_decrypt_wrong_key(caplog):
    key1 = Fernet.generate_key()
    key2 = Fernet.generate_key()
    
    encryptor1 = MetadataEncryptor(key1)
    encryptor2 = MetadataEncryptor(key2)
    
    record = {"code": "secret"}
    encrypted = encryptor1.encrypt_record(record)
    
    # Decrypt with wrong key
    decrypted = encryptor2.decrypt_record(encrypted)
    
    # Should return the encrypted version (fallback)
    assert decrypted["code"]["_encrypted"] is True
    
    # Check for warning
    assert "Failed to decrypt metadata field" in caplog.text

def test_passthrough_disabled():
    encryptor = MetadataEncryptor(None)
    record = {"code": "secret"}
    
    encrypted = encryptor.encrypt_record(record)
    assert encrypted == record
    
    decrypted = encryptor.decrypt_record(record)
    assert decrypted == record
