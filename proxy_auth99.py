# Расширенные настройки прокси ProxySaver с большим разнообразием портов
# Host: pool.proxysaver.com
# Port: 10000-10999 (HTTP/SOCKS)
# Country: USA  Alabama Lincoln
# Login: Tyvot7u5bOzB
# Password: 6Edg0zmh
# Rotation: For each request

import random

# Информация о прокси
proxy_info = {
    "host": "pool.proxysaver.com",
    "username": "Tyvot7u5bOzB",
    "password": "6Edg0zmh",
    "port_range": "10000-10999",
    "protocol": "HTTP/SOCKS",
    "country": "Germany",
    "region": "Waldbröl",
    "city": "Waldbröl",
    "rotation": "For each request",
    "traffic_limit": "100 MB",
    "traffic_used": "72.6 MB"
}

# Большой список разнообразных портов из диапазона 10000-10999
# Включены порты с разными интервалами для лучшего распределения
proxy_ports = [
    # Начальные порты (10000-10099)
    10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009,
    10010, 10011, 10012, 10013, 10014, 10015, 10016, 10017, 10018, 10019,
    10020, 10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028, 10029,
    10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037, 10038, 10039,
    10040, 10041, 10042, 10043, 10044, 10045, 10046, 10047, 10048, 10049,
    10050, 10055, 10060, 10065, 10070, 10075, 10080, 10085, 10090, 10095,
    
    # Средние порты (10100-10499)
    10100, 10105, 10110, 10115, 10120, 10125, 10130, 10135, 10140, 10145,
    10150, 10155, 10160, 10165, 10170, 10175, 10180, 10185, 10190, 10195,
    10200, 10205, 10210, 10215, 10220, 10225, 10230, 10235, 10240, 10245,
    10250, 10255, 10260, 10265, 10270, 10275, 10280, 10285, 10290, 10295,
    10300, 10305, 10310, 10315, 10320, 10325, 10330, 10335, 10340, 10345,
    10350, 10355, 10360, 10365, 10370, 10375, 10380, 10385, 10390, 10395,
    10400, 10405, 10410, 10415, 10420, 10425, 10430, 10435, 10440, 10445,
    10450, 10455, 10460, 10465, 10470, 10475, 10480, 10485, 10490, 10495,
    
    # Высокие порты (10500-10799)
    10500, 10505, 10510, 10515, 10520, 10525, 10530, 10535, 10540, 10545,
    10550, 10555, 10560, 10565, 10570, 10575, 10580, 10585, 10590, 10595,
    10600, 10605, 10610, 10615, 10620, 10625, 10630, 10635, 10640, 10645,
    10650, 10655, 10660, 10665, 10670, 10675, 10680, 10685, 10690, 10695,
    10700, 10705, 10710, 10715, 10720, 10725, 10730, 10735, 10740, 10745,
    10750, 10755, 10760, 10765, 10770, 10775, 10780, 10785, 10790, 10795,
    
    # Максимальные порты (10800-10999)
    10800, 10805, 10810, 10815, 10820, 10825, 10830, 10835, 10840, 10845,
    10850, 10855, 10860, 10865, 10870, 10875, 10880, 10885, 10890, 10895,
    10900, 10905, 10910, 10915, 10920, 10925, 10930, 10935, 10940, 10945,
    10950, 10955, 10960, 10965, 10970, 10975, 10980, 10985, 10990, 10995,
    10999,
    
    # Дополнительные случайные порты для еще большего разнообразия
    10077, 10088, 10099, 10111, 10122, 10133, 10144, 10166, 10177, 10188,
    10199, 10211, 10222, 10233, 10244, 10266, 10277, 10288, 10299, 10311,
    10322, 10333, 10344, 10366, 10377, 10388, 10399, 10411, 10422, 10433,
    10444, 10466, 10477, 10488, 10499, 10511, 10522, 10533, 10544, 10566,
    10577, 10588, 10599, 10611, 10622, 10633, 10644, 10666, 10677, 10688,
    10699, 10711, 10722, 10733, 10744, 10766, 10777, 10788, 10799, 10811,
    10822, 10833, 10844, 10866, 10877, 10888, 10899, 10911, 10922, 10933,
    10944, 10966, 10977, 10988
]

# Основной прокси (HTTP)
proxies = {
    "http": f"http://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['host']}:10000",
    "https": f"http://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['host']}:10000"
}

def get_proxy_string(port):
    """Получить строку прокси для определенного порта"""
    return f"http://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['host']}:{port}"

def get_random_proxy():
    """Получить случайный прокси из списка портов"""
    random_port = random.choice(proxy_ports)
    proxy_string = get_proxy_string(random_port)
    return {
        "http": proxy_string,
        "https": proxy_string
    }

