import json
from typing import Dict, List, Tuple
import datetime
import aiohttp
import asyncio
import pandas as pd

from main_api.object_model import Object

def dict_to_df(dct):
    df = pd.json_normalize(dct)
    html_table = df.to_html(classes='table table-stripped')
    context = {}
    context['html_table'] = html_table
    return context

class ABCP:
    userlogin = "api@id12480"
    userpsw = "d0f938ccf1a7b3b5da427e26e2d33215"
    async def get_json(self, endpoint, **filters):
        url = f'https://id12480.public.api.abcp.ru/' + "/".join(endpoint.split("_"))
        print(url+'?'+'&'.join([f'{k}={v}' for k,v in filters.items() if k not in ['userlogin','userpsw']] ))
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=filters) as response:
                response_text = await response.text()
        return json.loads(response_text)


    async def get_list(self, endpoint, **kwargs):
        filters = {'userlogin': self.userlogin,'userpsw': self.userpsw} | kwargs
        return Object(await self.get_json(endpoint, **filters))

    async def get_pd(self, endpoint, **kwargs):
        filters = {'userlogin': self.userlogin,'userpsw': self.userpsw} | kwargs
        return dict_to_df(await self.get_json(endpoint, **filters))
    async def get_dict(self, endpoint, **kwargs):
        filters = {'userlogin': self.userlogin,'userpsw': self.userpsw} | kwargs
        return await self.get_json(endpoint, **filters)

# Pr_Lg
# /search/warehouses	GET	Получение списка складов
# https://api.pr-lg.ru/search/warehouses?secret=LRwcBJHfEWlsCekJGPievDGwhjuxbpDl&action=list
# Параметр	Тип	Описание
# secret	Строка (@string)	Ваш API-ключ (обязательный параметр)
# action	Строка (@string)	Значение: "list" (обязательный параметр)
# Выходные параметры
# Параметр	Тип	Описание
# id	Число (@int)	ID-склада во внутренней системе
# name	Строка (@string)	Наименование склада
# delivery	Строка (@string)	Срок доставки (Строка к прим. "5 дн.")
# delivery_hours	Число (@int)	Количество часов доставки
# comment	Строка (@string)	Комментарий
# own	Число (@int)	1 - Склад Профит-лиги
# 0 - Сторонний склад
# active	Число (@int)	(0/1) Активен или не ативен склад

# /search/products	GET	Получение списка доступных товаров по заданому артикулу
# https://api.pr-lg.ru/search/products?secret=LRwcBJHfEWlsCekJGPievDGwhjuxbpDl&article=2382&brand=NGK
# Параметр	Тип	Описание
# secret	Строка (@string)	Ваш API-ключ (обязательный параметр)
# article	Строка (@string)	Артикул искомого товара (обязательный параметр)
# Выходные параметры
# Параметр	Тип	Описание
# article	Строка (@string)	Артикул товара
# brand	Строка (@string)	Наименование бренда
# description	Строка (@string)	Наименование товара
# brand_warranty	Число (@int)	Присутствует гарантия на бренд
# original	Число (@int)	(0/1) Оригинальный бренд
# countProducts	Число (@int)	Суммарное количество товара на всех складах

# /search/items	GET	Поиск товаров по артикулу с наличием
# https://api.pr-lg.ru/search/items?secret=LRwcBJHfEWlsCekJGPievDGwhjuxbpDl&article=2382
# Параметр	Тип	Описание
# secret	Строка (@string)	Ваш API-ключ (обязательный параметр)
# article	Строка (@string)	Артикул искомого товара (обязательный параметр)
# Выходные параметры
# Параметр	Тип	Описание
# id	Число (@int)	ID-товара во внутренней системе
# article	Строка (@string)	Артикул товара
# brand	Строка (@string)	Наименование бренда
# description	Строка (@string)	Наименование товара
# brand_warranty	Число (@int)	Присутствует гарантия на бренд
# original	Число (@int)	(0/1) Оригинальный бренд
# products	Массив (@array)	Массив товаров распределенный по складам:
    # article_id - ID-товара во внутренней системе
    # warehouse_id - ID-поставщика во внутренней системе
    # description - описание товара в прайсе поставщика
    # product_code - Системный Код товара во внутренней системе (используется для обмена с 1С)
    # multi - кратность товара (мин. кол. в заказе)
    # quantity - количество товара на складе
    # price - цена товара за 1 ед.
    # sale - уцененный товар (0/1)
    # comment - причина уцененного товара
    # incart - количество товара которое уже находится в корзине
    # custom_warehouse_name - Наименование поставщика
    # show_date - информация о сроке поставки на склад Профит-Лига
    # delivery_time - срок поставки в часах (используется для расчета динамических сроков поставки)
    # delivery_date - дата доставки до торговой точки клиента (Для установки торговой точки воспользуйтесь соответствующим методом)
    # sort - порядок сортировки склада при выдаче
    # waitings - ожидаемое количество товара на склад от поставщика
    # allow_return - разрешение на возврат товара (0/1)
    # return_days - количество дней на подачу заявки на возврат
    # delivery_probability - вероятность поставки склада (%)

# /search/crosses	GET	Получение остатков по артикулу и бренду, с заменами запрошенного товара
# https://api.pr-lg.ru/search/crosses?secret=LRwcBJHfEWlsCekJGPievDGwhjuxbpDl&article=2382&brand=NGK
# Параметр	Тип	Описание
# secret	Строка (@string)	Ваш API-ключ (обязательный параметр)
# article	Строка (@string)	Артикул искомого товара (обязательный параметр)
# brand	Строка (@string)	Бренд искомого товара (обязательный параметр)
# replaces	Число (@int)	Возвращать с заменами искомого товара (0/1)
# Выходные параметры
# Параметр	Тип	Описание
# id	Число (@int)	ID-товара во внутренней системе
# article	Строка (@string)	Артикул товара
# brand	Строка (@string)	Наименование бренда
# description	Строка (@string)	Наименование товара
# brand_warranty	Число (@int)	Присутствует гарантия на бренд
# original	Число (@int)	(0/1) Оригинальный бренд
# products	Массив (@array)	Массив товаров распределенный по складам:
    # article_id - ID-товара во внутренней системе
    # warehouse_id - ID-поставщика во внутренней системе
    # description - описание товара в прайсе поставщика
    # product_code - Системный Код товара во внутренней системе (используется для обмена с 1С)
    # multi - кратность товара (мин. кол. в заказе)
    # quantity - количество товара на складе
    # price - цена товара за 1 ед.
    # sale - уцененный товар (0/1)
    # comment - причина уцененного товара
    # incart - количество товара которое уже находится в корзине
    # custom_warehouse_name - Наименование поставщика
    # show_date - информация о сроке поставки на склад Профит-Лига
    # delivery_time - срок поставки в часах (используется для расчета динамических сроков поставки)
    # delivery_date - дата доставки до торговой точки клиента (Для установки торговой точки воспользуйтесь соответствующим методом)
    # sort - порядок сортировки склада при выдаче
    # waitings - ожидаемое количество товара на склад от поставщика
    # allow_return - разрешение на возврат товара (0/1)
    # return_days - количество дней на подачу заявки на возврат
    # delivery_probability - вероятность поставки склада (%)

# /cart/add	POST	Добавление товара в корзину
# Параметр	Тип	Описание
# secret	Строка (@string)	Ваш API-ключ (обязательный параметр)
# id	Число (@int)	ID-товара во внутренней системе (обязательный параметр)
# warehouse	Число (@int)	ID-поставщика во внутренней системе (обязательный параметр)
# quantity	Число (@int)	Количество добавляемое в корзину (обязательный параметр)
# code	Строка (@string)	Системный Код товара во внутренней системе (используется для обмена с 1С) (обязательный параметр)
# comment	Строка (@string)	Комментарий к товару (максимум 255 символов)
# Выходные параметры
# Параметр	Тип	Описание
# status	Строка (@string)	Статус выполнения:
# success - успешно добавлено
# no-quantity - указаное количество превышает наличие на складе
# less - указаное количество меньше, либо равно нулю
# error - ошибка добавления в корзину (товар неопределен, несоответствует кратность, ошибка записи)
# total	Дробное число (@float)	Сумма товаров в корзине
# count	Число (@int)	Общее количество всех товаров в корзине

# /cart/list	GET	Получение списка товаров в корзине
# https://api.pr-lg.ru/cart/list?secret=LRwcBJHfEWlsCekJGPievDGwhjuxbpDl
# Параметр	Тип	Описание
# secret	Строка (@string)	Ваш API-ключ (обязательный параметр)
# Выходные параметры
# Параметр	Тип	Описание
# article	Строка (@string)	Артикул товара
# brand	Строка (@string)	Бренд товара
# description	Строка (@string)	Наименование товара
# article_id	Число (@int)	ID-товара во внутренней системе
# warehouse_id	Число (@int)	ID-поставщика во внутренней системе
# product_code	Число (@int)	Системный Код товара во внутренней системе (используется для обмена с 1С)
# multi	Число (@int)	Кратность товара (мин. кол. в заказе)
# quantity	Число (@int)	Количество товара на складе
# price	Дробное число (@float)	Цена товара за 1 ед.
# sale	Число (@int)	Уцененный товар (0-нет, 1-да)
# comment	Строка (@string)	Причина уцененного товара
# incart	Число (@int)	Количество товара которое уже находится в корзине
# warehouse	Строка (@string)	Наименование поставщика
# show_date	Строка (@string)	Информация о сроке поставки на склад Профит-Лига
# sort	Число (@int)	порядок сортировки склада при выдаче
# allow_return	Число (@int)	Возможен возврат товара поставщику (1-да, 0-нет)

