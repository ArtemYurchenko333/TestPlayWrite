import time
import random
import asyncio
import requests
from playwright.async_api import async_playwright
from proxy_auth import proxies

class PlaywrightUhmegleBot:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.message_count = 0
        
    def test_proxy_with_requests(self):
        """Проверка прокси через requests"""
        try:
            print("🔍 Тестируем прокси через requests...")
            
            proxy_string = proxies["https"]
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
                try:
                    real_ip = requests.get('https://api.ipify.org', timeout=10).text.strip()
                    print(f"🏠 Реальный IP: {real_ip}")
                except:
                    print("⚠️ Не удалось получить реальный IP")
                
                # Тест с прокси
                response = requests.get('https://api.ipify.org', proxies=proxy_dict, timeout=15)
                proxy_ip = response.text.strip()
                print(f"📍 IP через прокси: {proxy_ip}")
                
                if proxy_ip != real_ip:
                    print("✅ Прокси работает через requests!")
                    return True
                else:
                    print("❌ Прокси НЕ работает - IP не изменился")
                    return False
                    
        except Exception as e:
            print(f"❌ Ошибка при тестировании прокси через requests: {e}")
            return False

    async def setup_browser_with_proxy(self):
        """Настройка браузера с прокси"""
        try:
            print("🔧 Настраиваем браузер с прокси...")
            
            # Извлекаем данные прокси
            proxy_string = proxies["https"]
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
            
            self.playwright = await async_playwright().start()
            
            # Настройки браузера
            browser_args = [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-web-security",
                "--ignore-certificate-errors",
                "--ignore-ssl-errors",
                "--allow-running-insecure-content",
                "--disable-extensions-except",
                "--disable-plugins-discovery"
            ]
            
            # Случайный user-agent
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
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
                viewport={"width": 1280, "height": 720}
            )
            
            # Создаем страницу
            self.page = await self.context.new_page()
            
            # Маскировка автоматизации
            await self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                window.chrome = {runtime: {}};
            """)
            
            print("✅ Браузер успешно настроен с прокси")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при настройке браузера: {e}")
            return False

    async def check_ip_in_browser(self):
        """Проверка IP адреса в браузере через api.ipify.org"""
        try:
            print("🌐 Проверяем IP адрес в браузере через api.ipify.org...")
            
            await self.page.goto("https://api.ipify.org", wait_until="networkidle")
            await self.page.wait_for_timeout(3000)
            
            # Получаем IP из pre тега
            ip_element = await self.page.query_selector("pre")
            if ip_element:
                ip_address = await ip_element.inner_text()
                ip_address = ip_address.strip()
                print(f"📍 Ваш IP адрес: {ip_address}")
                
                # Проверяем, что IP отличается от реального
                if ip_address and ip_address != "185.102.186.90":  # замените на ваш реальный IP
                    print("✅ Прокси работает корректно в браузере!")
                    return True
                else:
                    print("⚠️ Прокси может не работать - показывается ваш реальный IP")
                    return False
            else:
                print("❌ Не удалось найти элемент с IP")
                return False
                
        except Exception as e:
            print(f"❌ Ошибка при проверке IP: {e}")
            return False

    async def open_uhmegle(self):
        """Открытие сайта uhmegle.com"""
        try:
            print("🌐 Открываем uhmegle.com...")
            await self.page.goto("https://uhmegle.com/", wait_until="networkidle")
            await self.page.wait_for_timeout(5000)
            
            print(f"📄 Заголовок: {await self.page.title()}")
            print(f"🔗 URL: {self.page.url}")
            
            # Переход на текстовый чат если нужно
            if "google_vignette" in self.page.url:
                print("🔄 Переходим на текстовый чат...")
                await self.page.goto("https://uhmegle.com/text/", wait_until="networkidle")
                await self.page.wait_for_timeout(5000)
                print(f"✅ Новый URL: {self.page.url}")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при открытии сайта: {e}")
            return False

    async def find_and_click_start(self):
        """Поиск и нажатие кнопки Start"""
        try:
            print("🔍 Ищем кнопку Start...")
            await self.page.wait_for_timeout(5000)
            
            # Различные селекторы для кнопки Start
            selectors = [
                'button:has-text("Start")',
                'div:has-text("Start")',
                'span:has-text("Start")',
                'button:has-text("New")',
                'div:has-text("New")',
                '[class*="start"]',
                '[class*="bottomButton"]',
                'button',
                'div[role="button"]'
            ]
            
            for selector in selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for element in elements:
                        if await element.is_visible() and await element.is_enabled():
                            text = await element.inner_text()
                            text_lower = text.strip().lower()
                            
                            start_keywords = ["start", "begin", "new", "next", "go", "continue"]
                            if any(keyword in text_lower for keyword in start_keywords):
                                print(f"✅ Найдена кнопка: '{text}'")
                                print("🖱️ Нажимаем кнопку Start...")
                                await element.click()
                                await self.page.wait_for_timeout(3000)
                                return True
                except Exception:
                    continue
            
            # Fallback: нажимаем любую доступную кнопку
            buttons = await self.page.query_selector_all('button')
            for button in buttons:
                if await button.is_visible() and await button.is_enabled():
                    print("🖱️ Нажимаем любую доступную кнопку...")
                    await button.click()
                    await self.page.wait_for_timeout(3000)
                    return True
            
            print("❌ Кнопка Start не найдена")
            return False
            
        except Exception as e:
            print(f"❌ Ошибка при поиске кнопки Start: {e}")
            return False

    async def wait_for_chat_connection(self):
        """Ожидание подключения к чату"""
        try:
            print("⏳ Ожидаем подключения к чату...")
            await self.page.wait_for_timeout(5000)
            
            # Проверяем наличие элементов чата
            chat_selectors = [
                'textarea',
                'input[type="text"]',
                '[class*="input"]',
                '[class*="chat"]'
            ]
            
            for selector in chat_selectors:
                try:
                    element = await self.page.query_selector(selector)
                    if element and await element.is_visible():
                        print("✅ Подключение к чату успешно!")
                        return True
                except:
                    continue
            
            print("⚠️ Элементы чата не найдены, но продолжаем...")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при ожидании подключения: {e}")
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
                '[class*="input"] input'
            ]
            
            input_box = None
            for selector in input_selectors:
                try:
                    input_box = await self.page.query_selector(selector)
                    if input_box and await input_box.is_visible():
                        break
                except:
                    continue
            
            if not input_box:
                print("❌ Поле ввода не найдено")
                return False
            
            # Очищаем поле и вводим текст
            await input_box.clear()
            await self.page.wait_for_timeout(500)
            
            # Вводим текст с задержкой 3 секунды (по символу)
            typing_delay = 3000 / len(message)  # Распределяем 3 секунды на весь текст
            await input_box.type(message, delay=typing_delay)
            
            await self.page.wait_for_timeout(500)
            
            # Ищем кнопку отправки
            send_selectors = [
                'button:has-text("Send")',
                'button:has-text("Отправить")',
                '[class*="send"]',
                'input[type="submit"]'
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
                print("✅ Сообщение отправлено")
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

    async def disconnect_and_cleanup(self):
        """Отключение от собеседника"""
        try:
            print("🔌 Отключаемся от собеседника...")
            
            # Сначала пробуем нажать Stop/Really/Next
            stop_selectors = [
                'button:has-text("Stop")',
                'button:has-text("Really")',
                'button:has-text("Next")',
                'div:has-text("Stop")',
                'div:has-text("Really")',
                'div:has-text("Next")',
                '[class*="stop"]',
                '[class*="really"]',
                '[class*="next"]'
            ]
            
            for selector in stop_selectors:
                try:
                    elements = await self.page.query_selector_all(selector)
                    for element in elements:
                        if await element.is_visible() and await element.is_enabled():
                            text = await element.inner_text()
                            print(f"🖱️ Нажимаем кнопку: {text}")
                            await element.click()
                            await self.page.wait_for_timeout(1000)
                except:
                    continue
            
            print("✅ Отключение завершено")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при отключении: {e}")
            return False

    async def process_one_conversation(self):
        """Обработка одного разговора"""
        try:
            print(f"\n👤 Начинаем разговор #{self.message_count + 1}")
            
            # Список сообщений
            messages = [
                "Hey love, got a SC? Add me and let's chat emily_meland",
                "Hey f20, Add me on snapchat and let's chat —- emily_meland",
                "Hi, I'm Emily. Let's go to Snapchat - emily_meland",
                "Hey! Want to chat on Snapchat? emily_meland",
                "Hi there! Add me on SC: emily_meland"
            ]
            
            # Выбираем случайное сообщение
            message = random.choice(messages)
            
            # Отправляем сообщение (ввод занимает 3 секунды)
            if not await self.send_message(message):
                return False
            
            # Пауза между собеседниками 2.75 секунды
            print("⏳ Пауза 2.75 секунды...")
            await asyncio.sleep(2.75)
            
            # Отключаемся
            await self.disconnect_and_cleanup()
            
            self.message_count += 1
            print(f"✅ Разговор #{self.message_count} завершен")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при обработке разговора: {e}")
            return False

    async def run(self):
        """Основная функция запуска"""
        try:
            print("🚀 Запускаем бота...")
            
            # 1. Проверяем прокси через requests
            if not self.test_proxy_with_requests():
                print("⚠️ Прокси не работает через requests, но продолжаем...")
            
            # 2. Настраиваем браузер
            if not await self.setup_browser_with_proxy():
                print("❌ Не удалось настроить браузер")
                return False
            
            # 3. Проверяем IP в браузере
            if not await self.check_ip_in_browser():
                print("⚠️ Проблема с прокси в браузере, но продолжаем...")
            
            # 4. Открываем сайт
            if not await self.open_uhmegle():
                print("❌ Не удалось открыть сайт")
                return False
            
            # 5. Ищем и нажимаем Start
            if not await self.find_and_click_start():
                print("❌ Не удалось найти кнопку Start")
                return False
            
            # 6. Ждем подключения к чату
            if not await self.wait_for_chat_connection():
                print("⚠️ Не удалось дождаться подключения к чату, но продолжаем...")
            
            # 7. Обрабатываем одного собеседника
            print("🔄 Начинаем обработку собеседника...")
            await self.process_one_conversation()
            
            print("🎉 Обработка завершена!")
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
    bot = PlaywrightUhmegleBot()
    
    try:
        await bot.run()
    except KeyboardInterrupt:
        print("\n⚠️ Программа прервана пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        await bot.cleanup()

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
    print("🤖 UHMEGLE BOT - PLAYWRIGHT ВЕРСИЯ")
    print("=" * 50)
    run_bot()