def get_proxy_by_port(port):
    """Получить прокси с определенным портом"""
    if port in proxy_ports:
        proxy_string = get_proxy_string(port)
        return {
            "http": proxy_string,
            "https": proxy_string
        }
    else:
        # Если порт не в списке, но в диапазоне 10000-10999, все равно попробуем
        if 10000 <= port <= 10999:
            proxy_string = get_proxy_string(port)
            return {
                "http": proxy_string,
                "https": proxy_string
            }
        else:
            return proxies

def get_multiple_random_proxies(count=5):
    """Получить несколько случайных прокси"""
    selected_ports = random.sample(proxy_ports, min(count, len(proxy_ports)))
    proxies_list = []
    
    for port in selected_ports:
        proxy_string = get_proxy_string(port)
        proxies_list.append({
            "port": port,
            "http": proxy_string,
            "https": proxy_string
        })
    
    return proxies_list

def get_proxy_by_range(start_port, end_port):
    """Получить прокси из определенного диапазона портов"""
    range_ports = [port for port in proxy_ports if start_port <= port <= end_port]
    if range_ports:
        selected_port = random.choice(range_ports)
        proxy_string = get_proxy_string(selected_port)
        return {
            "port": selected_port,
            "http": proxy_string,
            "https": proxy_string
        }
    else:
        return get_random_proxy()

def get_ports_by_category():
    """Получить порты по категориям"""
    return {
        "low": [port for port in proxy_ports if 10000 <= port <= 10199],
        "medium_low": [port for port in proxy_ports if 10200 <= port <= 10399],
        "medium": [port for port in proxy_ports if 10400 <= port <= 10599],
        "medium_high": [port for port in proxy_ports if 10600 <= port <= 10799],
        "high": [port for port in proxy_ports if 10800 <= port <= 10999]
    }

def get_proxy_by_category(category="random"):
    """Получить прокси из определенной категории портов"""
    categories = get_ports_by_category()
    
    if category == "random":
        category = random.choice(list(categories.keys()))
    
    if category in categories and categories[category]:
        selected_port = random.choice(categories[category])
        proxy_string = get_proxy_string(selected_port)
        return {
            "category": category,
            "port": selected_port,
            "http": proxy_string,
            "https": proxy_string
        }
    else:
        return get_random_proxy()

# SOCKS прокси (если нужен)
def get_socks_proxy(port=None):
    """Получить SOCKS5 прокси"""
    if port is None:
        port = random.choice(proxy_ports)
    
    return {
        "http": f"socks5://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['host']}:{port}",
        "https": f"socks5://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['host']}:{port}"
    }

# Статистика портов
def get_ports_statistics():
    """Получить статистику по портам"""
    categories = get_ports_by_category()
    total_ports = len(proxy_ports)
    
    stats = {
        "total_ports": total_ports,
        "port_range": f"{min(proxy_ports)}-{max(proxy_ports)}",
        "categories": {}
    }
    
    for category, ports in categories.items():
        stats["categories"][category] = {
            "count": len(ports),
            "percentage": round((len(ports) / total_ports) * 100, 1),
            "range": f"{min(ports)}-{max(ports)}" if ports else "empty"
        }
    
    return stats

if __name__ == "__main__":
    print("🚀 РАСШИРЕННЫЕ НАСТРОЙКИ ПРОКСИ ProxySaver")
    print("=" * 60)
    
    # Основная информация
    print("🔧 Информация о прокси:")
    for key, value in proxy_info.items():
        print(f"   • {key.replace('_', ' ').capitalize()}: {value}")
    
    # Статистика портов
    print(f"\n📊 Статистика портов:")
    stats = get_ports_statistics()
    print(f"   • Всего портов: {stats['total_ports']}")
    print(f"   • Диапазон: {stats['port_range']}")
    
    print(f"\n📋 Распределение по категориям:")
    for category, info in stats["categories"].items():
        print(f"   • {category.replace('_', ' ').title()}: {info['count']} портов ({info['percentage']}%) - {info['range']}")
    
    # Примеры прокси
    print(f"\n🔗 Примеры прокси:")
    print(f"   • Основной: {proxies['http']}")
    
    print(f"\n🎲 Случайные прокси:")
    for i in range(5):
        random_proxy = get_random_proxy()
        print(f"   • {random_proxy['http']}")
    
    print(f"\n🎯 Прокси по категориям:")
    for category in ["low", "medium", "high"]:
        cat_proxy = get_proxy_by_category(category)
        print(f"   • {category.capitalize()} (порт {cat_proxy.get('port', 'N/A')}): {cat_proxy['http']}")
    
    print(f"\n🧪 SOCKS5 прокси:")
    socks_proxy = get_socks_proxy()
    print(f"   • {socks_proxy['http']}")
    
    print(f"\n✅ Конфигурация готова к использованию!")
    print(f"📈 Доступно {len(proxy_ports)} различных портов для ротации")