# /cart/remove	POST	Удаление товара из корзины
# Параметр	Тип	Описание
# secret	Строка (@string)	Ваш API-ключ (обязательный параметр)
# id	Число (@int)	ID-товара во внутренней системе (article_id в списке товаров корзины)
# warehouse	Число (@int)	ID-поставщика во внутренней системе (обязательный параметр)
# Выходные параметры
# Параметр	Тип	Описание
# status	Строка (@string)	Статус выполнения:
# cart-success - успешно удалено
# cart-error - ошибка при удалении из корзины
# total	Дробное число (@float)	Сумма товаров в корзине
# count	Число (@int)	Общее количество всех товаров в корзине

# /cart/point	POST	Установка торговой точки по-умолчанию
# Параметр	Тип	Описание
# secret	Строка (@string)	Ваш API-ключ (обязательный параметр)
# code	Строка (@string)	Код торговой точки, может быть получен при запросе метода "Настройки заказа"
# Выходные параметры
# Параметр	Тип	Описание
# status	Строка (@string)	Статус установки торговой точки (success|error)
# err	Строка (@string)	Описание ошибки

# /cart/params	GET	Получение настроек заказа
# https://api.pr-lg.ru/cart/params?secret=LRwcBJHfEWlsCekJGPievDGwhjuxbpDl
# Параметр	Тип	Описание
# secret	Строка (@string)	Ваш API-ключ (обязательный параметр)
# Выходные параметры
# Параметр	Тип	Описание
# methods	Массив (@array)	Список способов получения товара:
# id - ID способа доставки
# name - Наименование способа доставки
# points	Массив (@array)	Список доступных адресов доставки:
# code - Код торговой точки в системе
# point - Наименование торговой точки в системе
# address - Фактический адрес торговой точки
# pickup_points	Массив (@array)	Список доступных адресов самовывоза:
# code - Код точки самовывоза в системе
# name - Наименование точки самовывоза в системе
# address - Фактический адрес точки самовывоза
# payment	Массив (@array)	Список способов оплаты:
# id - ID способа оплаты
# name - Наименование способа оплаты
# statuses	Массив (@array)	Список статусов заказа:
# id - ID статуса
# name - Наименование статуса
# description - Расшифровка статуса

# /cart/order	POST	Формирование заказа из корзины
# Параметр	Тип	Описание
# secret	Строка (@string)	Ваш API-ключ (обязательный параметр)
# method	Число (@int)	ID способа доставки (обязательный параметр)
# payment	Число (@int)	ID способа оплаты (обязательный параметр)
# point	Строка (@string)	Код торговой точки из массива настроек (обязателен при доставке)
# address	Строка (@string)	Фактический адрес торговой точки из массива настроек (обязателен при доставке)
# pickup_point	Строка (@string)	Код точки самовывоза из массива настроек (обязателен при выборе в качетве доставки самовывоз)
# Выходные параметры
# Параметр	Тип	Описание
# status	Строка (@int)	Результат выполнения:
# success - успешно сохранено
# error - ошибка при сохранении
# orders	Массив (@array)	Список номеров созданных заказов (может остутствовать)
# err	Строка (@int)	Описание ошибки (может остутствовать)

# /orders/list	GET	Получение списка заказов
# Параметр	Тип	Описание
# secret	Строка (@string)	Ваш API-ключ (обязательный параметр)
# page	Число (@int)	Номер страницы
# order_id	Строка (@string)	Номер заказа. Можно указать несколько заказов через запятую (максимум 3 заказа в одном запросе)
# status_id	Число (@int)	ID статуса заказа. Список статусов можно получить с помощью получения параметров заказа /cart/params
# date_start	Строка (@string)	Фильтр даты начала списка. Формат даты "YYYY-MM-DD" (На данный момент времени эта функция отключена)
# date_end	Строка (@string)	Фильтр даты окончания списка. Формат даты "YYYY-MM-DD" (На данный момент времени эта функция отключена)
# Выходные параметры
# Параметр	Тип	Описание
# pages	Строка (@int)	Общее кол-во страниц
# currentPage	Строка (@int)	Текущая страница
# pageSize	Строка (@int)	Элементов на странице
# data	Массив (@array)	Массив заказов:
    # order_id - ID (номер) заказа
    # comment - Комментарий к заказу
    # datetime - Дата и время формирования заказа
    # delivery_date - Срок доставки до торговой точки
    # point_code - Системный код торговой точки во внутренней системе (используется для обмена с 1С)
    # delivery_point_id - ID торговой точки доставки
    # point_name - Название тороговой точки
    # point_delivery_address - Адрес доставки
    # delivery_name - Тип доставки
    # delivery_method_id - ID типа доставки
    # payment_id - Тип оплаты
    # payment_name - Название типа оплаты
    # products - Массив товаров заказа:
        # id - ID (номер) товара в заказе во внутренней системе
        # article_id - ID-товара во внутренней системе
        # product_code - Системный Код товара во внутренней системе (используется для обмена с 1С)
        # price - Цена (руб.)
        # quantity - Кол-во
        # comment - Комментарий к товару в заказе
        # article - Артикул товара
        # brand - Производитель
        # description - Наименование
        # status_id - ID (номер) статуса товара в заказе
        # status - Статус товара в заказе
        # status_description - Расшифровка статуса
        # status_update - Дата обновления статуса
        # custom_warehouse_name - Наименование поставщика
        # show_date - информация о сроке поставки на склад Профит-Лига
        # sale - уцененный товар (0/1)

class Pr_Lg:
    API_KEY = "LRwcBJHfEWlsCekJGPievDGwhjuxbpDl"
    async def get_json(self, endpoint, **filters):
        url = f'https://api.pr-lg.ru/search/{endpoint}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=filters) as response:
                response_text = await response.text()
        return json.loads(response_text)


    async def get_list(self, endpoint, **kwargs):
        filters = {'secret': self.API_KEY} | kwargs
        return Object(await self.get_json(endpoint, **filters))

    async def get_pd(self, endpoint, **kwargs):
        filters = {'secret': self.API_KEY} | kwargs
        return dict_to_df(await self.get_json(endpoint, **filters))



import zeep
from zeep import Client, helpers

#  http://api.rossko.ru/
# Сервис для оформления заказа.
#
# При выборе курьерской доставки стоит помнить, что существует минимальная сумма для её осуществления.
# Информацию о минимальной сумме смотрите на портале своего филиала или в ответном сообщении сервиса (в случае неудачи).
#
# Для тестирования данного сервиса включите соответствующую настройку в настройках личного кабинета на портале.
# Все заказы совершенные в режиме тестирования будут удалены через 24 часа. Информация о таких заказах доступна исключительно в сервисе GetOrders.
# Нигде более она фигурировать не будет.
#
# Параметры запроса
# Параметр	Тип	Обязателен	Описание
# KEY1	string	Да	Ключ авторизации (1).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: cba94510b02ecccef994b52711c84413
# KEY2	string	Да	Ключ авторизации (2).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: 8c7b4ba7acc716fe5bd7a80c513ad930
# delivery	array	Да	Содержит в себе информацию о доставке
    # delivery_id	integer	Да	Идентификатор доставки.
    # Можно посмотреть в сервисе GetCheckoutDetails
    # address_id	string		Идентификатор адреса доставки. Поле является обязательным, если тип доставки не равен самовывозу.
    # Можно посмотреть в сервисе GetCheckoutDetails
# payment	array	Да	Содержит в себе информацию о способе оплаты
    # payment_id	integer	Да	Идентификатор оплаты.
    # Можно посмотреть в сервисе GetCheckoutDetails
    # requisite_id	integer		Идентификатор реквизитов. Поле является обязательным, если тип оплаты - оплата картой и тип доставки не равен самовывозу.
    # Можно посмотреть в сервисе GetCheckoutDetails
# contact	array	Да	Содержит в себе информацию о контактных данных
    # name	string	Да	ФИО покупателя
    # phone	string	Да	Контактный номер
    # comment	string		Комментарий к заказу для оператора
# delivery_parts	boolean	Да	Доставлять заказ по частям или нет
# PARTS	array	Да	Содержит в себе элемент Part
    # Part	array	Да	Содержит в себе список заказываемой номенклатуры
        # partnumber	string	Да	Артикул номенклатуры. Можно посмотреть в сервисе GetSearch
        # brand	string	Да	Наименование производителя. Можно посмотреть в сервисе GetSearch
        # stock	string	Да	Необходимый склад. Можно посмотреть в сервисе GetSearch
        # count	integer	Да	Необходимое количество
        # comment	string		Комментарий к позиции в заказе. Ограничение 50 символов.

