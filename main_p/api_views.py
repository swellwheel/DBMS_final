from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main_p.models import Users
from main_p.models import Book
from main_p.models import BookCategory
from main_p.models import UserRole
from .models import SaleOrder
from .models import WantOrder
from .models import Sell
from .models import LookFor
from django.utils import timezone
from self_info.models import Order
from self_info.api_views import OrderSerializer
from self_info.models import Book_object
from self_info.api_views import BookObjectSerializer
from self_info.api_views import UserSerializer
from self_info.models import User
from .models import ReceiveWant
from .models import ReceiveSale
from django.core.paginator import Paginator
from evaluate.api_views import UsersSerializer
from django.db.models import Q
from django.db import transaction


class MainPAPIView(APIView):
    def get(self, request, user_id, *args, **kwargs):
        user = Users.objects.get(userid=user_id)
        username = user.username
        serializer = UsersSerializer(user)

        return Response({'message': f'API for user {user_id}', 'username': username, 'user': serializer.data})


class PostAPIView(APIView):
    def post(self, request, user_id, *args, **kwargs):
        with transaction.atomic():
            user = Users.objects.get(userid=user_id)
            order_type = request.data.get('order_type')

            if order_type == 'sell':
                book_counter = 1
                order_id = SaleOrder.objects.count() + 1
                current_datetime = timezone.now()
                current_date = current_datetime.date()
                sale_order = SaleOrder.objects.create(orderid=order_id, userid=user, postdate=current_date)

                while True:
                    isbn_key = f'isbn_{book_counter}'
                    price_key = f'price_{book_counter}'
                    description_key = f'description_{book_counter}'

                    isbn = request.data.get(isbn_key)
                    price = request.data.get(price_key)
                    description = request.data.get(description_key)
                    status = 'Posting'

                    if isbn is None:
                        # No more books, break out of the loop
                        break


                    book = Book.objects.get(isbn=isbn)
                    Sell.objects.create(orderid=sale_order, isbn=book, price=price, status=status, description=description, finishdate=None)
                    book_counter += 1



            else:
                book_counter = 1
                order_id = WantOrder.objects.count() + 1
                current_datetime = timezone.now()
                current_date = current_datetime.date()
                want_order = WantOrder.objects.create(orderid=order_id, userid=user, postdate=current_date)

                while True:
                    isbn_key = f'isbn_{book_counter}'
                    description_key = f'description_{book_counter}'

                    isbn = request.data.get(isbn_key)
                    description = request.data.get(description_key)
                    status = 'Posting'

                    if isbn is None:
                        # No more books, break out of the loop
                        break

                    book = Book.objects.get(isbn=isbn)

                    LookFor.objects.create(orderid=want_order, isbn=book, status=status, description=description, finishdate=None)
                    book_counter += 1
            return Response({'user_id': user_id, 'order_id': order_id})



class SearchAPIView(APIView):
    def get_books_for_order(self, correspond_isbns, order_type):
        # Example: Modify your queryset to use select_related/prefetch_related
        if order_type == 'sell':
            sells = Sell.objects.filter(isbn__isbn__in=correspond_isbns).select_related(
                'orderid', 'orderid__userid', 'isbn'
            )
        else:
            sells = LookFor.objects.filter(isbn__isbn__in=correspond_isbns).select_related(
                'orderid', 'orderid__userid', 'isbn'
            )

        orders = []
        correspond_order_ids = []

        for sell in sells:
            order_id = sell.orderid.orderid
            if order_id != correspond_order_ids[-1] if correspond_order_ids else True:
                correspond_order_ids.append(order_id)

        for order_id in correspond_order_ids:
            sale_order = SaleOrder.objects.get(orderid=order_id)
            sells = Sell.objects.filter(orderid=order_id)
            posting_bool = False
            books = []

            for sell in sells:
                status = sell.status
                if status == 'Posting':
                    posting_bool = True
                    break

            if posting_bool:
                for sell in sells:
                    isbn = sell.isbn.isbn
                    price = sell.price if order_type == 'sell' else None
                    status = sell.status
                    description = sell.description

                    try:
                        receive_sale = ReceiveSale.objects.get(orderid=sale_order.orderid)
                        receiverid = receive_sale.userid.userid
                        receivername = Users.objects.get(userid=receiverid).username
                        receiver = User(receiverid, receivername)
                    except ReceiveSale.DoesNotExist:
                        receiver = None

                    book = Book.objects.get(isbn=isbn)
                    title = book.title
                    author = book.author
                    new_book = Book_object(isbn, price, description, receiver, status, title, author)
                    books.append(new_book)

                new_order = Order(sale_order.orderid, self.user_id, books)
                orders.append(new_order)

                if len(orders) > 100:
                    break

        return orders

    def post(self, request, user_id, *args, **kwargs):
        self.user_id = user_id
        orders = []

        order_type = request.data.get('order_type')
        category = request.data.get('category')
        key_word = request.data.get('keyword')

        if key_word == '':
            all_book_category = BookCategory.objects.filter(category=category)
            correspond_isbns = [book_category.isbn.isbn for book_category in all_book_category]
            orders = self.get_books_for_order(correspond_isbns, order_type)
        else:
            results = Book.objects.filter(
                Q(author__icontains=key_word) | Q(title__icontains=key_word)
            ).values_list('isbn', flat=True)

            # Convert the queryset to a list of ISBNs
            isbn_list = list(results)

            orders = self.get_books_for_order(isbn_list, order_type)
        orders_serializer = OrderSerializer(orders, many=True)
        return Response({'orders': orders_serializer.data, 'user_id': user_id})