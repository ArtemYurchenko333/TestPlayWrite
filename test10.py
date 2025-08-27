import time
import random
import asyncio
import requests
from playwright.async_api import async_playwright
from proxy_auth99 import proxies, get_random_proxy, proxy_info

class MultiUserUhmegleBot:
    def __init__(self, max_users=35):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.message_count = 0
        self.max_users = max_users
        self.current_proxy = None
        
    def test_proxy_with_requests(self):
        """Проверка прокси через requests с ротацией и несколькими сервисами"""
        try:
            print("🔍 Тестируем прокси через requests...")
            
            # Используем случайный прокси для тестирования
            self.current_proxy = get_random_proxy()
            proxy_string = self.current_proxy["https"]
            print(f"🔧 Тестируем прокси: {proxy_string}")
            
            proxy_parts = proxy_string.replace("http://", "").split("@")
            
            if len(proxy_parts) == 2:
                auth_part = proxy_parts[0]
                server_part = proxy_parts[1]
                username, password = auth_part.split(":")
                
                proxy_dict = {
                    'http': f'http://{username}:{password}@{server_part}',
                    'https': f'http://{username}:{password}@{server_part}'
                }
                
                # Тест без прокси (реальный IP)
                real_ip = None
                try:
                    real_ip = requests.get('https://httpbin.org/ip', timeout=10).json()['origin']
                    print(f"🏠 Реальный IP: {real_ip}")
                except:
                    try:
                        real_ip = requests.get('https://api.ipify.org', timeout=10).text.strip()
                        print(f"🏠 Реальный IP: {real_ip}")
                    except:
                        print("⚠️ Не удалось получить реальный IP")
                
                # Тестируем прокси через разные сервисы
                test_services = [
                    'https://httpbin.org/ip',
                    'https://api.ipify.org',
                    'https://icanhazip.com'
                ]
                
                for service in test_services:
                    try:
                        print(f"🔄 Тестируем через {service}...")
                        
                        if 'httpbin' in service:
                            response = requests.get(service, proxies=proxy_dict, timeout=15)
                            proxy_ip = response.json()['origin'].split(',')[0].strip()
                        else:
                            response = requests.get(service, proxies=proxy_dict, timeout=15)
                            proxy_ip = response.text.strip()
                        
                        print(f"📍 IP через прокси ({service}): {proxy_ip}")
                        
                        if proxy_ip and proxy_ip != real_ip:
                            print(f"✅ Прокси работает через requests! ({service})")
                            return True
                        elif proxy_ip == real_ip:
                            print(f"⚠️ IP не изменился через {service}")
                        else:
                            print(f"⚠️ Некорректный ответ от {service}")
                            
                    except requests.exceptions.ProxyError as e:
                        print(f"❌ Ошибка прокси с {service}: {e}")
                    except requests.exceptions.Timeout as e:
                        print(f"❌ Таймаут с {service}: {e}")
                    except Exception as e:
                        print(f"❌ Ошибка с {service}: {e}")
                        continue
                
                print("❌ Прокси не работает через все тестируемые сервисы")
                return False
                    
        except Exception as e:
            print(f"❌ Критическая ошибка при тестировании прокси: {e}")
            return False

    def test_proxy_connection(self):
        """Тест базового соединения с прокси сервером"""
        try:
            import socket
            
            # Используем текущий прокси или получаем новый
            if not self.current_proxy:
                self.current_proxy = get_random_proxy()
            
            proxy_string = self.current_proxy["https"]
            proxy_parts = proxy_string.replace("http://", "").split("@")
            
            if len(proxy_parts) == 2:
                server_part = proxy_parts[1]
                host, port = server_part.split(":")
                
                print(f"🔌 Тестируем TCP соединение с {host}:{port}...")
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                result = sock.connect_ex((host, int(port)))
                sock.close()
                
                if result == 0:
                    print("✅ Прокси сервер доступен")
                    return True
                else:
                    print(f"❌ Прокси сервер недоступен (код ошибки: {result})")
                    return False
                    
        except Exception as e:
            print(f"❌ Ошибка при тестировании соединения: {e}")
            return False

    def diagnose_proxy_issues(self):
        """Диагностика проблем с прокси"""
        print("\n" + "🔬 ДИАГНОСТИКА ПРОБЛЕМ С ПРОКСИ")
        print("=" * 50)
        
        if not self.current_proxy:
            self.current_proxy = get_random_proxy()
        
        proxy_string = self.current_proxy["https"]
        proxy_parts = proxy_string.replace("http://", "").split("@")
        
        if len(proxy_parts) == 2:
            auth_part = proxy_parts[0]
            server_part = proxy_parts[1]
            username, password = auth_part.split(":")
            host, port = server_part.split(":")
            
            print(f"🔧 Текущий прокси:")
            print(f"   • Хост: {host}")
            print(f"   • Порт: {port}")
            print(f"   • Пользователь: {username}")
            print(f"   • Пароль: {'*' * len(password)}")
            
            print(f"\n🔍 Возможные проблемы:")
            print(f"   • Прокси сервер может быть недоступен")
            print(f"   • Неверные учетные данные")
            print(f"   • Прокси не поддерживает HTTPS")
            print(f"   • Блокировка со стороны провайдера")
            print(f"   • Исчерпан лимит трафика")
            
            print(f"\n💡 Рекомендации:")
            print(f"   1. Проверьте доступность {host}:{port}")
            print(f"   2. Убедитесь в правильности логина/пароля")
            print(f"   3. Попробуйте другой порт из диапазона 10000-10999")
            print(f"   4. Проверьте лимит трафика в панели ProxySaver")
            print(f"   5. Попробуйте запустить без прокси для тестирования")
            
        print("=" * 50)

    async def setup_browser_with_proxy(self):
        """Настройка браузера с прокси и ротацией"""
        try:
            print("🔧 Настраиваем браузер с прокси...")
            
            # Используем текущий прокси или получаем новый
            if not self.current_proxy:
                self.current_proxy = get_random_proxy()
            
            proxy_string = self.current_proxy["https"]
            proxy_parts = proxy_string.replace("http://", "").split("@")
            
            if len(proxy_parts) != 2:
                print("❌ Неверный формат прокси")
                return False
                
            auth_part = proxy_parts[0]
            server_part = proxy_parts[1]
            username, password = auth_part.split(":")
            proxy_host, proxy_port = server_part.split(":")
            
            print(f"🔧 Прокси сервер: {proxy_host}:{proxy_port}")
            print(f"🔧 Пользователь: {username}")
            print(f"🌍 Локация: {proxy_info['country']}, {proxy_info['region']}")
            
            self.playwright = await async_playwright().start()
            
            # Настройки браузера для стабильности
            browser_args = [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--ignore-certificate-errors",
                "--ignore-ssl-errors",
                "--allow-running-insecure-content",
                "--disable-extensions-except",
                "--disable-plugins-discovery",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
                "--disable-renderer-backgrounding"
            ]
            
            # Случайный user-agent
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
            ]
            
            # Запускаем браузер
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                args=browser_args
            )
            
            # Создаем контекст с прокси
            self.context = await self.browser.new_context(
                proxy={
                    "server": f"http://{proxy_host}:{proxy_port}",
                    "username": username,
                    "password": password
                },
                user_agent=random.choice(user_agents),
                viewport={"width": 1280, "height": 720},
                locale="en-US"
            )
            
            # Создаем страницу
            self.page = await self.context.new_page()
            
            # Увеличиваем таймауты
            self.page.set_default_timeout(30000)
            self.page.set_default_navigation_timeout(60000)
            
            # Маскировка автоматизации
            await self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                window.chrome = {runtime: {}};
                
                // Блокируем WebRTC для скрытия реального IP
                navigator.getUserMedia = navigator.webkitGetUserMedia = navigator.mozGetUserMedia = function () {
                    throw new Error('WebRTC blocked');
                };
            """)
            
            print("✅ Браузер успешно настроен с прокси")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при настройке браузера: {e}")
            return False

    async def setup_browser_without_proxy(self):
        """Настройка браузера БЕЗ прокси (для тестирования)"""
        try:
            print("🔧 Настраиваем браузер БЕЗ прокси...")
            
            self.playwright = await async_playwright().start()
            
            # Настройки браузера
            browser_args = [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
            
            # Запускаем браузер
            self.browser = await self.playwright.chromium.launch(
                headless=False,
                args=browser_args
            )
            
            # Создаем контекст БЕЗ прокси
            self.context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 720}
            )
            
            # Создаем страницу
            self.page = await self.context.new_page()
            
            # Увеличиваем таймауты
            self.page.set_default_timeout(30000)
            self.page.set_default_navigation_timeout(60000)
            
            # Маскировка автоматизации
            await self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                window.chrome = {runtime: {}};
            """)
            
            print("✅ Браузер успешно настроен БЕЗ прокси")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при настройке браузера без прокси: {e}")
            return False

    async def check_ip_in_browser(self):
        """Проверка IP адреса в браузере через несколько сервисов"""
        # Сначала пробуем HTTP сервисы (могут лучше работать через прокси)
        ip_services = [
            {
                "url": "http://httpbin.org/ip",
                "name": "HTTPBin (HTTP)",
                "selector": "pre",
                "json_key": "origin"
            },
            {
                "url": "http://api.ipify.org",
                "name": "IPify (HTTP)",
                "selector": "pre",
                "json_key": None
            },
            {
                "url": "http://icanhazip.com",
                "name": "ICanHazIP (HTTP)",
                "selector": "pre",
                "json_key": None
            },
            {
                "url": "https://httpbin.org/ip",
                "name": "HTTPBin (HTTPS)",
                "selector": "pre",
                "json_key": "origin"
            },
            {
                "url": "https://api.ipify.org",
                "name": "IPify (HTTPS)",
                "selector": "pre",
                "json_key": None
            }
        ]
        
        for service in ip_services:
            try:
                print(f"🌐 Проверяем IP через {service['name']}: {service['url']}")
                
                # Переходим на сервис с увеличенным таймаутом
                await self.page.goto(service['url'], wait_until="domcontentloaded", timeout=20000)
                await self.page.wait_for_timeout(5000)
                
                # Получаем IP из элемента
                ip_element = await self.page.query_selector(service['selector'])
                if ip_element:
                    content = await ip_element.inner_text()
                    content = content.strip()
                    
                    # Если это JSON, парсим его
                    if service['json_key']:
                        try:
                            import json
                            data = json.loads(content)
                            ip_address = data.get(service['json_key'], '').split(',')[0].strip()
                        except:
                            ip_address = content
                    else:
                        ip_address = content
                    
                    print(f"📍 IP от {service['name']}: {ip_address}")
                    
                    # Проверяем, что IP валидный
                    if ip_address and len(ip_address.split('.')) == 4:
                        # Проверяем, что IP отличается от реального (замените на ваш реальный IP)
                        if ip_address != "185.102.186.90":
                            print(f"✅ Прокси работает корректно! IP: {ip_address}")
                            return True
                        else:
                            print(f"⚠️ Показывается реальный IP: {ip_address}")
                    else:
                        print(f"⚠️ Некорректный IP: {ip_address}")
                else:
                    print(f"❌ Не удалось найти элемент с IP на {service['name']}")
                
            except Exception as e:
                print(f"❌ Ошибка с {service['name']}: {e}")
                continue
        
        print("⚠️ Не удалось проверить IP ни через один сервис")
        
        # Дополнительная проверка - можем ли мы вообще загрузить страницы через прокси
        print("🔍 Проверяем общую работоспособность прокси...")
        try:
            await self.page.goto("http://example.com", wait_until="domcontentloaded", timeout=15000)
            print("✅ Простая HTTP страница загружается - прокси частично работает")
            return True
        except Exception as e:
            print(f"❌ Даже простая страница не загружается: {e}")
            
            # Последняя проверка - без прокси ли мы работаем?
            print("🔍 Возможно, прокси не настроен и мы работаем напрямую...")
            try:
                await self.page.goto("https://www.google.com", wait_until="domcontentloaded", timeout=10000)
                print("⚠️ Google загружается - возможно, работаем без прокси")
                return True
            except Exception as e2:
                print(f"❌ Интернет соединение отсутствует: {e2}")
                return False

    async def open_uhmegle_with_retry(self):
        """Открытие сайта uhmegle.com с повторными попытками"""
        urls_to_try = [
            "https://uhmegle.com/text/",
            "https://uhmegle.com/",
            "https://www.uhmegle.com/text/",
            "https://www.uhmegle.com/"
        ]
        
        for attempt in range(3):
            for url in urls_to_try:
                try:
                    print(f"🌐 Попытка {attempt + 1}: Открываем {url}...")
                    
                    await self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    await self.page.wait_for_timeout(5000)
                    
                    title = await self.page.title()
                    current_url = self.page.url
                    
                    print(f"📄 Заголовок: {title}")
                    print(f"🔗 URL: {current_url}")
                    
                    # Проверяем на успешную загрузку
                    if "uhmegle" in current_url.lower() and not "error" in title.lower():
                        print("✅ Сайт успешно загружен!")
                        return True
                        
                except Exception as e:
                    print(f"⚠️ Ошибка с {url}: {e}")
                    continue
            
            if attempt < 2:
                print(f"⏳ Ждем {(attempt + 1) * 5} секунд перед следующей попыткой...")
                await asyncio.sleep((attempt + 1) * 5)
        
        print("❌ Не удалось открыть сайт после всех попыток")
        return False

    async def wait_for_connection_and_start(self):
        """Ожидание подключения к серверу и поиск кнопки Start"""
        try:
            print("⏳ Ожидаем подключения к серверу...")
            
            # Ждем исчезновения сообщения о подключении
            for attempt in range(20):
                try:
                    # Проверяем текст на странице
                    page_text = await self.page.inner_text("body")
                    
                    if "connecting to server" in page_text.lower():
                        print(f"🔄 Попытка {attempt + 1}: Подключаемся к серверу...")
                        await self.page.wait_for_timeout(3000)
                        continue
                    
                    if "lost connection" in page_text.lower():
                        print("🔄 Потеряно соединение, ждем переподключения...")
                        await self.page.wait_for_timeout(3000)
                        continue
                    
                    if "attempting to reconnect" in page_text.lower():
                        print("🔄 Попытка переподключения...")
                        await self.page.wait_for_timeout(3000)
                        continue
                    
                    # Если нет сообщений о подключении, ищем кнопку Start
                    if await self.find_and_click_start():
                        return True
                    
                    await self.page.wait_for_timeout(3000)
                    
                except Exception as e:
                    print(f"⚠️ Ошибка при ожидании: {e}")
                    await self.page.wait_for_timeout(3000)
                    continue
            
            print("❌ Не удалось дождаться подключения к серверу")
            return False
            
        except Exception as e:
            print(f"❌ Ошибка при ожидании подключения: {e}")
            return False

    async def find_and_click_start(self):
        """Поиск и нажатие кнопки Start"""
        try:
            print("🔍 Ищем кнопку Start...")
            
            # Различные селекторы для кнопки Start
            selectors_to_try = [
                'button:has-text("Start")',
                'div:has-text("Start")',
                'span:has-text("Start")',
                'button:has-text("New")',
                'div:has-text("New")',
                'button:has-text("Begin")',
                '[class*="start"]',
                '[class*="bottomButton"]',
                '[class*="button"]',
                'button',
                'div[role="button"]'
            ]
            
            for selector in selectors_to_try:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for element in elements:
                        if await element.is_visible() and await element.is_enabled():
                            text = await element.inner_text()
                            text_lower = text.strip().lower()
                            
                            start_keywords = [
                                "start", "begin", "new", "next", "go", 
                                "continue", "chat", "connect", "enter"
                            ]
                            
                            if any(keyword in text_lower for keyword in start_keywords) or len(text_lower) == 0:
                                print(f"✅ Найдена кнопка: '{text}' (селектор: {selector})")
                                print("🖱️ Нажимаем кнопку...")
                                
                                await element.scroll_into_view_if_needed()
                                await element.click()
                                await self.page.wait_for_timeout(3000)
                                
                                print("✅ Кнопка Start нажата успешно!")
                                return True
                                
                except Exception:
                    continue
            
            print("❌ Кнопка Start не найдена")
            return False
            
        except Exception as e:
            print(f"❌ Ошибка при поиске кнопки Start: {e}")
            return False

    async def wait_for_chat_ready(self):
        """Ожидание готовности чата"""
        try:
            print("⏳ Ожидаем готовности чата...")
            
            for attempt in range(15):
                try:
                    # Ищем элементы чата
                    chat_selectors = [
                        'textarea',
                        'input[type="text"]',
                        '[class*="input"]',
                        '[class*="chat"]',
                        '[placeholder*="message"]',
                        '[placeholder*="type"]'
                    ]
                    
                    for selector in chat_selectors:
                        try:
                            element = await self.page.query_selector(selector)
                            if element and await element.is_visible():
                                print(f"✅ Найдено поле ввода: {selector}")
                                return True
                        except:
                            continue
                    
                    # Проверяем текст на странице
                    page_text = await self.page.inner_text("body")
                    if any(keyword in page_text.lower() for keyword in ["you're now chatting", "stranger", "connected"]):
                        print("✅ Чат готов к использованию!")
                        return True
                    
                    print(f"🔄 Попытка {attempt + 1}: Ждем готовности чата...")
                    await self.page.wait_for_timeout(2000)
                    
                except Exception as e:
                    print(f"⚠️ Ошибка при ожидании чата: {e}")
                    await self.page.wait_for_timeout(2000)
                    continue
            
            print("⚠️ Чат может быть не готов, но продолжаем...")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при ожидании готовности чата: {e}")
            return False

    async def send_message(self, message):
        """Отправка сообщения"""
        try:
            print(f"📤 Отправляем сообщение: {message}")
            
            # Ищем поле ввода
            input_selectors = [
                'textarea',
                'input[type="text"]',
                '[class*="input"] textarea',
                '[class*="input"] input',
                '[placeholder*="message"]',
                '[placeholder*="type"]'
            ]
            
            input_box = None
            for selector in input_selectors:
                try:
                    input_box = await self.page.query_selector(selector)
                    if input_box and await input_box.is_visible() and await input_box.is_enabled():
                        print(f"✅ Найдено поле ввода: {selector}")
                        break
                except:
                    continue
            
            if not input_box:
                print("❌ Поле ввода не найдено")
                return False
            
            # Фокусируемся на поле
            await input_box.focus()
            await self.page.wait_for_timeout(500)
            
            # Очищаем поле
            await input_box.fill("")
            await self.page.wait_for_timeout(500)
            
            # Вводим текст с задержкой 4 секунды (по символу)
            typing_delay = 4000 / len(message)
            await input_box.type(message, delay=typing_delay)
            
            await self.page.wait_for_timeout(500)
            
            # Ищем кнопку отправки
            send_selectors = [
                'button:has-text("Send")',
                'button:has-text("Отправить")',
                '[class*="send"]',
                'input[type="submit"]',
                '[onclick*="send"]'
            ]
            
            send_btn = None
            for selector in send_selectors:
                try:
                    send_btn = await self.page.query_selector(selector)
                    if send_btn and await send_btn.is_visible():
                        break
                except:
                    continue
            
            if send_btn:
                await send_btn.click()
                await self.page.wait_for_timeout(1000)
                print("✅ Сообщение отправлено через кнопку")
                return True
            else:
                # Пробуем отправить через Enter
                await input_box.press('Enter')
                await self.page.wait_for_timeout(1000)
                print("✅ Сообщение отправлено через Enter")
                return True
                
        except Exception as e:
            print(f"❌ Ошибка при отправке сообщения: {e}")
            return False

    async def find_next_button(self):
        """Поиск кнопки для перехода к следующему собеседнику"""
        try:
            print("🔍 Пытаемся завершить текущий чат и перейти к новому собеседнику...")

            ## Шаг 1. Нажимаем «Stop»
            #if not await self._click_first_visible([
            #    # Возможные варианты расположения Stop-кнопки
            #    'button:has-text("Stop")',                 # Кнопка
            #    'div:has-text("Stop")',                    # Вложенный div с текстом
            #    'div.bottomButton.stop',                    # Контейнер-кнопка
            #    'div.bottomButton.skipButton.stop',         # Полный набор классов
            #    '[class*="skipButton"][class*="stop"]',   # Комбинация классов
            #    '[class*="stop"]',                         # Любой элемент с классом stop
            #], "stop"):
            #    print("⚠️ Кнопка Stop не найдена. Пропускаем завершение чата ...")

            if not await self._click_first_visible([
                # Правильные селекторы на основе HTML структуры для кнопки Stop
                'div.bottomButton.outlined.skipButton.noSelect.stop',    # Полный набор классов кнопки
                'div.bottomButton.stop',                                 # Упрощенный вариант
                'div[class*="bottomButton"][class*="stop"]',             # Через атрибуты
                'div.bottomButton:has-text("Stop")',                     # Кнопка содержащая текст Stop
                'div.bottomButton.skipButton:has-text("Stop")',          # Более специфично
                '.stop',                                                 # Простой класс
                'div:has(.mainText:has-text("Stop"))',                   # Div содержащий mainText с Stop
            ], "Stop"):
                print("⚠️ Кнопка Stop не найдена. Пропускаем завершение чата ...")

            # Небольшая пауза чтобы появилась кнопка подтверждения
            await self.page.wait_for_timeout(2000)

            ## Шаг 2. Подтверждаем «Really»
            #await self._click_first_visible([
            #    # Возможные варианты расположения Really-кнопки (подтверждение)
            #    'button:has-text("Really")',               # Кнопка
            #    'div:has-text("Really")',                  # Вложенный div с текстом
            #    'div.bottomButton.really',                  # Контейнер-кнопка
            #    'div.bottomButton.skipButton.really',       # Полный набор классов
            #    '[class*="skipButton"][class*="really"]', # Комбинация классов
            #    '[class*="really"]',                       # Любой элемент с классом really
            #], "really")

            await self._click_first_visible([
                # Правильные селекторы на основе HTML структуры
                'div.bottomButton.outlined.skipButton.noSelect.really',  # Полный набор классов кнопки
                'div.bottomButton.really',                               # Упрощенный вариант
                'div[class*="bottomButton"][class*="really"]',           # Через атрибуты
                'div.bottomButton:has-text("Really")',                   # Кнопка содержащая текст Really
                'div.bottomButton.skipButton:has-text("Really")',        # Более специфично
                '.really',                                               # Простой класс
                'div:has(.mainText:has-text("Really"))',                 # Div содержащий mainText с Really
            ], "Really")

            # Ждём появления кнопки для нового собеседника
            await self.page.wait_for_timeout(2500)

            # Шаг 3. Запускаем новый чат — «Start» или «New»
            #if not await self._click_first_visible([
            #    'button:has-text("Start")',
            #    'div:has-text("Start")',
            #    'button:has-text("New")',
            #    'div:has-text("New")',
            #    '[class*="start"]',
            #    '[class*="new"]',
            #], "Start/New"):
            if not await self._click_first_visible([
            # Селекторы для кнопки New
            'div.bottomButton.outlined.skipButton.noSelect.new',     # Полный набор классов кнопки New
            'div.bottomButton.new',                                  # Упрощенный вариант New
            'div[class*="bottomButton"][class*="new"]',              # Через атрибуты New
            'div.bottomButton:has-text("New")',                      # Кнопка содержащая текст New
            'div.bottomButton.skipButton:has-text("New")',           # Более специфично New
            '.new',                                                  # Простой класс new
            'div:has(.mainText:has-text("New"))',                    # Div содержащий mainText с New
    
            # Селекторы для кнопки Start (если она существует)
            'div.bottomButton.outlined.skipButton.noSelect.start',   # Полный набор классов кнопки Start
            'div.bottomButton.start',                                # Упрощенный вариант Start
            'div[class*="bottomButton"][class*="start"]',            # Через атрибуты Start
            'div.bottomButton:has-text("Start")',                    # Кнопка содержащая текст Start
            'div.bottomButton.skipButton:has-text("Start")',         # Более специфично Start
            '.start',                                                # Простой класс start
            'div:has(.mainText:has-text("Start"))',                  # Div содержащий mainText с Start
    
            # Старые селекторы как fallback
            'button:has-text("Start")',
            'div:has-text("Start")',
            'button:has-text("New")',
            'div:has-text("New")',
            '[class*="start"]',
            '[class*="new"]',
            ], "Start/New"):
                print("⚠️ Не удалось запустить новый чат. Возможно страница изменилась, продолжаем...")

            return True

        except Exception as e:
            print(f"❌ Ошибка при поиске кнопки перехода: {e}")
            return False

    async def _click_first_visible(self, selectors: list[str], debug_name: str = "") -> bool:
        """Ищет первый видимый элемент по переданным селекторам и кликает по нему"""
        for selector in selectors:
            try:
                elements = await self.page.query_selector_all(selector)
                for element in elements:
                    if await element.is_visible() and await element.is_enabled():
                        text = (await element.inner_text()).strip()
                        print(f"🖱️ Нажимаем {debug_name or text}: '{text or selector}'")
                        await element.click()
                        return True
            except Exception:
                continue
        return False

    async def process_one_conversation(self, user_number):
        """Обработка одного разговора"""
        try:
            print(f"\n👤 Начинаем разговор с пользователем #{user_number}/{self.max_users}")
            print(f"📊 Прогресс: {user_number}/{self.max_users} ({(user_number/self.max_users)*100:.1f}%)")
            
            # Список сообщений
             #messages = [
            #    "Hey love, got a SC? Add me and let's chat emily_meland",
            #    "Hey f20, Add me on snapchat and let's chat —- emily_meland",
            #    "Hi, I'm Emily. Let's go to Snapchat - emily_meland",
            #    "Hey! Want to chat on Snapchat? emily_meland",
            #    "Hi there! Add me on SC: emily_meland"
            #]

            messages = [
                "Hey F, let’s chat on a s n a p? Add me and let's chat emilymelandxxx",
                "Hey f20, Add me on snapchat and let's chat… emilymelandxxx",
                "Hi, I'm Emily. Let's go to Snapchat - emilymelandxxx",
                "Hey! Want to chat on Snapchat? emilymelandxxx",
                "Hi there! Add me on snap: emilymelandxxx"
            ]
            
            # Выбираем случайное сообщение
            message = random.choice(messages)
            
            # Отправляем сообщение (ввод занимает 4 секунды)
            if not await self.send_message(message):
                print("⚠️ Не удалось отправить сообщение, но продолжаем...")
            
            # Пауза между собеседниками 4.75 секунды
            print("⏳ Пауза 4.75 секунды...")
            await asyncio.sleep(4.75)
            
            # Переходим к следующему собеседнику (если не последний)
            if user_number < self.max_users:
                await self.find_next_button()
                # Ждем загрузки нового собеседника
                await self.page.wait_for_timeout(3000)
            
            self.message_count += 1
            print(f"✅ Разговор с пользователем #{user_number} завершен")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при обработке разговора: {e}")
            return False

    def check_proxy_ip(self):
        """Проверка IP через сервис https://api.ipify.org для проверки работы прокси"""
        try:
            # Убеждаемся, что выбран текущий прокси
            if not self.current_proxy:
                self.current_proxy = get_random_proxy()

            proxy_string = self.current_proxy["https"]
            proxy_parts = proxy_string.replace("http://", "").split("@")

            # Формируем словарь прокси для requests
            if len(proxy_parts) == 2:
                auth_part, server_part = proxy_parts
                username, password = auth_part.split(":")
                proxy_dict = {
                    "http": f"http://{username}:{password}@{server_part}",
                    "https": f"http://{username}:{password}@{server_part}"
                }
            else:
                proxy_dict = {"http": proxy_string, "https": proxy_string}

            print("🌐 Проверяем IP через https://api.ipify.org ...")
            response = requests.get("https://api.ipify.org", proxies=proxy_dict, timeout=15)
            ip_address = response.text.strip()
            print(f"📍 IP через прокси: {ip_address}")
            return True
        except Exception as e:
            print(f"❌ Не удалось получить IP через прокси: {e}")
            return False

    async def run(self):
        """Основная функция запуска для работы с несколькими пользователями"""
        try:
            print(f"🚀 Запускаем бота для общения с {self.max_users} пользователями...")
            print(f"🔒 Используем прокси: {proxy_info['host']} ({proxy_info['country']})")

            # 1. Проверяем IP через сервис api.ipify.org
            print("\n1️⃣ ПРОВЕРКА IP ЧЕРЕЗ API.IPIFY.ORG")
            print("-" * 40)
            if not self.check_proxy_ip():
                print("⚠️ Не удалось получить IP через прокси, но продолжаем...")

            # 2. Настраиваем браузер
            print("\n2️⃣ НАСТРОЙКА БРАУЗЕРА")
            print("-" * 40)
            if not await self.setup_browser_with_proxy():
                print("❌ Не удалось настроить браузер")
                return False

            # 3. Открываем сайт с повторными попытками
            print("\n3️⃣ ОТКРЫТИЕ САЙТА")
            print("-" * 40)
            if not await self.open_uhmegle_with_retry():
                print("❌ Не удалось открыть сайт")
                return False

            # 4. Ждем подключения к серверу и ищем кнопку Start
            print("\n4️⃣ ПОДКЛЮЧЕНИЕ К СЕРВЕРУ")
            print("-" * 40)
            if not await self.wait_for_connection_and_start():
                print("❌ Не удалось подключиться к серверу или найти кнопку Start")
                return False

            # 5. Ждем готовности чата
            print("\n5️⃣ ОЖИДАНИЕ ГОТОВНОСТИ ЧАТА")
            print("-" * 40)
            if not await self.wait_for_chat_ready():
                print("⚠️ Чат может быть не готов, но продолжаем...")

            # 6. Обрабатываем всех пользователей
            print("\n6️⃣ ОБРАБОТКА ПОЛЬЗОВАТЕЛЕЙ")
            print("-" * 40)

            
            for user_num in range(1, self.max_users + 1):
                try:
                    success = await self.process_one_conversation(user_num)
                    if not success:
                        print(f"⚠️ Ошибка с пользователем #{user_num}, продолжаем...")
                    
                    # Небольшая пауза между пользователями
                    if user_num < self.max_users:
                        await asyncio.sleep(1)
                        
                except Exception as e:
                    print(f"❌ Критическая ошибка с пользователем #{user_num}: {e}")
                    continue
                
            print("=" * 60)
            print(f"🎉 Обработка завершена! Отправлено сообщений: {self.message_count}/{self.max_users}")
            return True
            
        except Exception as e:
            print(f"❌ Критическая ошибка в работе бота: {e}")
            return False
        finally:
            await self.cleanup()

    async def run_without_proxy(self):
        """Запуск бота БЕЗ прокси для тестирования"""
        try:
            print(f"🚀 Запускаем бота БЕЗ ПРОКСИ для общения с {self.max_users} пользователями...")
            print("⚠️ ВНИМАНИЕ: Работа без прокси - ваш реальный IP будет виден!")
            
            # 1. Настраиваем браузер без прокси
            print("\n1️⃣ НАСТРОЙКА БРАУЗЕРА (БЕЗ ПРОКСИ)")
            print("-" * 40)
            if not await self.setup_browser_without_proxy():
                print("❌ Не удалось настроить браузер")
                return False
            
            # 2. Проверяем IP (должен быть реальный)
            print("\n2️⃣ ПРОВЕРКА IP (РЕАЛЬНЫЙ)")
            print("-" * 40)
            await self.check_ip_in_browser()
            
            # 3. Открываем сайт
            print("\n3️⃣ ОТКРЫТИЕ САЙТА")
            print("-" * 40)
            if not await self.open_uhmegle_with_retry():
                print("❌ Не удалось открыть сайт")
                return False
            
            # 4. Подключение к серверу
            print("\n4️⃣ ПОДКЛЮЧЕНИЕ К СЕРВЕРУ")
            print("-" * 40)
            if not await self.wait_for_connection_and_start():
                print("❌ Не удалось подключиться к серверу или найти кнопку Start")
                return False
            
            # 5. Ожидание готовности чата
            print("\n5️⃣ ОЖИДАНИЕ ГОТОВНОСТИ ЧАТА")
            print("-" * 40)
            if not await self.wait_for_chat_ready():
                print("⚠️ Чат может быть не готов, но продолжаем...")
            
            # 6. Обработка пользователей
            print("\n6️⃣ ОБРАБОТКА ПОЛЬЗОВАТЕЛЕЙ")
            print("-" * 40)
            
            for user_num in range(1, self.max_users + 1):
                try:
                    success = await self.process_one_conversation(user_num)
                    if not success:
                        print(f"⚠️ Ошибка с пользователем #{user_num}, продолжаем...")
                    
                    # Небольшая пауза между пользователями
                    if user_num < self.max_users:
                        await asyncio.sleep(1)
                        
                except Exception as e:
                    print(f"❌ Критическая ошибка с пользователем #{user_num}: {e}")
                    continue
                
            print("=" * 60)
            print(f"🎉 Обработка завершена! Отправлено сообщений: {self.message_count}/{self.max_users}")
            return True
            
        except Exception as e:
            print(f"❌ Критическая ошибка в работе бота: {e}")
            return False
        finally:
            await self.cleanup()

    async def cleanup(self):
        """Очистка ресурсов"""
        try:
            if self.page:
                print("🔒 Закрываем страницу...")
                await self.page.close()
                self.page = None
                
            if self.context:
                print("🔒 Закрываем контекст...")
                await self.context.close()
                self.context = None
                
            if self.browser:
                print("🔒 Закрываем браузер...")
                await self.browser.close()
                self.browser = None
                
            if self.playwright:
                print("🔒 Останавливаем Playwright...")
                await self.playwright.stop()
                self.playwright = None
                
            print("✅ Очистка завершена")
            
        except Exception as e:
            print(f"⚠️ Ошибка при очистке: {e}")
            
        # Дополнительная задержка для корректного закрытия процессов
        await asyncio.sleep(1)