#  http://api.rossko.ru/service/v2.1/GetOrders
# Сервис для получения изменений по заказам. Настоятельно рекомендуем получать информацию о заказах исключительно по идентификаторам.
# Получить информацию можно:
# - по id заказа
# - по списку id
# - за период start_date - end_date
# - последние N заказов
# - заказы с определенным статусом
#
# Параметры запроса
# Параметр	Тип	Обязателен	Описание
# KEY1	string	Да	Ключ авторизации (1).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: cba94510b02ecccef994b52711c84413
# KEY2	string	Да	Ключ авторизации (2).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: 8c7b4ba7acc716fe5bd7a80c513ad930
# order_ids	array		Содержит в себе элемент id
# id	integer		Номер заказа
# limit	integer		Если не указывать идентификаторы заказов, но указать лимит, вернется список последних N заказов. Можно группировать с параметром type. По умолчанию 20, не может превышать 500.
# type	integer		Тип заказов, которые хотелось бы получить. Можно группировать с интервалом времени
# Возможные варианты:
#    1 - неподтвержденные
#    2 - неукомплектованные
#    3 - несобранные
#    4 - неотгруженные
# start_date	date		Дата начала выборки. Дата указывается в формате Y-m-d (2017-05-31)
# end_date	date		Дата конца выборки (включительно). Дата указывается в формате Y-m-d (2017-05-31). При указании данного параметра - параметр start_date обязателен

#  http://api.rossko.ru/service/v2.1/GetCheckoutDetails
# Позволяет показать способы доставки и оплаты, адреса доставки, реквизиты.
# Адреса доставок и реквизиты заполняются в личном кабинете на портале.
#
# Параметры запроса
# Параметр	Тип	Обязателен	Описание
# KEY1	string	Да	Ключ авторизации (1).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: cba94510b02ecccef994b52711c84413
# KEY2	string	Да	Ключ авторизации (2).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: 8c7b4ba7acc716fe5bd7a80c513ad930

#  http://api.rossko.ru/service/v2.1/GetDeliveryDetails
# Позволяет получить волны доступных доставок.
#
# Важно! Для экспресс доставки выдается только одна волна, но она динамическая и зависит от времени обращения к сервису.
# Ориентироваться нужно на время, до которого требуется оформить заказ (timeLimit).
#
# Параметры запроса
# Параметр	Тип	Обязателен	Описание
# KEY1	string	Да	Ключ авторизации (1).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: cba94510b02ecccef994b52711c84413
# KEY2	string	Да	Ключ авторизации (2).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: 8c7b4ba7acc716fe5bd7a80c513ad930
# date	date	Да	Дата на которую необходимо получить информацию. Формат даты Y-m-d
# address_id	integer	Да	Адрес доставки. Можно посмотреть в сервисе GetCheckoutDetails

#  http://api.rossko.ru/service/v2.1/GetSearch
# Данный сервис используется для поиска номенклатуры.
# Дополнительно (через персонального менеджера) можно подключить\отключить - аналоги; аналоги не в наличии; предложения сторонних поставщиков.
#
# Сервис имеет минутные и дневные лимиты, при достижении которых перестает отвечать.
#
# Параметры запроса
# Параметр	Тип	Обязателен	Описание
# KEY1	string	Да	Ключ авторизации (1).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: cba94510b02ecccef994b52711c84413
# KEY2	string	Да	Ключ авторизации (2).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: 8c7b4ba7acc716fe5bd7a80c513ad930
# text	string	Да	Поисковая строка. Принимает на вход любые фразы.
# Для оптимального поиска используйте - артикул; артикул + бренд; код номенклатуры.
# Пример: KYB 333114
# delivery_id	string	Да	Тип доставки.
# Можно посмотреть в сервисе GetCheckoutDetails
# address_id	integer		Адрес доставки. Поле является обязательным, если тип доставки не равен самовывозу.
# Можно посмотреть в сервисе GetCheckoutDetails

#  http://api.rossko.ru/service/v2.1/GetSettlements
# Данный сервис используется для получения информации по взаиморасчетам и реализациям.
#
# Реализации выводятся с лимитом (20) на страницу. Для просмотра других результатов используйте параметр offset.
#
# Параметры запроса
# Параметр	Тип	Обязателен	Описание
# KEY1	string	Да	Ключ авторизации (1).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: cba94510b02ecccef994b52711c84413
# KEY2	string	Да	Ключ авторизации (2).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: 8c7b4ba7acc716fe5bd7a80c513ad930
# contractor	string		Идентификатор конкретного контрагента, если у вас их несколько.
# Получить и сохранить можно при первом обращении в сервис GetSettlements.
# Пример: 3db1ebdd-a33c-12e2-t597-66e541e1f9ed
# offset	integer		Смещение относительно кол-ва результатов (20) на страницу.
# startDate	date		Дата начала выборки. Дата указывается в формате Y-m-d (2017-05-31).
# При указании данного параметра - параметр endDate обязателен.
# endDate	date		Дата конца выборки (включительно). Дата указывается в формате Y-m-d (2017-05-31).
# При указании данного параметра - параметр startDate обязателен.
# status	string		Выборка реализаций по статусу. Возможные варианты:
#    Проведено
#    Оплачено
#    Не оплачено
#    Просрочено
#    Обрабатывается

#  http://api.rossko.ru/service/v2.1/GetBrokenWave
# Данный сервис используется для получения/удаления информации по недоступным волнам доставки.
# При совершении заказа через API - такие волны не будут выбираться для ближайшей доставки, будет выбрана следующая доступная волна.
#
# Для появления заблокированной волны достаточно отсутствовать на месте во время доставки.
#
# Параметры запроса
# Параметр	Тип	Обязателен	Описание
# KEY1	string	Да	Ключ авторизации (1).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: cba94510b02ecccef994b52711c84413
# KEY2	string	Да	Ключ авторизации (2).
# Можно получить в личном кабинете или через персонального менеджера.
# Пример: 8c7b4ba7acc716fe5bd7a80c513ad930
# guid_list	array		Список идентификаторов недоступных волн, которые необходимо разблокировать.
# Пример: 3db1ebdd-a33c-12e2-t597-66e541e1f9ed

class RosskoAPI:
    WSDL_URL = 'http://api.rossko.ru/service/v2.1/{}?wsdl'
    key1 = 'aaa6fde614635bf8f263adedee84b652'
    key2 = '4d51529e43c34caced946d8c5c290b72'

    def __init__(self, service_name: str) -> None:
        self.client = Client(self.WSDL_URL.format(service_name))

    async def get_json(self, endpoint, **filters):
        match endpoint:
            case 'GetCheckout':
                return dict(await self.get_checkout(**filters))
            case 'GetOrders':
                return dict(await self.get_orders(**filters))
            case 'GetSearch':
                return dict(await self.get_search(**filters))
            case 'GetDeliveryDetails':
                return dict(await self.get_delivery_details(**filters))
            case 'GetCheckoutDetails':
                return dict(await self.get_checkout_details())
            case 'GetSettlements':
                return dict(await self.get_settlements(**filters))
            case 'GetBrokenWave':
                return dict(await self.get_broken_wave())
            case _:
                return [{'-': '-'}]
    async def get_pd(self, endpoint, **kwargs):
        return dict_to_df(await self.get_json(endpoint, **kwargs))


    async def get_checkout(
            self,
            delivery_id: int,
            address_id: int,
            payment_id: int,
            requisite_id: int,
            name: str,
            phone: str,
            comment: str,
            parts: List[Dict[str, str]]
    ) -> str:
        delivery = {
            'delivery_id': delivery_id,
            'address_id': address_id
        }
        payment = {
            'payment_id': payment_id,
            'requisite_id': requisite_id
        }
        contact = {
            'name': name,
            'phone': phone,
            'comment': comment
        }
        delivery_parts = True
        PARTS = {'Part': parts}
        response = self.client.service.GetCheckout(
            KEY1=self.key1,
            KEY2=self.key2,
            delivery=delivery,
            payment=payment,
            contact=contact,
            delivery_parts=delivery_parts,
            PARTS=PARTS
        )
        return helpers.serialize_object(response, dict)

    async def get_orders(self,
                         order_ids: List[int] = [],
                         limit: int = None,
                         _type: int = None,
                         start_date: str = '',
                         end_date: str = datetime.datetime.now().strftime("%Y-%m-%d")) -> str:
        response = self.client.service.GetOrders(
            KEY1=self.key1,
            KEY2=self.key2,
            order_ids=order_ids,
            limit=limit,
            type=_type,
            start_date=start_date,
            end_date=end_date
        )
        return helpers.serialize_object(response, dict)

    async def get_checkout_details(self) -> str:
        response = self.client.service.GetCheckoutDetails(KEY1=self.key1, KEY2=self.key2)
        return helpers.serialize_object(response, dict)

    async def get_delivery_details(self, date: str, address_id: int) -> str:
        response = await self.client.service.GetDeliveryDetails(KEY1=self.key1, KEY2=self.key2,
                                                                date=date, address_id=address_id)
        return helpers.serialize_object(response, dict)

    async def get_search(self, text: str, delivery_id: str, address_id: int = None) -> str:
        response = self.client.service.GetSearch(KEY1=self.key1, KEY2=self.key2, text=text,
                                                 delivery_id=delivery_id, address_id=address_id)
        return helpers.serialize_object(response, dict)

    async def get_settlements(self, contractor: str = '', offset: int = None, startDate: str = '',
                              endDate: str = datetime.datetime.now().strftime("%Y-%m-%d"), status: str = '') -> str:
        response = self.client.service.GetSettlements(KEY1=self.key1, KEY2=self.key2, contractor=contractor,
                                                      offset=offset, startDate=startDate, endDate=endDate,
                                                      status=status)
        return helpers.serialize_object(response, dict)

    async def get_broken_wave(self, guid_list: List[int] = []) -> str:
        response = self.client.service.GetBrokenWave(KEY1=self.key1, KEY2=self.key2, guid_list=guid_list)
        return helpers.serialize_object(response, dict)

