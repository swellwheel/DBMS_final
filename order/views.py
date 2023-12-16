from django.shortcuts import render,redirect
import requests
from main_p.models import SaleOrder
from main_p.models import WantOrder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class FakeUser:
        def __init__(self, user_id, user_name, role='user',email="p@gmail.com"):
            self.user_id = user_id
            self.user_name = user_name
            self.role = role
            self.email = email
class FakeBook:
        def __init__(self, isbn, price, description, receiver, status):
            self.isbn = isbn
            self.price = price
            self.description = description
            self.status = status
            self.receiver = receiver
            self.title = '假書名'
            self.author = '假作者'
class FakeOrder:
        def __init__(self, order_id, user_id, books):
            self.order_id = order_id
            self.user_id = user_id
            self.books = books
class FakeBook_detail:
        def __init__(self, isbn, price, description, poster, status):
            self.isbn = isbn
            self.price = price
            self.description = description
            self.poster = poster
            self.status = status
            self.title = '假書名'
            self.author = '假作者'
            self.category = ['理學院', "文學院"]
            self.courseID = '123456'
            self.academic_year = '112-1'
            self.courseName = '資料庫'
            self.teacherName = '孔子'





def index(request):
    return render(request, 'order/index.html')

def want_order(request, user_id):
    user1 = FakeUser(3, 'Jerry3')
    books1 = [FakeBook("ISBN1", None, "Description 1",user1,'posting'), FakeBook("ISBN2", None, "Description 2",user1,'posting')]
    books2 = [FakeBook("ISBN3", None, "Description 3",user1,'posting')]
    books3 = [FakeBook("ISBN4", None, "Description 1",user1,'posting'), FakeBook("ISBN2", None, "Description 2",user1,'posting')]
    books4 = [FakeBook("ISBN5", None, "Description 3",user1,'posting')]
    # 創建假訂單數據
    orders = [
        FakeOrder(1, user_id, books1),
        FakeOrder(2, user_id, books2),
        FakeOrder(3, user_id, books3),
        FakeOrder(4, user_id, books4),
    ]

    api_url = f'http://localhost:8000/order/api/want_order/{user_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    orders = api_response.get('orders')
    
    # 分頁
    items_per_page = 20
    paginator = Paginator(orders, items_per_page)
    page = request.GET.get('page')

    try:
        orders_page = paginator.page(page)
    except PageNotAnInteger:
        orders_page = paginator.page(1)
    except EmptyPage:
        orders_page = paginator.page(paginator.num_pages)

    return render(request, 'order/want_order.html', {'orders':orders_page,'user_id': user_id})

def sale_order(request, user_id):
    user1 = FakeUser(3, 'Jerry3')
    books1 = [FakeBook("ISBN1", '100', "Description 1",user1,'posting'), FakeBook("ISBN2", '100', "Description 2",user1,'posting')]
    books2 = [FakeBook("ISBN3", '100', "Description 3",user1,'posting')]
    books3 = [FakeBook("ISBN4", '100', "Description 1",user1,'posting'), FakeBook("ISBN2", '100', "Description 2",user1,'posting')]
    books4 = [FakeBook("ISBN5", '100', "Description 3",user1,'posting')]
    # 創建假訂單數據
    orders = [
        FakeOrder(1, user_id, books1),
        FakeOrder(2, user_id, books2),
        FakeOrder(3, user_id, books3),
        FakeOrder(4, user_id, books4),
    ]
    api_url = f'http://localhost:8000/order/api/sale_order/{user_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    orders = api_response.get('orders')
    
    # 分頁
    items_per_page = 20
    paginator = Paginator(orders, items_per_page)
    page = request.GET.get('page')

    try:
        orders_page = paginator.page(page)
    except PageNotAnInteger:
        orders_page = paginator.page(1)
    except EmptyPage:
        orders_page = paginator.page(paginator.num_pages)
    

    return render(request, 'order/sale_order.html', {'orders':orders_page,'user_id': user_id})

def want_order_detail(request, user_id, order_id):
    user1 = FakeUser(3, 'Jerry3')
    books1 = [FakeBook_detail("ISBN1", "100", "Description 1",poster=user1,status='finished'), FakeBook_detail("ISBN2", "150", "Description 2",poster=user1,status='posting')]
    poster_id = books1[0].poster.user_id
    api_url = f'http://localhost:8000/order/api/sale_order_detail/{user_id}/{order_id}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    books = api_response.get('books')
    poster_id = WantOrder.objects.get(orderid=order_id).userid
    
    if request.method == 'POST':
        for key, value in request.POST.items():
                if value == 'receive':
                    return redirect('order:receive', type='want_order', user_id=user_id,poster_id=poster_id, order_id=order_id)
    return render(request, 'order/detail/want_order_detail.html', {'books':books1,'user_id': user_id, 'order_id': order_id})

def sale_order_detail(request, user_id, order_id):
    user1 = FakeUser(3, 'Jerry3')
    books1 = [FakeBook_detail("ISBN1", "100", "Description 1",poster=user1,status='finished'), FakeBook_detail("ISBN2", "150", "Description 2",poster=user1,status='posting')]
    poster_id = books1[0].poster.user_id
    if request.method == 'POST':
        for key, value in request.POST.items():
                if value == 'receive':
                    return redirect('order:receive', type='sale_order', user_id=user_id , poster_id=poster_id, order_id=order_id)
    return render(request, 'order/detail/sale_order_detail.html', {'books':books1,'user_id': user_id, 'order_id': order_id})

def receive(request, user_id, poster_id, order_id, type):
    fake_poster = FakeUser(poster_id, 'Jerry3')
    return render(request, 'order/receive.html', {'type':type, 'user_id':user_id, 'poster': fake_poster, 'order_id': order_id})
    api_url = f'http://localhost:8000/order/api/receive/{user_id}/{poster_id}>/{order_id}/{type}'
    api_response = requests.get(api_url)
    api_response = api_response.json()
    poster = api_response.get('poster')
    return render(request, 'order/receive.html', {'type':type, 'user_id':user_id, 'poster': poster, 'order_id': order_id})
"""
def order_list(request):
    # 獲取所有訂單對象，你的邏輯可能會有所不同
    all_orders = Order.objects.all()

    # 定義每頁顯示的資料筆數
    items_per_page = 20

    # 將所有訂單對象分頁
    paginator = Paginator(all_orders, items_per_page)

    # 獲取當前頁碼
    page = request.GET.get('page')

    try:
        # 根據當前頁碼獲取對應頁的訂單對象
        orders = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整數，將第一頁返回
        orders = paginator.page(1)
    except EmptyPage:
        # 如果page超出範圍，返回最後一頁
        orders = paginator.page(paginator.num_pages)

    return render(request, 'your_template.html', {'orders': orders})
"""
