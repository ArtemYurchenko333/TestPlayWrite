import requests
import socket
import time
import asyncio
from playwright.async_api import async_playwright
from proxy_auth33 import proxies, get_random_proxy, proxy_info, get_proxy_by_port

class ProxyTester:
    def __init__(self):
        self.current_proxy = None
        self.results = {}
        
    def print_header(self, title):
        """Печать заголовка"""
        print("\n" + "=" * 60)
        print(f"🔍 {title}")
        print("=" * 60)
    
    def print_section(self, title):
        """Печать секции"""
        print(f"\n📋 {title}")
        print("-" * 40)
    
    def parse_proxy(self, proxy_string):
        """Парсинг строки прокси"""
        try:
            proxy_parts = proxy_string.replace("http://", "").split("@")
            if len(proxy_parts) == 2:
                auth_part = proxy_parts[0]
                server_part = proxy_parts[1]
                username, password = auth_part.split(":")
                host, port = server_part.split(":")
                
                return {
                    'host': host,
                    'port': int(port),
                    'username': username,
                    'password': password,
                    'full_string': proxy_string
                }
            return None
        except Exception as e:
            print(f"❌ Ошибка парсинга прокси: {e}")
            return None
    
    def test_tcp_connection(self, proxy_data):
        """Тест TCP соединения с прокси сервером"""
        try:
            print(f"🔌 Тестируем TCP соединение с {proxy_data['host']}:{proxy_data['port']}...")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            start_time = time.time()
            result = sock.connect_ex((proxy_data['host'], proxy_data['port']))
            end_time = time.time()
            
            sock.close()
            
            if result == 0:
                response_time = round((end_time - start_time) * 1000, 2)
                print(f"✅ TCP соединение установлено ({response_time}ms)")
                return True, response_time
            else:
                print(f"❌ TCP соединение не удалось (код ошибки: {result})")
                return False, None
                
        except Exception as e:
            print(f"❌ Ошибка TCP соединения: {e}")
            return False, None
    
    def test_http_proxy_requests(self, proxy_data):
        """Тест HTTP прокси через requests"""
        try:
            print(f"🌐 Тестируем HTTP прокси через requests...")
            
            proxy_dict = {
                'http': f'http://{proxy_data["username"]}:{proxy_data["password"]}@{proxy_data["host"]}:{proxy_data["port"]}',
                'https': f'http://{proxy_data["username"]}:{proxy_data["password"]}@{proxy_data["host"]}:{proxy_data["port"]}'
            }
            
            # Получаем реальный IP
            try:
                real_ip = requests.get('https://httpbin.org/ip', timeout=10).json()['origin']
                print(f"🏠 Реальный IP: {real_ip}")
            except:
                real_ip = "неизвестен"
                print("⚠️ Не удалось получить реальный IP")
            
            # Тестируем разные сервисы
            test_urls = [
                {'url': 'https://httpbin.org/ip', 'name': 'HTTPBin', 'json_key': 'origin'},
                {'url': 'https://api.ipify.org', 'name': 'IPify', 'json_key': None},
                {'url': 'https://icanhazip.com', 'name': 'ICanHazIP', 'json_key': None}
            ]
            
            successful_tests = 0
            proxy_ips = []
            
            for test in test_urls:
                try:
                    print(f"   🔄 Тестируем {test['name']}...")
                    start_time = time.time()
                    
                    response = requests.get(test['url'], proxies=proxy_dict, timeout=15)
                    
                    end_time = time.time()
                    response_time = round((end_time - start_time) * 1000, 2)
                    
                    if test['json_key']:
                        proxy_ip = response.json()[test['json_key']].split(',')[0].strip()
                    else:
                        proxy_ip = response.text.strip()
                    
                    print(f"   ✅ {test['name']}: {proxy_ip} ({response_time}ms)")
                    proxy_ips.append(proxy_ip)
                    successful_tests += 1
                    
                except requests.exceptions.ProxyError as e:
                    print(f"   ❌ {test['name']}: Ошибка прокси - {e}")
                except requests.exceptions.Timeout as e:
                    print(f"   ❌ {test['name']}: Таймаут - {e}")
                except Exception as e:
                    print(f"   ❌ {test['name']}: {e}")
            
            if successful_tests > 0:
                unique_ips = list(set(proxy_ips))
                print(f"✅ HTTP прокси работает! Успешных тестов: {successful_tests}/3")
                print(f"📍 IP адреса через прокси: {', '.join(unique_ips)}")
                
                if real_ip != "неизвестен" and any(ip != real_ip for ip in unique_ips):
                    print("✅ IP успешно изменен - прокси работает корректно!")
                    return True, unique_ips
                else:
                    print("⚠️ IP не изменился - возможны проблемы с прокси")
                    return False, unique_ips
            else:
                print("❌ HTTP прокси не работает")
                return False, []
                
        except Exception as e:
            print(f"❌ Ошибка тестирования HTTP прокси: {e}")
            return False, []
    
    async def test_playwright_proxy(self, proxy_data):
        """Тест прокси в Playwright"""
        try:
            print(f"🎭 Тестируем прокси в Playwright...")
            
            playwright = await async_playwright().start()
            
            browser = await playwright.chromium.launch(headless=True)
            
            context = await browser.new_context(
                proxy={
                    "server": f"http://{proxy_data['host']}:{proxy_data['port']}",
                    "username": proxy_data['username'],
                    "password": proxy_data['password']
                }
            )
            
            page = await context.new_page()
            
            # Тестируем разные сервисы
            test_services = [
                'https://httpbin.org/ip',
                'https://api.ipify.org',
                'https://icanhazip.com'
            ]
            
            successful_tests = 0
            playwright_ips = []
            
            for service in test_services:
                try:
                    print(f"   🔄 Playwright тест: {service}")
                    
                    await page.goto(service, timeout=20000)
                    await page.wait_for_timeout(3000)
                    
                    if 'httpbin' in service:
                        content = await page.inner_text('pre')
                        import json
                        ip = json.loads(content)['origin'].split(',')[0].strip()
                    else:
                        ip = await page.inner_text('pre')
                        ip = ip.strip()
                    
                    print(f"   ✅ {service}: {ip}")
                    playwright_ips.append(ip)
                    successful_tests += 1
                    
                except Exception as e:
                    print(f"   ❌ {service}: {e}")
            
            await browser.close()
            await playwright.stop()
            
            if successful_tests > 0:
                unique_ips = list(set(playwright_ips))
                print(f"✅ Playwright прокси работает! Успешных тестов: {successful_tests}/3")
                print(f"📍 IP адреса: {', '.join(unique_ips)}")
                return True, unique_ips
            else:
                print("❌ Playwright прокси не работает")
                return False, []
                
        except Exception as e:
            print(f"❌ Ошибка тестирования Playwright прокси: {e}")
            return False, []
    
    def test_multiple_ports(self, base_proxy_data, ports_to_test=5):
        """Тест нескольких портов"""
        print(f"🔄 Тестируем {ports_to_test} разных портов...")
        
        base_port = base_proxy_data['port']
        working_ports = []
        
        for i in range(ports_to_test):
            test_port = base_port + i
            print(f"\n   🔌 Тестируем порт {test_port}...")
            
            test_proxy_data = base_proxy_data.copy()
            test_proxy_data['port'] = test_port
            
            tcp_result, response_time = self.test_tcp_connection(test_proxy_data)
            if tcp_result:
                working_ports.append({'port': test_port, 'response_time': response_time})
        
        if working_ports:
            print(f"\n✅ Рабочие порты найдены: {len(working_ports)}/{ports_to_test}")
            for port_info in working_ports:
                print(f"   • Порт {port_info['port']}: {port_info['response_time']}ms")
        else:
            print(f"\n❌ Ни один из {ports_to_test} портов не работает")
        
        return working_ports
    
    def generate_report(self):
        """Генерация отчета"""
        self.print_header("ОТЧЕТ О ТЕСТИРОВАНИИ ПРОКСИ")
        
        print(f"🔧 Информация о прокси:")
        print(f"   • Провайдер: {proxy_info['host']}")
        print(f"   • Страна: {proxy_info['country']}")
        print(f"   • Регион: {proxy_info['region']}")
        print(f"   • Лимит трафика: {proxy_info['traffic_limit']}")
        
        print(f"\n📊 Результаты тестирования:")
        for test_name, result in self.results.items():
            status = "✅ Работает" if result['success'] else "❌ Не работает"
            print(f"   • {test_name}: {status}")
            if 'details' in result:
                print(f"     {result['details']}")
        
        # Рекомендации
        print(f"\n💡 Рекомендации:")
        if any(result['success'] for result in self.results.values()):
            print("   ✅ Прокси частично или полностью работает")
            if not self.results.get('tcp', {}).get('success'):
                print("   ⚠️ Проблемы с TCP соединением - проверьте хост/порт")
            if not self.results.get('http', {}).get('success'):
                print("   ⚠️ Проблемы с HTTP - проверьте логин/пароль")
            if not self.results.get('playwright', {}).get('success'):
                print("   ⚠️ Проблемы с Playwright - возможны ограничения HTTPS")
        else:
            print("   ❌ Прокси не работает совсем")
            print("   • Проверьте настройки в proxy_auth22.py")
            print("   • Обратитесь к провайдеру прокси")
            print("   • Попробуйте другие порты")
    
    async def run_full_test(self):
        """Полный тест прокси"""
        self.print_header("КОМПЛЕКСНАЯ ПРОВЕРКА ПРОКСИ")
        
        # Выбираем случайный прокси
        self.current_proxy = get_random_proxy()
        proxy_string = self.current_proxy["https"]
        
        print(f"🔧 Тестируемый прокси: {proxy_string}")
        
        proxy_data = self.parse_proxy(proxy_string)
        if not proxy_data:
            print("❌ Не удалось распарсить прокси")
            return
        
        # 1. TCP соединение
        self.print_section("1. ТЕСТ TCP СОЕДИНЕНИЯ")
        tcp_success, response_time = self.test_tcp_connection(proxy_data)
        self.results['tcp'] = {
            'success': tcp_success,
            'details': f"Время отклика: {response_time}ms" if response_time else "Соединение не установлено"
        }
        
        # 2. HTTP прокси через requests
        self.print_section("2. ТЕСТ HTTP ПРОКСИ (REQUESTS)")
        http_success, ips = self.test_http_proxy_requests(proxy_data)
        self.results['http'] = {
            'success': http_success,
            'details': f"IP адреса: {', '.join(ips)}" if ips else "Нет рабочих IP"
        }
        
        # 3. Playwright прокси
        self.print_section("3. ТЕСТ PLAYWRIGHT ПРОКСИ")
        playwright_success, playwright_ips = await self.test_playwright_proxy(proxy_data)
        self.results['playwright'] = {
            'success': playwright_success,
            'details': f"IP адреса: {', '.join(playwright_ips)}" if playwright_ips else "Нет рабочих IP"
        }
        
        # 4. Тест нескольких портов
        self.print_section("4. ТЕСТ АЛЬТЕРНАТИВНЫХ ПОРТОВ")
        working_ports = self.test_multiple_ports(proxy_data, 5)
        self.results['ports'] = {
            'success': len(working_ports) > 0,
            'details': f"Найдено рабочих портов: {len(working_ports)}/5"
        }
        
        # Генерируем отчет
        self.generate_report()