# https://автосоюз.рф/Content/Page/576
# Получение брендов по артикулу
#
# HTTP метод
#
# GET
#
# URL запроса
#
# /SearchService/GetBrands?article={article}&withoutTransit={true/false}
#
# Заголовки запроса
#
# Authorization: Basic {credentials}
# Accept: application/json
# Content-type: application/json
#
# Параметры запроса
#
# (Все параметры обязательные!)
#
# article – Артикул (тип string)
#
# withoutTransit – Не возвращать транзитных поставщиков (тип Bool)
#
# Ответ
#
# JSON, коллекция объектов следующей структуры:
#
# "Article": "333305"
#
# Артикул детали
#
# String
#
# "Brand": "KYB"
#
# Производитель (бренд)
#
# String
#
# "Description": "Амортизатор
#
# Описание детали
#
# String
#
#
#
#
#
# Получение результатов по артикулу и бренду
#
# HTTP метод
#
# GET
#
# URL запроса
#
# /SearchService/GetParts?article={article}&brand={brand}&withoutTransit={true/false}
#
# Заголовки запроса
#
# Authorization: Basic {credentials}
# Accept: application/json
# Content-type: application/json
#
# Параметры запроса
#
# (Все параметры обязательные!)
#
# article – Артикул (тип string)
#
# brand – Бренд (тип string)
#
# withoutTransit – Не возвращать транзитных поставщиков (тип Bool)
#
# Ответ
#
# JSON, коллекция объектов следующей структуры:
#
# «Article»: «334826»
#
# Артикул детали
#
# String
#
# «Brand»: «KYB»
#
# Производитель (бренд)
#
# String
#
# «CostSale»: 1234
#
# Цена продажи
#
# Double
#
# «Count»: 10
#
# Количество
#
# Short
#
# «CountText»: >10
#
# Количество в текстовом виде	String
# «Description»: «Амортизатор»
#
# Описание детали
#
# String
#
# «IsAllowDiscountRefund»:true
#
# Признак возможности возрата детали поставщику
#
# Bool
#
# «IsAnalog»: false
#
# Признак аналога на искомую деталь
#
# Bool
#
# «IsDefective»: false
#
# Признак уцененного товара
#
# Bool
#
# «IsOriginal»: false
#
# Признак оригинального производителя
#
# Bool
#
# «IsWarehouse»: true
#
# Принадлежность товара собственному складу
#
# Bool
#
# «MinCount»: 2
#
# Кратность или партийность товара в шт.
#
# Int?
#
# «SupplierColor»: #6adafc
#
# Цвет заливки строки на сайте
#
# String
#
# «SupplierLastUpdate»:
#
# Дата обновления прайса
#
# String
#
# «SupplierName»: «АВТОСОЮЗ»
#
# Название поставщика
#
# String
#
# «SupplierPercent»: 97
#
# Вероятность поставки	Int?
# «SupplierTimeMax»: 0
#
# Максимальный гарантированный срок поставки в часах
#
# Short?
#
# «SupplierTimeMin»: 24
#
# Минимальный ожидаемый срок поставки в часах
#
# Short?
#
#
#
# РАБОТА С ЗАКАЗАМИ
# Отправка товаров в заказ (без отправки в корзину)
#
# HTTP метод
#
# GET
#
# URL запроса
#
# /SearchService/AddOrder?items=[array of items]
#
# Заголовки запроса
#
# Authorization: Basic {credentials}
# Accept: application/json
# Content-type: application/json
#
# Параметры запроса
#
# (Все параметры обязательные!)
#
# items – Массив объектов вида:
#
# [{
#
# article – Артикул (тип string),
#
# brand – Бренд (тип string),
#
# SupplierName – имя поставщика (тип string),
#
# CostSale – цена товара (тип double),
#
# Quantity – количество единиц товара (тип int),
#
# SupplierTimeMin – минимальный срок поставки в часах (тип int),
#
# SupplierTimeMax – максимальный срок поставки в часах (тип int),
#
# Comment – комментарий к позиции (тип string),
#
# GioID – уникальный идентификатор позиции в вашей системе (тип int)
#
# },{..}, …]
#
# Внимание! Параметр необходимо кодировать в строку URL-адреса!
#
# Ответ
#
# JSON, коллекция объектов следующей структуры:
#
# "AddToOrderResult": true
#
# Признак создания заказа
#
# Bool
#
# "AddToOrderStatus": "Ожидает обработки"
#
# Текущий статус позиции в заказе
#
# String
#
# "OrderID": 1234
#
# Номер заказа данной позиции
#
# String
#
# "GioId": 12345
#
# Идентификатор позиции в вашей системе
#
# int
#
#
#
#
#
# Получение информации о статусах заказа
#
# HTTP метод
#
# GET
#
# URL запроса
#
# /SearchService/GetPositionsByOrder/{orderId}
#
# Заголовки запроса
#
# Authorization: Basic {credentials}
#
# Accept: application/json
#
# Content-type: application/json
#
# Параметры запроса
#
# orderId - номер заказа в нашей системе (тип int)
#
# Ответ
#
# JSON, коллекция объектов следующей структуры:
#
# «Article»: 333305
#
# Артикул детали
#
# String
#
# «Brand»: KYB
#
# Производитель (бренд)
#
# String
#
# «CostSale»: 123
#
# Цена продажи
#
# Double
#
# «Count»: 1
#
# Количество
#
# Short
#
# «DateAdded»: /Date(1543900279493)/
#
# Дата заказа
#
# DateTime
#
# «DeliveryTimeMax»: 0
#
# Максимальный гарантированный срок поставки в часах
#
# Short?
#
# «DeliveryTimeMin»: 24
#
# Минимальный ожидаемый срок поставки в часах
#
# Short?
#
# «Description»: «Амортизатор»
#
# Описание детали
#
# String
#
# «Id»: «334826»
#
# Номер позиции в заказе
#
# Int
#
# «Status»
#
# Информация по статусу позиции
#
# Object
#
# «SubOrderId»: «4334826»
#
# Номер заказа
#
# Int
#
# «Sum»: 123
#
# Сумма
#
# Double
#
# «SupplierName »: «АВТОСОЮЗ»
#
# Название поставщика
#
# String
#
# Object Status
#
# «Id»: «5334826»
#
# Номер статуса
#
# Int
#
# «CategoryId»: «0»
#
# Категория статуса
#
# Short
#
# «Name»: «Принят»
#
# Наименование статуса
#
# String
#
# «Color»: #6adafc
#
# Цвет статуса
#
# String
#
# «Date»: /Date(1543900279493)/
#
# Дата установки статуса
#
# DateTime
#
# «IsCompletedLabel»: «334826»
#
# Признак конечного статуса
#
# Bool
#
#
#
# РАБОТА С КОРЗИНОЙ
# Отправка товара в корзину на сайте
#
# HTTP метод
#
# GET
#
# URL запроса
#
# /SearchService/AddToBasket?article={Article}&brand={Brand}&supplierName={SupplierName}&costSale={CostSale}&quantity={Count}&supplierTimeMin={SupplierTimeMin}&supplierTimeMax={SupplierTimeMax}&comment={comment}
#
# Заголовки запроса
#
# Authorization: Basic {credentials}
# Accept: application/json
# Content-type: application/json
#
# Параметры запроса
#
# (Все параметры обязательные!)
#
# article – Артикул (тип string)
#
# brand – Бренд (тип string)
#
# supplierName – имя поставщика (тип string)
#
# costSale – цена товара (тип double)
#
# quantity – количество единиц товара (тип int)
#
# supplierTimeMin – минимальный срок поставки в часах (тип int)
#
# supplierTimeMax – максимальный срок поставки в часах (тип int)
#
# comment – комментарий к позиции (тип string)
#
# Ответ
#
# "Ok" – товар добавлен.
#
# "Value is not acceptable for article" -  неверно задан артикул
#
# "Value is not acceptable for brand" - неверно задан бренд
#
# "Value is not acceptable for supplierName" - неверно задано название поставщика
#
# "Value is not acceptable for costSale" - неверно задана цена
#
# "Value is not acceptable for quantity" - неверно задано количество
#
# "Quantity is more than the supplier stock" - Количество больше чем в наличии у транзитного поставщика
# "Quantity does not match MinCount" - Количество не соответствует кратности товара
#
# "Undefined Error" – невозможно добавить позицию по другим причинам
#
#
#
#
#
# Получение информации о позициях в корзине
#
# HTTP метод
#
# GET
#
# URL запроса
#
# /SearchService/GetBasket
#
# Заголовки запроса
#
# Authorization: Basic {credentials}
# Accept: application/json
# Content-type: application/json
#
# Параметры запроса
#
#
# Ответ
#
# JSON, коллекция объектов следующей структуры:
#
# «Article»: 333305
#
# Артикул детали
#
# String
#
# «Brand»: KYB
#
# Производитель (бренд)
#
# String
#
# «Comment»: «комментарий»
#
# Комментарий клиента
#
# String?
#
# «Cost»: 123
#
# Цена продажи
#
# Double
#
# «Count»: 1
#
# Количество
#
# Short
#
# «Description»: «Амортизатор»
#
# Описание детали
#
# String
#
# «Id»: «17473452»
#
# Номер позиции в корзине
#
# Int
#
# «MinCount»: 0
#
# Кратность или партийность товара в шт.
#
# Int?
#
# «SupCode»: «АВТОСОЮЗ»
#
# Название поставщика
#
# String
#
# «SupTimeMax»: 0
#
# Максимальный гарантированный срок поставки в часах
#
# Short?
#
# «SupTimeMin»: 24
#
# Минимальный ожидаемый срок поставки в часах
#
# Short?
#
#
#
# Изменение комментария позиции в корзине
#
# HTTP метод
#
# POST
#
# URL запроса
#
# /SearchService/ChangeBasketPositionComment?positionId={positionId}&comment={comment}
#
# Заголовки запроса
#
# Authorization: Basic {credentials}
# Accept: application/json
# Content-type: application/json
#
# Параметры запроса
#
# positionId – Номер позиции в корзине (Int)
#
# comment – Новый комментарий (String)
#
# Ответ
#
# JSON, коллекция объектов следующей структуры:
#
# «Article»: 333305
#
# Артикул детали
#
# String
#
# «Brand»: KYB
#
# Производитель (бренд)
#
# String
#
# «Comment»: «комментарий»
#
# Комментарий клиента
#
# String?
#
# «Cost»: 123
#
# Цена продажи
#
# Double
#
# «Count»: 1
#
# Количество
#
# Short
#
# «Description»: «Амортизатор»
#
# Описание детали
#
# String
#
# «Id»: «17473452»
#
# Номер позиции в корзине
#
# Int
#
# «MinCount»: 0
#
# Кратность или партийность товара в шт.
#
# Int?
#
# «SupCode»: «АВТОСОЮЗ»
#
# Название поставщика
#
# String
#
# «SupTimeMax»: 0
#
# Максимальный гарантированный срок поставки в часах
#
# Short?
#
# «SupTimeMin»: 24
#
# Минимальный ожидаемый срок поставки в часах
#
# Short?
#
#
#
# Изменение количества позиции в корзине
#
# HTTP метод
#
# POST
#
# URL запроса
#
# /SearchService/ChangeBasketPositionCount?positionId={positionId}&count={count}
#
# Заголовки запроса
#
# Authorization: Basic {credentials}
# Accept: application/json
# Content-type: application/json
#
# Параметры запроса
#
# positionId – Номер позиции в корзине (Int)
#
# count – Новое количество (Short)
#
# Ответ
#
# JSON, коллекция объектов следующей структуры:
#
# «Article»: 333305
#
# Артикул детали
#
# String
#
# «Brand»: KYB
#
# Производитель (бренд)
#
# String
#
# «Comment»: «комментарий»
#
# Комментарий клиента
#
# String?
#
# «Cost»: 123
#
# Цена продажи
#
# Double
#
# «Count»: 1
#
# Количество
#
# Short
#
# «Description»: «Амортизатор»
#
# Описание детали
#
# String
#
# «Id»: «17473452»
#
# Номер позиции в корзине
#
# Int
#
# «MinCount»: 0
#
# Кратность или партийность товара в шт.
#
# Int?
#
# «SupCode»: «АВТОСОЮЗ»
#
# Название поставщика
#
# String
#
# «SupTimeMax»: 0
#
# Максимальный гарантированный срок поставки в часах
#
# Short?
#
# «SupTimeMin»: 24
#
# Минимальный ожидаемый срок поставки в часах
#
# Short?
#
#
#
# Удаление позиции из корзины
#
# HTTP метод
#
# POST
#
# URL запроса
#
# /SearchService/RemoveBasketPosition?positionId={positionId}
#
# Заголовки запроса
#
# Authorization: Basic {credentials}
# Accept: application/json
# Content-type: application/json
#
# Параметры запроса
#
# positionId – Номер позиции в корзине (Int)
#
# Ответ
#
# JSON, коллекция объектов следующей структуры:
#
# «Article»: 333305
#
# Артикул детали
#
# String
#
# «Brand»: KYB
#
# Производитель (бренд)
#
# String
#
# «Comment»: «комментарий»
#
# Комментарий клиента
#
# String?
#
# «Cost»: 123
#
# Цена продажи
#
# Double
#
# «Count»: 1
#
# Количество
#
# Short
#
# «Description»: «Амортизатор»
#
# Описание детали
#
# String
#
# «Id»: «17473452»
#
# Номер позиции в корзине
#
# Int
#
# «MinCount»: 0
#
# Кратность или партийность товара в шт.
#
# Int?
#
# «SupCode»: «АВТОСОЮЗ»
#
# Название поставщика
#
# String
#
# «SupTimeMax»: 0
#
# Максимальный гарантированный срок поставки в часах
#
# Short?
#
# «SupTimeMin»: 24
#
# Минимальный ожидаемый срок поставки в часах
#
# Short?
#
#
#
# Очистка корзины
#
# HTTP метод
#
# POST
#
# URL запроса
#
# /SearchService/ClearBasket
#
# Заголовки запроса
#
# Authorization: Basic {credentials}
# Accept: application/json
# Content-type: application/json
#
# Параметры запроса
#
#
# Ответ
#
# JSON объект следующей структуры:
#
# "IsSuccess": true
#
# Признак успешной очистки
#
# Bool
#
#
#
# Получение реквизитов для оформления корзины в заказ
#
# HTTP метод
#
# POST
#
# URL запроса
#
# /SearchService/GetCheckoutParams
#
# Заголовки запроса
#
# Authorization: Basic {credentials}
# Accept: application/json
# Content-type: application/json
#
# Параметры запроса
#
#
# Ответ
#
# JSON объект следующей структуры:
#
# «Deliveries»
#
# Типы доставки
#
# Object
#
# «Payments»
#
# Типы оплаты
#
# Object
#
# Object Deliveries коллекция объектов следующей структуры:
#
# «DeliveryTypeId»: 1
#
# Код типа доставки
#
# Short
#
# «Name»:«Самовывоз»
#
# Имя типа доставки
#
# String
#
# «Params»
#
# Параметры типа доставки
#
# Object
#
# Object Payments коллекция объектов следующей структуры:
#
# «PaymentType»:1
#
# Код типа оплаты
#
# Short
#
# «Name»:«Наличная»
#
# Имя типа оплаты
#
# String
#
# Object Params
#
# «HasAnotherShippingCompany»: False
#
# Признак сторонней компании доставки
#
# Bool
#
# «HasDeliveryPoint»:True
#
# Признак точки выдачи
#
# Bool
#
# «Points»
#
# Точки выдачи
#
# Object
#
# «Addresses»
#
# Адреса доставки
#
# Object
#
# Object Points коллекция объектов следующей структуры:
#
# «Description»:«Самовывоз»
#
# Описание типа доставки
#
# String
#
# «Id»:23
#
# Уникальный код адреса доставки
#
# Int
#
# «Name»:«Самовывоз»
#
# Имя типа доставки
#
# String
#
# Object Addresses коллекция объектов следующей структуры:
#
# «Address»:«Адыгея, 17 лет Октября, хутор (Майкопский Район),12»
#
# Адрес доставки
#
# String
#
# «Id»:2854
#
# Уникальный код адреса доставки
#
# Int
#
# «IsDefault»:True
#
# Признак точки выдачи по умолчанию
#
# Bool
#
# «Type»:«Домашний»
#
# Тип адреса доставки
#
# String
#
#
#
# Оформление корзины
#
# HTTP метод
#
# POST
#
# URL запроса
#
# /SearchService/CheckoutBasket?positionIds={positionIds}&deliveryTypeId={deliveryTypeId}&paymentTypeId={paymentTypeId}&addressId={addressId}&deliveryPointId={deliveryPointId}&comment={comment}
#
# Заголовки запроса
#
# Authorization: Basic {credentials}
# Accept: application/json
# Content-type: application/json
#
# Параметры запроса
#
# positionIds – список id позиций из корзины для заказа (Int)
# deliveryTypeId –код типа доставки (или самовывоза) (Short)
# paymentTypeId – код типа оплаты (Short)
# addressId – код адреса доставки (Int)
# deliveryPointId – код точки выдачи (Int)
# comment – комментарий к заказу (String)
#
# Ответ
#
# JSON, коллекция объектов следующей структуры:
#
# "AddToOrderResult": true
#
# Признак создания заказа
#
# Bool
#
# "AddToOrderStatus": "Ожидает обработки"
#
# Текущий статус позиции в заказе
#
# String
#
# "OrderID": " 1234
#
# Номер заказа данной позиции
#
# String
#
# "PositionId": 12345
#
# Идентификатор позиции в корзине
#
# int
#
#
#
# ОБЩИЕ ПРИМЕЧАНИЯ
#
# Запросы осуществляются с помощью HTTP-методов GET
#
# Для запросов требуется преобразовать ваш логин и пароль вида «Login:Password» в стандарт Base64 и подставить в {credentials}
#
# В итоге, строка авторизации должна иметь вид как представлено ниже.
# Пример кода на C#:
#
# return "Basic " + Convert.ToBase64String(Encoding.UTF8.GetBytes(Login + ":" +Password));
# Для параметра withoutTransit допустимы только значения true/false. 0 и 1 не являются допустимыми с точки зрения c# для типа bool (System.Boolean).
#
# Важно! Домен сайта https://api.автосоюз.рф должен быть написан в punycode: https://api.xn--80aep1aarf3h.xn--p1ai
# Также обратите внимание, что артикулы, бренды и прочие параметры URL-адреса нужно кодировать, чтобы передавались они верно. В нашем примере используется
#
# HttpUtility.UrlEncode
# Пример кода для автоматического оформления заказа:
#
# HttpClient client = new HttpClient();
# string lp = Convert.ToBase64String(Encoding.UTF8.GetBytes(login + ":" + password)).ToString();
# Uri url = new Uri("https://api.xn--80aep1aarf3h.xn--p1ai/SearchService/AddOrder?items=" + HttpUtility.UrlEncode(items));
# client.BaseAddress = url;
# client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue("Basic", lp);
# var response = client.GetAsync(url).Result;
# Возможные ошибки
#
# Неверные логин и/или пароль, указанные в обращении к Сервису. Они должны совпадать с логином/паролем для доступа на наш сайт.
# Убедитесь, что ваши запросы идут с IP адреса, который вы указывали при запросе доступа к Сервису
# Нет транзитных поставщиков в результате – дневной лимит на поиск по транзитным поставщикам исчерпан, обратитесь к менеджеру
# Доступ запрещён по другим причинам
class AutoSous:
    async def get_json(self, endpoint, **filters):
        url = f'https://api.автосоюз.рф/SearchService/{endpoint}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=filters) as response:
                response_text = await response.text()
        return json.loads(response_text)


    async def get_pd(self, endpoint, **kwargs):
        return dict_to_df(await self.get_json(endpoint, **kwargs))


