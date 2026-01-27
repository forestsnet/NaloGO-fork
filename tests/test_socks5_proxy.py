"""
Тест для проверки работы SOCKS5 прокси.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from nalogo import Client
from nalogo._http import AsyncHTTPClient


@pytest.mark.asyncio
async def test_client_with_socks5_proxy():
    """Проверка инициализации клиента с SOCKS5 прокси."""
    
    # Создаем клиент с SOCKS5
    client = Client(proxies="socks5://127.0.0.1:1080")
    
    # Проверяем, что http_client создан с правильными параметрами
    assert client.http_client is not None
    assert client.http_client._client_kwargs.get("proxies") == "socks5://127.0.0.1:1080"
    
    # Закрываем клиент
    await client.close()


@pytest.mark.asyncio
async def test_client_with_socks5_auth():
    """Проверка инициализации клиента с SOCKS5 прокси и авторизацией."""
    
    proxy_url = "socks5://user:pass@127.0.0.1:1080"
    client = Client(proxies=proxy_url)
    
    assert client.http_client._client_kwargs.get("proxies") == proxy_url
    
    await client.close()


@pytest.mark.asyncio
async def test_client_with_multiple_proxies():
    """Проверка инициализации клиента с разными прокси для HTTP/HTTPS."""
    
    proxies = {
        "http://": "socks5://127.0.0.1:1080",
        "https://": "socks5://127.0.0.1:1080"
    }
    client = Client(proxies=proxies)
    
    assert client.http_client._client_kwargs.get("proxies") == proxies
    
    await client.close()


@pytest.mark.asyncio
async def test_client_context_manager():
    """Проверка работы context manager."""
    
    async with Client(proxies="socks5://127.0.0.1:1080") as client:
        assert client.http_client is not None
        # В контексте менеджере клиент должен быть инициализирован
        await client.http_client._ensure_client()
        assert client.http_client._client is not None
    
    # После выхода из контекста клиент должен быть закрыт
    assert client.http_client._client is None


@pytest.mark.asyncio
async def test_http_client_reuse():
    """Проверка, что HTTP клиент переиспользуется, а не создается заново."""
    
    client = Client()
    await client.http_client._ensure_client()
    
    # Сохраняем ссылку на первый клиент
    first_http_client = client.http_client._client
    
    # Вызываем _ensure_client еще раз
    await client.http_client._ensure_client()
    
    # Должен вернуться тот же самый клиент
    assert client.http_client._client is first_http_client
    
    await client.close()


@pytest.mark.asyncio
async def test_custom_httpx_settings():
    """Проверка передачи дополнительных параметров httpx."""
    
    client = Client(
        proxies="socks5://127.0.0.1:1080",
        timeout=30.0,
        limits={"max_connections": 100},
        verify=False
    )
    
    assert client.http_client._client_kwargs.get("proxies") == "socks5://127.0.0.1:1080"
    assert client.http_client._client_kwargs.get("timeout") == 30.0
    assert client.http_client._client_kwargs.get("limits") == {"max_connections": 100}
    assert client.http_client._client_kwargs.get("verify") is False
    
    await client.close()
