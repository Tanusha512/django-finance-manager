"""
URL конфигурация для проекта django-finance-manager.

Список `urlpatterns` направляет URL к представлениям. Для получения дополнительной информации см.:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Примеры:
Представления функций
    1. Добавьте импорт: from my_app import views
    2. Добавьте URL в urlpatterns: path('', views.home, name='home')
Представления на основе классов
    1. Добавьте импорт: from other_app.views import Home
    2. Добавьте URL в urlpatterns: path('', Home.as_view(), name='home')
Включение другого URLconf
    1. Импортируйте функцию include(): from django.urls import include, path
    2. Добавьте URL в urlpatterns: path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Основные URL паттерны проекта
urlpatterns = [
    # Административная панель Django
    path('admin/', admin.site.urls),
    
    # Подключаем URL приложения finance
    # Все URL приложения finance будут доступны по корневому пути
    path('', include('finance.urls')),
    
    # Для Django Debug Toolbar (опционально)
    # path('__debug__/', include('debug_toolbar.urls')),
]

# В режиме разработки добавляем обработку статических и медиа файлов
if settings.DEBUG:
    # Обработка медиафайлов (загруженные пользователями файлы)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Обработка статических файлов (опционально, если не работает через collectstatic)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Для продакшена (комментируем в режиме разработки)
# else:
#     # Настройки для продакшена с использованием веб-сервера
#     # Статические файлы должны обслуживаться веб-сервером (nginx/apache)
#     pass