# https://portal.moskvorechie.ru/index.lmz#g7&id=120
# Запросы в формате JSON
# Данные в формате JSON передаются методом HTTP POST или HTTP GET. Запросы отправляют на адрес API Портала:
# http://portal.moskvorechie.ru/portal.api
# Для доступа к API через криптографический протокол SSL, который защищает данные от несанкционированного доступа при передаче по открытым каналам связи, запросы надо отправлять на адрес:
# https://portal.moskvorechie.ru/portal.api
#
# API доступен только авторизованным пользователям Портала. Пользователи идентифицируют себя следующим способом:
# Передаваемый запрос на сервер всегда должен сожержать ключ "l" со значением логина, для доступа на портал. А также должен содержать ключ "p" с наборм 64 символов, которые отображаются у Вас в настройках при включении доступа к API портала. На каждый договор создается в настройках Портала свой собственный ключ доступа, он определяет условия договора под которыми отображаются цена и под данным договором будет размещается заказ.
#
# API Портала поддерживает несколько различных режимов кодировки. По умолчанию наш портал работает с кодировкой CP-1251, но также может получать/выдавать результаты в кодировках: UTF-8 и KOI8-R. Для того, чтобы на портале использовать кодировку отличную от CP-1251, необходимо указать дополнительный входной параметр "cs=utf8" для использования кодировки UTF-8 или же "cs=koi8r" для работы с кодировкой KOI8-R.
# Также передаваемый массив при запросе всегда включает ключ act с именем вызываемого метода, доступные методы перечислены ниже.
#
# Например при использовании метода HTTP SSL GET, запрос будет выглядеть следующим образом:
# GET https://portal.moskvorechie.ru/portal.api?l=username&p=keyphrase&act=brand_by_nr&nr=kl2&alt\n
# Или запрос методом HTTP POST:
# POST http://portal.moskvorechie.ru/portal.api HTTP/1.0\n
# Host: portal.moskvorechie.ru\n
# Content-Type: application/x-www-form-urlencoded\n
# Content-Length: 52\n
# \n
# l=username&p=keyphrase&act=brand_by_nr&nr=kl2&alt&oe

