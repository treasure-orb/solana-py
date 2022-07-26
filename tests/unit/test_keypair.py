import base64

from solders.pubkey import Pubkey

from solana.keypair import Keypair


def test_new_keypair() -> None:
    """Test new keypair with random seed is created successfully."""
    keypair = Keypair()
    assert len(keypair.secret_key) == 64
    assert len(bytes(keypair.public_key)) == Pubkey.LENGTH


def test_generate_keypair() -> None:
    """Test .generate constructor works."""
    keypair = Keypair.generate()
    assert len(keypair.secret_key) == 64


def test_sign_message(stubbed_sender):
    """Test message signing."""
    msg = b"hello"
    signature = stubbed_sender.sign(msg)
    assert signature.verify(stubbed_sender.public_key.to_solders(), msg)


def test_create_from_secret_key() -> None:
    """Test creation with 64-byte secret key."""
    secret_key = base64.b64decode(
        "mdqVWeFekT7pqy5T49+tV12jO0m+ESW7ki4zSU9JiCgbL0kJbj5dvQ/PqcDAzZLZqzshVEs01d1KZdmLh4uZIg=="
    )
    keypair = Keypair.from_secret_key(secret_key)
    assert str(keypair.public_key) == "2q7pyhPwAwZ3QMfZrnAbDhnh9mDUqycszcpf86VgQxhF"
    assert keypair.secret_key == secret_key


def test_create_from_seed() -> None:
    """Test creation with 32-byte secret seed."""
    seed = bytes([8] * 32)
    keypair = Keypair.from_seed(seed)
    assert str(keypair.public_key) == "2KW2XRd9kwqet15Aha2oK3tYvd3nWbTFH1MBiRAv1BE1"
    assert keypair.seed == seed


def test_set_operations() -> None:
    """Tests that a keypair is now hashable with the appropriate set operations."""
    keypair_primary = Keypair.generate()
    keypair_secondary = Keypair.generate()
    keypair_duplicate = keypair_secondary
    keypair_set = {keypair_primary, keypair_secondary, keypair_duplicate}
    assert keypair_primary.__hash__() != keypair_secondary.__hash__()
    assert keypair_secondary.__hash__() == keypair_duplicate.__hash__()
    assert len(keypair_set) == 2