def test_specific_proxy():
    """Тест конкретного прокси"""
    print("🔧 ТЕСТ КОНКРЕТНОГО ПРОКСИ")
    print("-" * 40)
    
    # Можете указать конкретный порт
    specific_port = input("Введите порт для тестирования (или Enter для случайного): ").strip()
    
    if specific_port and specific_port.isdigit():
        test_proxy = get_proxy_by_port(int(specific_port))
        print(f"🎯 Тестируем порт {specific_port}")
    else:
        test_proxy = get_random_proxy()
        print("🎲 Тестируем случайный прокси")
    
    print(f"📍 Прокси: {test_proxy['https']}")
    
    # Быстрый тест через requests
    try:
        proxy_string = test_proxy["https"]
        proxy_parts = proxy_string.replace("http://", "").split("@")
        auth_part = proxy_parts[0]
        server_part = proxy_parts[1]
        username, password = auth_part.split(":")
        
        proxy_dict = {
            'http': f'http://{username}:{password}@{server_part}',
            'https': f'http://{username}:{password}@{server_part}'
        }
        
        print("🔄 Тестируем через requests...")
        response = requests.get('https://httpbin.org/ip', proxies=proxy_dict, timeout=15)
        proxy_ip = response.json()['origin']
        
        print(f"✅ Успех! IP через прокси: {proxy_ip}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

async def main():
    """Главная функция"""
    print("🤖 ТЕСТЕР ПРОКСИ ProxySaver")
    print("=" * 60)
    print("Режимы тестирования:")
    print("1. 🔍 Полная проверка (рекомендуется)")
    print("2. ⚡ Быстрая проверка конкретного прокси")
    print("3. 📊 Информация о настройках")
    
    try:
        choice = input("\nВыберите режим (1-3): ").strip()
        
        if choice == "1":
            tester = ProxyTester()
            await tester.run_full_test()
            
        elif choice == "2":
            test_specific_proxy()
            
        elif choice == "3":
            print("\n📋 ИНФОРМАЦИЯ О НАСТРОЙКАХ")
            print("-" * 40)
            print(f"🔧 Хост: {proxy_info['host']}")
            print(f"🌍 Страна: {proxy_info['country']}")
            print(f"🏙️ Регион: {proxy_info['region']}")
            print(f"🏘️ Город: {proxy_info['city']}")
            print(f"👤 Пользователь: {proxy_info['username']}")
            print(f"🔑 Пароль: {'*' * len(proxy_info['password'])}")
            print(f"🚪 Диапазон портов: {proxy_info['port_range']}")
            print(f"📊 Лимит трафика: {proxy_info['traffic_limit']}")
            print(f"🔄 Ротация: {proxy_info['rotation']}")
            
            print(f"\n🔗 Примеры прокси:")
            for i in range(3):
                example_proxy = get_random_proxy()
                print(f"   • {example_proxy['https']}")
                
        else:
            print("❌ Неверный выбор")
            
    except KeyboardInterrupt:
        print("\n⚠️ Тестирование прервано")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("🚀 Запуск тестера прокси...")
    asyncio.run(main())