# Получение списка производителей по номеру производителя.
# "act=brand_by_nr"
# Функция возвращает список названия брендов производителей, а также названия автозапчастей при запросе по номеру запчасти. Поддерживается возможность задавать как сам номер производителя, так и оригинальные номера, а также кроссовые(альтернативные) номера.
# Для обращения к данной функции необходимо передать следующие значения:
# "l=username" - Имя пользователя, логин
# "p=keyphrase" - Ключ доступа (64 символа)
# "act=brand_by_nr" - Название функции
# "nr=search number" - Номер производителя
# А также дополнительные параметры:
# "name" - Добавляет к результатам запроса дополнительное поле "name" в котором содержится название автозапчастей для каждого названия производителя.
# "oe" - По умолчанию поиск производителей производится только по номеру самого производителя, но если добавить данный параметр, тогда можно также передавать оригинальные номера, и позиции будут искаться через кросс таблицы на оригинальные номера.
# "alt" - При использовании данного параметра, в результатах данной процедуру будут также выводиться бренды на которые есть аналоги на нашем складе.
#
# Функция возвращает следующие значения:
# "nr" - Номер производителя
# "brand" - Название производителя
# "name" - Название товара, выводится при использовани при запросе параметра "name"
# Пример использования:
# Запрос методом GET
# http://portal.moskvorechie.ru/portal.api?l=username&p=keyphrase&act=brand_by_nr&nr=32-D88-F&alt&name
# Данный запрос получает список названий производителей, названий автозапчастей и их номеров, у которых в кажетве номера производителя или в качестве кросс-номеров (аналогов) указан номер "32-D88-F"
# Результатом данного запроса будет:
#    {"result": [
#        {"nr":"A-3045GR","brand":"Optimal","name":"Амортизатор BMW E46 -04/01 пер.прав.газ.SPORT"},
#        {"nr":"32-D88-F","brand":"Boge","name":"Амортизатор BMW E46 -04/01 пер.прав.газ.SPORT"},
#        {"nr":"A-3105GR","brand":"Optimal","name":"Амортизатор BMW E46 -04/01 пер.прав.газ.SPORT"}
#    ]}

# Получение списка автозапчастей по номеру и названию производителя.
# "act=price_by_nr_firm"
# Для обращения к данной функции необходимо передать следующие значения:
# "l=username" - Имя пользователя, логин
# "p=keyphrase" - Ключ доступа (64 символа)
# "act=price_by_nr_firm" - Название функции
# "nr=search number" - Номер производителя
# "v=1" - Версия функции
#
# А также дополнительные параметры:
# "f=brand name" - Название производителя, при необходимости мы сможете отфильтровать по определенному производителю.
# "oe" - По умолчанию поиск производителей производится только по номеру самого производителя, но если добавить данный параметр, тогда можно также передавать оригинальные номера, и позиции будут искаться через кросс таблицы на оригинальные номера.
# "alt" - При использовании данного параметра, в результатах данной процедуру будут также выводиться бренды на которые есть аналоги на нашем складе.
# "avail" - Отображать только позиции, которые есть в наличии на складе. (В т.ч. позиции под заказ)
# "extstor" - При использовании данного параметра, из результатов скрываются все предложения со сторонних складов (позиции под заказ). Будет отображаться только наличие с локальных складов.
#
# Функция возвращает следующие значения:
# "nr" - Номер производителя
# "brand" - Название производителя
# "name" - Название автозапчасти
# "stock" - Кол-во позиций на складе, ("0" - нет наличии, "+" - есть в наличии, но кол-во не указано)
# "ddays" - Средний срок поставки в днях
# "minq" - Минимальное кол-во для заказа
# "upd" - Дата, время на которое актуальны данные
# "price" - Цена для данного клиента
# "currency" - Валюта в которой представлена цена
# "gid" - ID товара в прайс-листе. Необходимо для выполнения операций с данной позицией, напр. "добавление в корзину".
# "sname" - Название склада, где находится данная деталь
# "sflag" - Поле с флагами, в зависимости от позиции символа определяет то или иное условие, символ может принимать или "0" - нет или "1" - да.
# 1 символ - Является ли данный склад локальным "1" или сторонним поставщиком "0"
# 2 символ - Указывается если запрещен возврат детали, если равен "1" значит данную деталь нельзя вернуть обратно
# Например "01" - стронний склад + запрещены возвраты
# Пример использования:
# Запрос методом GET
# http://portal.moskvorechie.ru/portal.api?l=username&p=keyphrase&act=price_by_nr_firm&v=1&nr=OC47&f=Knecht&cs=utf8
# Данный запрос получает список позиций, названий, их номеров, цен и т.д. у которых в качестве номера производителя или в качестве кросс-номеров (аналогов) указан номер "32-D88-F" и производитель "Boge"
# Результатом данного запроса будет:
#    {"result": [
#        {"nr":"OC47", "brand":"Knecht", "name":"Фильтр масляный", "stock":"150", "ddays":"7", "minq":"1", "upd":"01.02.20 02:27", "price":"546.65", "currency":"руб.", "gid":"103423892", "sname":"Стор 34", "sflag":"00"},
#        {"nr":"OC47", "brand":"Knecht", "name":"Фильтр масляный AUDI/VW", "stock":"0", "ddays":"0", "minq":"1", "upd":"02.02.20 11:05", "price":"398.13", "currency":"руб.", "gid":"1001135363", "sname":"Центр.", "sflag":"10"}
#    ]}

