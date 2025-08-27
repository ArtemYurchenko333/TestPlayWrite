# Новые настройки прокси на основе скриншота
# Host: pool.proxysaver.com
# Port: 10000-10999 (HTTP/SOCKS)
# Country: USA, Texas, Bulverde
# Login: iz6fyhJYysH4
# Password: 7DJjbhyq
# Rotation: 	10 min

# Основной прокси (HTTP)
proxies = {
    "http": "http://iz6fyhJYysH4:7DJjbhyq@pool.proxysaver.com:10000",
    "https": "http://iz6fyhJYysH4:7DJjbhyq@pool.proxysaver.com:10000"
}

# Альтернативные порты для ротации
proxy_ports = [
    10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009,
    10010, 10011, 10012, 10013, 10014, 10015, 10016, 10017, 10018, 10019,
    10020, 10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028, 10029,
    10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037, 10038, 10039,
    10040, 10041, 10042, 10043, 10044, 10045, 10046, 10047, 10048, 10049,
    10050
]

# Функция для получения случайного прокси
def get_random_proxy():
    import random
    port = random.choice(proxy_ports)
    return {
        "http": f"http://iz6fyhJYysH4:7DJjbhyq@pool.proxysaver.com:{port}",
        "https": f"http://Niz6fyhJYysH4:7DJjbhyq@pool.proxysaver.com:{port}"
    }

# Функция для получения прокси с определенным портом
def get_proxy_by_port(port):
    if port in proxy_ports:
        return {
            "http": f"http://iz6fyhJYysH4:7DJjbhyq@pool.proxysaver.com:{port}",
            "https": f"http://iz6fyhJYysH4:7DJjbhyq@pool.proxysaver.com:{port}"
        }
    else:
        return proxies

# Информация о прокси
proxy_info = {
    "host": "pool.proxysaver.com",
    "username": "NmSvj3ScvHdW",
    "password": "7DJjbhyq",
    "port_range": "10000-10999",
    "protocol": "HTTP/SOCKS",
    "country": "USA",
    "region": "New York",
    "city": "Delhi",
    "rotation": "For each request",
    "traffic_limit": "100 MB"
}

# SOCKS прокси (если нужен)
socks_proxies = {
    "http": "socks5://iz6fyhJYysH4:7DJjbhyq@pool.proxysaver.com:10000",
    "https": "socks5://iz6fyhJYysH4:7DJjbhyq@pool.proxysaver.com:10000"
}

# Для тестирования разных форматов
proxy_formats = {
    "http_format": {
        "http": "http://iz6fyhJYysH4:7DJjbhyq@pool.proxysaver.com:10000",
        "https": "http://iz6fyhJYysH4:7DJjbhyq@pool.proxysaver.com:10000"
    },
    "socks5_format": {
        "http": "socks5://iz6fyhJYysH4:7DJjbhyq@pool.proxysaver.com:10000",
        "https": "socks5://iz6fyhJYysH4:7DJjbhyq@pool.proxysaver.com:10000"
    }
}

if __name__ == "__main__":
    print("🔧 Настройки прокси ProxySaver:")
    print(f"   • Хост: {proxy_info['host']}")
    print(f"   • Порты: {proxy_info['port_range']}")
    print(f"   • Пользователь: {proxy_info['username']}")
    print(f"   • Пароль: {'*' * len(proxy_info['password'])}")
    print(f"   • Страна: {proxy_info['country']}")
    print(f"   • Регион: {proxy_info['region']}")
    print(f"   • Город: {proxy_info['city']}")
    print(f"   • Ротация: {proxy_info['rotation']}")
    print(f"   • Лимит трафика: {proxy_info['traffic_limit']}")
    
    print(f"\n🌐 Основной прокси:")
    print(f"   • HTTP: {proxies['http']}")
    print(f"   • HTTPS: {proxies['https']}")
    
    print(f"\n🎲 Случайный прокси:")
    random_proxy = get_random_proxy()
    print(f"   • HTTP: {random_proxy['http']}")
    print(f"   • HTTPS: {random_proxy['https']}")