async def main():
    """Главная функция"""
    print("🤖 UHMEGLE BOT - МУЛЬТИ-ПОЛЬЗОВАТЕЛЬСКАЯ ВЕРСИЯ")
    print("=" * 60)
    print("🔧 Функции:")
    print("   ✅ Отправка сообщений 35 пользователям")
    print("   ✅ Ротация прокси ProxySaver")
    print("   ✅ Автоматический переход между собеседниками")
    print("   ✅ Прогресс-бар и статистика")
    print("   ✅ Улучшенная обработка ошибок")
    print("=" * 60)
    
    print("\n🔧 Режимы работы:")
    print("1. 🔒 С прокси ProxySaver (рекомендуется)")
    print("2. 🌐 Без прокси (для тестирования)")
    print("3. 🔍 Только диагностика прокси")
    
    try:
        mode = input("\nВыберите режим (1-3, по умолчанию 1): ").strip()
        if not mode:
            mode = "1"
            
        max_users = input("Введите количество пользователей (по умолчанию 35): ").strip()
        if not max_users or not max_users.isdigit():
            max_users = 35
        else:
            max_users = int(max_users)
            
        bot = MultiUserUhmegleBot(max_users=max_users)
        
        if mode == "1":
            # Обычный режим с прокси
            await bot.run()
        elif mode == "2":
            # Режим без прокси
            await bot.run_without_proxy()
        elif mode == "3":
            # Только диагностика
            print("\n🔍 ДИАГНОСТИКА ПРОКСИ")
            print("-" * 40)
            bot.test_proxy_connection()
            bot.test_proxy_with_requests()
            bot.diagnose_proxy_issues()
        else:
            print("❌ Неверный выбор режима")
        
    except KeyboardInterrupt:
        print("\n⚠️ Программа прервана пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

def run_bot():
    """Функция запуска с правильной обработкой для Windows"""
    import warnings
    warnings.filterwarnings("ignore", category=ResourceWarning)
    
    # Устанавливаем политику событий для Windows
    if hasattr(asyncio, 'WindowsProactorEventLoopPolicy'):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
    finally:
        # Принудительная очистка всех задач
        try:
            loop = asyncio.get_event_loop()
            if not loop.is_closed():
                pending = asyncio.all_tasks(loop)
                if pending:
                    for task in pending:
                        task.cancel()
        except:
            pass

if __name__ == "__main__":
    run_bot()