# Добавление позиции из прайс-листа в корзину пользователя.
# "act=to_basket"
# Функция позволяет добавить позиции(автозапчасти) из прайс-листа в корзину пользователя Портала. Для добавления в корзину товара необходимо передать функции внутренний ID позиции, который можно получить из других функций применяя доп. входной параметр "gid".
# Для обращения к данной функции необходимо передать следующие значения:
# "l=username" - Имя пользователя, логин
# "p=keyphrase" - Ключ доступа (64 символа)
# "act=to_basket" - Название функции
# "gid=ID" - ID позиции в прайс-листе.
#
# А также дополнительные параметры:
# "q=integer" - Количество добавляемое в корзину.
# "c=comment" - Комментарий к позиции.
# "bid" - При наличии флага bid, функция вернет ID товара в корзине для последующего попозиционного размещения заказа.
#
#
# Функция возвращает следующие значения:
# "status" - Статус добавления товара в корзину, 0 - товар успешно добавлен, 1 - произвошла ошибка (см поле "msg").
# "msg" - Если произошла ошибка при добавлении товара в корзину, в данном поле будет указано, почему позиция не была добавлена в корзину.
# "id" - ID товара в корзине, если указан флаг "bid".
# Пример использования:
# Запрос методом GET
# http://portal.moskvorechie.ru/portal.api?l=username&p=keyphrase&act=to_basket&gid=100185696&q=3
# Данный запрос добавляет позицию с ID 100185696 в корзину пользователя username в количестве 3-х штук.
# Результатом данного запроса будет:
#    {"result": {
#        "status":"0",
#        "msg":""
#    }}

# Получение списка автозапчастей из корзины портала.
# "act=my_basket"
# Для обращения к данной функции необходимо передать следующие значения:
# "l=username" - Имя пользователя, логин
# "p=keyphrase" - Ключ доступа (64 символа)
# "act=my_basket" - Название функции
# А также дополнительные параметры:
# "id" - Выводить дополнительное поле, идентифицирующее позицию в корзине.
# "gid" - Отображать уникальный ID товара в системе.
# "store" - Показывать доп. информацию по складу.
#
# Функция возвращает следующие значения:
# "nr" - Номер производителя
# "brand" - Название производителя
# "name" - Название автозапчасти
# "stock" - Кол-во позиций на складе
# "delivery" - Средний срок поставки
# "quantity" - Кол-во добавленных в корзину позиций
# "ref" - Комментарий к добавленной позиции
# "minq" - Минимальное кол-во для заказа
# "upd" - Дата, время на которое актуальны данные
# "price" - Цена для данного клиента
# "currency" - Валюта в которой представлена цена
# "id" - ID строки в корзине, конкретная строка в корзине (если указан параметр "id").
# "gid" - Уникальный ID товара в системе (если указан параметр "gid").
# "sname" - Название склада, где находится данная деталь (если указан параметр "store")
# "sflag" - Поле с флагами (если указан параметр "store"), в зависимости от позиции символа определяет то или иное условие, символ может принимать или "0" - нет или "1" - да.
# 1 символ - Является ли данный склад локальным "1" или сторонним поставщиком "0"
# 2 символ - Указывается если запрещен возврат детали, если равен "1" значит данную деталь нельзя вернуть обратно
# Например "01" - стронний склад + запрещены возвраты
# Пример использования:
# Запрос методом GET
# http://portal.moskvorechie.ru/portal.api?l=username&p=keyphrase&act=my_basket
# Данный запрос возвращает содержимое корзины на портале, список позиций, названий, их номеров, цен и т.д.
# В случае если корзина пуста, поступит следующий ответ:
# {"result":{"status":"0","msg":"Корзина пуста"}}
# В обратном случае результатом данного запроса будет:
#    {"result": [
#        {"nr":"32-D88-F", "brand":"Boge", "name":"Амортизатор пер прав BMW E46 SPORT", "stock":"2", "delivery":"10 дней", "quantity":"10", "ref":"в головной офис", "minq":"1", "upd":"11.03.12 02:30", "price":"3629.50", "currency":"руб."},
#        {"nr":"A-3105GR", "brand":"Optimal", "name":"Амортизатор газ. F. R BMW 3 E46 98-01 (32-D88-F)", "stock":"1", "delivery":"10 дней", "quantity":"8", "ref":"", "minq":"1", "upd":"11.03.12 02:45", "price":"2039.09", "currency":"руб."}
#    ]}

# Оформление заказа в учетной системе на Портале из корзины пользователя.
# "act=make_order_v2"
# Функция позволяет оформить заказ непосредственно в учетной системе из позиций ранее добавленных в корзину пользователя Портала.
# Размещение заказов происходит в режиме очереди, поэтому для контроля за ходом размещения заказа существует 2 последовательных действия.
#
# Этап 1. Размещение заказа из корзины
# Этап 2. Проверка состояния оформления заказа (необязательно)
# Если в корзине содержатся позиции с разных складов, заказ будет разбит на составные заказы по каждому складу, им будет присвоен свой ID, и за состоянием каждого Вы сможете следить отдельно.
#
# Заказ будет размещен на ближайшую дату доставки/самовывоза. Если указана доставка, то она будет произведена по адресу соответствующему договору под которым размещается заказ.
#
# Этап 1. Добавление в очередь на размещение заказа из корзины.
# Для обращения к данной функции необходимо передать следующие параметры:
# "l=username" - Имя пользователя, логин
# "p=keyphrase" - Ключ доступа (64 символа), на каждый договор создается в настройках Портала свой собственный. Определяет условия договора под которыми размещается заказ.
# "act=make_order_v2" - Название функции
# А также дополнительные параметры:
# "gids=41856825;41856826;41856822;" - Если указан данный параметр, заказ оформляется только на перечисленные в данном параметре позиции из корзины. Внимание! ID позиций для данного параметра получаются из функции "act=my_basket" с использованием доп. параметра при вызове "id" или при использовании функции "act=to_basket" с флагом "bid". В результатах этих функций ID позиции указано в поле "id". Несколько значений указываются через ";". Данные ID это именно строки из корзины, каждый раз будут отличаться.
# "pos_list=1001304205:3:;1001304206:1:reference 1;1001386004:7:reference 2" - Также можно разместить заказ предварительно не добавляя товар в корзину. Если указан данный параметр, позиции из корзины (включая параметр gids) не будут использоваться, только перечисленные в "pos_list". Массив позиций в "pos_list" разделен символом ";". Каждый элемент позиции состоит из 3-х составляющих: GID позиции в прайс-листе ("act=price_by_nr_firm" с использованием параметра "gid"), кол-во позиций для заказа, комментарий к позиции (макс 100 символов). Все эти составляющие разделены символом ":".
# "on=name" - Название заказа.
# "dl=1" - Тип доставки, "1" - требуется доставка, "0" - самовывоз, "2" - только зарезервировать.
# Функция возвращает следующие значения: (Если заказ разбился на подзаказы возвращается массив значений "id" и "name")
# "id" - ID заказа на портале, потребуется для последующих этапов.
# "name" - Название заказа.
# Существует минимальный интервал между размещениями заказов от одного пользователя, на текущий момент он составляет 60 сек. Если заказ будет размещен, пока интервал не пройдет с момента последнего размещения заказа, сервис отобразит ошибку.
# Этап 2. Проверка состояния оформления заказа (данный этап не обязателен).
# Данная функция не будет отображать дальнейшее движение товара и изменение заказа, только первоначальный этап размещения заказа в учетной системе. Для дальнейшего отслежения состояния заказов используйте функции получения данных из учетной системы.
# Обращение к данной функции чаще чем 1 раз в 0.5 секунды, может привезти к автоматической временной блокировке.
# Для обращения к данной функции необходимо передать следующие параметры:
# "l=username" - Имя пользователя, логин
# "p=keyphrase" - Ключ доступа (64 символа), на каждый договор создается в настройках Портала свой собственный. Определяет условия договора под которыми размещается заказ.
# "act=make_order_v2" - Название функции
# "oids=16707178;16707179;16707180" - Список ID заказов Портала, полученный на Этапе №1.
# Функция возвращает следующие значения: (По каждому заказу указанному в параметре "oids")
# "id" - ID заказа на портале.
# "status_id" - ID статуса.
# -1 Производится подключение к учетной системе
# -2 Создание заказа в учетной системе
# -3 Производится резервирование заказанного Вами товара
# -4 Создается расходная накладная для Вашего заказа
# -9 Ваш заказ отправляется менеджрам в ТЗ
#  0 Заказ не найден
#  1 Заказ размещен в учетной системе
#  2 Создана РН
#  3 Создана заявка
#  9 заказ отправлен на ручную обработку менеджерам компании и будет обработан в рабочее время.
# "status_txt" - Статус текстом.
# "doc_id" - ID документа в учетной системе. ID документа потребуется для последующего получения информации по данному документу непосредственно из учетной системы.
# "pos_list" - список позиций по данному заказу. Содержит массив. Выводится только если заказ уже размещен (status_id > 0).
# "firm" - Производитель.
# "nr" - Номер производителя.
# "cnt" - Заказанное количество.
# "cnt_chk" - Количество подтвержденное учетной системой.
# "price" - Цена при оформлении заказа.
# "price_chk" - Цена подтвержденная учетной системой.
# "ref" - Комментарий к позиции, указанный при добавлении позиции в корзину
# Пример использования:
# Запрос методом GET
# http://portal.moskvorechie.ru/portal.api?l=username&p=keyphrase&act=make_order_v2&on=ref35744&dl=1&gids=41856825;41856826;41856822
# Данный запрос оформляет заказ из корзины на позиции ID: 41856825,41856826,41856822. С использованием договора опреденного ключом "p=keyphrase", с ближайшей доставкой.
# Результатом данного запроса будет:
#    {"result": [{
#        "id":"1648864",
#        "name":"ref35744"
#    }]}

