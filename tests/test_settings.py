import os
from mcp_lightrag.settings import get_settings
from mcp_lightrag.models import ServerSettings

def test_default_settings():
    settings = get_settings()
    assert settings.host == "localhost"
    assert settings.port == 9621
    assert settings.api_key == ""
    assert settings.base_url == "http://localhost:9621"

def test_env_settings():
    os.environ["LIGHTRAG_HOST"] = "test-host"
    os.environ["LIGHTRAG_PORT"] = "1234"
    os.environ["LIGHTRAG_API_KEY"] = "test-key"
    
    settings = get_settings()
    assert settings.host == "test-host"
    assert settings.port == 1234
    assert settings.api_key == "test-key"
    assert settings.base_url == "http://test-host:1234"
    
    # Cleanup
    del os.environ["LIGHTRAG_HOST"]
    del os.environ["LIGHTRAG_PORT"]
    del os.environ["LIGHTRAG_API_KEY"]
