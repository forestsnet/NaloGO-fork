"""
Пример использования клиента NaloGO с SOCKS5 прокси.

Для работы с SOCKS5 необходимо установить httpx с поддержкой socks:
    pip install httpx[socks]
"""

import asyncio
from nalogo import Client


async def example_with_socks5():
    """Пример с SOCKS5 прокси."""
    
    # Вариант 1: SOCKS5 прокси без авторизации
    async with Client(proxies="socks5://127.0.0.1:1080") as client:
        # Аутентификация
        token = await client.create_new_access_token("inn", "password")
        await client.authenticate(token)
        
        # Использование API
        income_api = client.income()
        result = await income_api.create("Услуга", 1000.00, 1)
        print(f"Чек создан: {result}")


async def example_with_socks5_auth():
    """Пример с SOCKS5 прокси с авторизацией."""
    
    # Вариант 2: SOCKS5 прокси с логином/паролем
    async with Client(proxies="socks5://username:password@127.0.0.1:1080") as client:
        token = await client.create_new_access_token("inn", "password")
        await client.authenticate(token)
        
        income_api = client.income()
        result = await income_api.create("Услуга", 1000.00, 1)
        print(f"Чек создан: {result}")


async def example_with_different_proxies():
    """Пример с разными прокси для HTTP и HTTPS."""
    
    # Вариант 3: Разные прокси для разных протоколов
    proxies = {
        "http://": "socks5://127.0.0.1:1080",
        "https://": "socks5://127.0.0.1:1080",
    }
    
    async with Client(proxies=proxies) as client:
        token = await client.create_new_access_token("inn", "password")
        await client.authenticate(token)
        
        income_api = client.income()
        result = await income_api.create("Услуга", 1000.00, 1)
        print(f"Чек создан: {result}")


async def example_without_context_manager():
    """Пример без использования context manager."""
    
    client = Client(proxies="socks5://127.0.0.1:1080")
    
    try:
        token = await client.create_new_access_token("inn", "password")
        await client.authenticate(token)
        
        income_api = client.income()
        result = await income_api.create("Услуга", 1000.00, 1)
        print(f"Чек создан: {result}")
    finally:
        # Важно закрыть клиент вручную
        await client.close()


async def example_with_custom_httpx_settings():
    """Пример с дополнительными настройками httpx."""
    
    # Можно передать любые параметры httpx.AsyncClient
    async with Client(
        proxies="socks5://127.0.0.1:1080",
        timeout=30.0,  # увеличенный таймаут
        limits={"max_connections": 100, "max_keepalive_connections": 20},
        verify=True,  # проверка SSL сертификатов
    ) as client:
        token = await client.create_new_access_token("inn", "password")
        await client.authenticate(token)
        
        income_api = client.income()
        result = await income_api.create("Услуга", 1000.00, 1)
        print(f"Чек создан: {result}")


if __name__ == "__main__":
    # Запуск примера
    asyncio.run(example_with_socks5())