# Получение данных по автозапчасти по уникальному ключу.
# "act=g_info"
# Для обращения к данной функции необходимо передать следующие значения:
# "l=username" - Имя пользователя, логин
# "p=keyphrase" - Ключ доступа (64 символа)
# "act=g_info" - Название функции
# "key=unique key" - Уникальный ID товара, выводится в функциях API под именем "gid"
#
# А также дополнительные параметры:
# "type" - Использовать в качестве уникального ID товара инвентарный номер компании (выгружается в прайс-листе).
# "store" - Показывать доп. информацию по складу.
#
# Функция возвращает следующие значения:
# "nr" - Номер производителя
# "brand" - Название производителя
# "name" - Название автозапчасти
# "stock" - Кол-во позиций на складе, ("0" - нет наличии, "+" - есть в наличии, но кол-во не указано)
# "delivery" - Средний срок поставки
# "minq" - Минимальное кол-во для заказа
# "upd" - Дата, время на которое актуальны данные
# "price" - Цена для данного клиента
# "currency" - Валюта в которой представлена цена
# "gid" - Уникальный ID товара в системе.
# "sname" - Название склада, где находится данная деталь (если указан параметр "store")
# "sflag" - Поле с флагами (если указан параметр "store"), в зависимости от позиции символа определяет то или иное условие, символ может принимать или "0" - нет или "1" - да.
# 1 символ - Является ли данный склад локальным "1" или сторонним поставщиком "0"
# 2 символ - Указывается если запрещен возврат детали, если равен "1" значит данную деталь нельзя вернуть обратно
# Например "01" - стронний склад + запрещены возвраты
# Пример использования:
# Запрос методом GET
# http://portal.moskvorechie.ru/portal.api?l=username&p=keyphrase&act=g_info&key=1001184
# Данный запрос получает описание позиции, название, цену и т.д. у которой в качестве уникального номера в системе указано "1001184".
# Результатом данного запроса будет:
#    {"result": [
#        {"nr":"209312","brand":"NK","name":"Диск тормозной CHRISLER VOYAGER/DODGE CARAVAN 00- передний D=302мм.","stock":"2","delivery":"на складе","minq":"2","upd":"09.03.13 03:06","price":"1005.77","currency":"руб.","gid":"1001184"}
#    ]}

# Получение актуальных остатков по складу в виде файла.
# "act=pricelist"
# Данный метод позволяет получать актуальные остатки по доступным Вам складам. Предполагается, что используя механизм рассылки прайс-листа на Портале, утром, Вы получаете всю доступную номенклатуру с Вашими ценами. Далее в течении дня, т.к. цены могут изменится только в исключительной ситуации, Вы сможете используя данный сервис, поддерживать остатки по нужному складу в актуальном состоянии. Выдаваемые сервисом имена файлов являются временными, доступны в течении нескольких часов и содержат в себе информацию актуальную на момент создания данных файлов. Для получения новых имен файлов со свежими остатками, необходимо вновь вызвать данную функцию и получить актуальные имена файлов. Файлы генерируются, если произошли изменения и не чаще, чем раз в 15 минут, поэтому вызывать данный сервис чаще, не является целесообразным и может привести к блокировке Вашего аккаунта.
# Для обращения к данной функции необходимо передать следующие значения:
# "l=username" - Имя пользователя, логин
# "p=keyphrase" - Ключ доступа (64 символа)
# "act=pricelist" - Название функции
#
# Функция возвращает массив со следующими значениями:
# "id" - ID склада
# "name" - Название склада
# "time" - Время на которое актуальны остатки
# "file" - Имя файла с остатками
#
# Данная функция вернет список доступных Вам складов с указанием имени временного файла с остатками. После получения ответа с названием файла, необходимо для нужного склада скачать файл с остатками используя протоколы http или https, расположенного по адресу http(s)://portal.moskvorechie.ru/, например http://portal.moskvorechie.ru/price_api/2_Q3....7caI.txt
# Файл с остатками имеет текстовый формат с разделителем - табуляция (\t), со следующими колонками:
# ID товара в прайс-листе. Необходимо для сопоставления с полным прайс-листом с ценами или для выполнения операций через API с данной позицией, напр. "добавление в корзину".
# Название производителя.
# Номер производителя.
# Кол-во позиций на складе.
#
# Пример использования:
# Запрос методом GET
# http://portal.moskvorechie.ru/portal.api?l=username&p=keyphrase&act=pricelist&cs=utf8
# Результатом данного запроса будет:
#    {"result":[
#        {"id":"2","name":"Запад","time":"21.01.20 22:51","file":"/price_api/2_Q3cEtQUfql7EVBmq5XOl9DswyZUEIsSXK2EE7hCJmW0rdVNbCahCTtPAPp3z7caI.txt"},
#        {"id":"4","name":"Центр","time":"21.01.20 22:04","file":"/price_api/4_kUpptbuSsjgeOO4wHLB3gPw9OIZcyasuBnQ6h5wf5ucg00XXubT6VNGkFDtJGh20.txt"}
#    ]}

class Moskvorechie:
    username = 'zakupkaavtosnab2'
    password = 'UGoMvk9oFfigXsoXhIYznR2gVRTYpKWqvDgmzwjdJz5Ww9OsKNLB4LH5m1I1ZlL7'
    async def get_json(self, endpoint, **filters):
        url = f'https://portal.moskvorechie.ru/portal.api?{endpoint}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=filters) as response:
                response_text = await response.text()
        return json.loads(response_text)


    async def get_pd(self, endpoint, **kwargs):
        filters = {'l': self.username, 'p': self.password, 'act': endpoint} | kwargs
        return dict_to_df(await self.get_json(endpoint, **filters))



async def main():
    # objects = await Pr_Lg().get_list('warehouses')
    # print(objects)

    # client = RosskoAPIClient()
    # result = client.search('333114', '000000002', '112233')
    # print(result)

    # rossko_api = RosskoAPI('GetCheckout')
    # delivery_id = '000000002'
    # address_id = '112233'
    # payment_id = '1'
    # requisite_id = '112233'
    # name = 'Your name'
    # phone = 'Your phone'
    # comment = 'My first test order'
    # parts = [
    #     {
    #         'partnumber': 'BPR6E',
    #         'brand': 'NGK',
    #         'stock': 'HST375',
    #         'count': '1',
    #         'comment': 'Item comment'
    #     },
    #     {
    #         'partnumber': '333114',
    #         'brand': 'KYB',
    #         'stock': 'HST125',
    #         'count': '2',
    #         'comment': 'Item comment'
    #     }
    # ]
    #
    # result = rossko_api.get_checkout(delivery_id, address_id, payment_id, requisite_id, name, phone, comment, parts)
    # print(result)

    # api = RosskoAPI('GetCheckoutDetails')
    # response = api.get_checkout_details()
    # print(response)
    return

if __name__ == '__main__':
    asyncio.run(main())