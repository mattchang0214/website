from books.forms import BookForm
from books.models import Book
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def home(request):
    template_name = 'books/home.html'

    return render(request, template_name)

def index(request):
    template_name = 'books/all_books.html'
    object_name = {'book_list': Book.objects.all().order_by('-updated')}

    return render(request, template_name, object_name)

def my_books(request):
    template_name = 'books/my_books.html'
    reorderBook = Book.objects.all().order_by('-updated')
    object_name = {'book_list': reorderBook.filter(seller=request.user)}

    return render(request, template_name, object_name)

def create_book(request):
    form = BookForm()
    object_name = {'form': form}
    template_name = 'books/book_form.html'

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            # for book in Book.objects.all():
            #     if .name == form.cleaned_data['name']:
            #         object_name = {
            #             'form': form,
            #             'error_message': 'Artist already exists!'
            #         }
            #         return render(request, template_name, object_name)
            book = form.save(commit=False)
            book.seller = request.user
            book.save()
            return redirect('books:mine')
        object_name = {'form': form}

    return render(request, template_name, object_name)

def update_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    form = BookForm(instance=book)
    object_name = {'form': form}
    template_name = 'books/edit_book.html'

    if book.seller != request.user:
        return render(request, 'books/forbidden.html')

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book.save()
            return redirect('books:mine')
        object_name = {'form': form}

    return render(request, template_name, object_name)

def delete_book(request, book_id):
    book = Book.objects.get(pk=book_id)

    if book.seller != request.user:
        return render(request, 'books/forbidden.html')

    book.delete()
    return redirect('books:mine')

# Source: https://stackoverflow.com/questions/19402172/how-to-write-a-search-function-in-django
def search(request):
    template_name = 'books/result.html'
    query = request.GET.get('q')
    results = Book.objects.all()
    object_name = {'results': results}

    if query:
        results = Book.objects.filter(Q(title__icontains=query))
        object_name = {'results': results, 'query': query}

    return render(request, template_name, object_name)

# Source: https://stackoverflow.com/questions/3005080/how-to-send-html-email-with-django-with-dynamic-content-in-it
def sold(request, book_id):
    if not request.user.is_superuser:
        return render(request, 'books/forbidden.html')

    book = Book.objects.get(pk=book_id)
    book.seller.userprofile.total += book.price

    subject, to = 'Subject', book.seller.email
    object_name = {'book': book, 'userprofile': book.seller.userprofile}

    # render with dynamic value
    html_content = render_to_string('books/mail_template.html', object_name)
    # Strip the html tag. So people can see the pure text at least.
    text_content = strip_tags(html_content)

    # create the email, and attach the HTML version as well.
    msg = EmailMultiAlternatives(subject, text_content, to=[to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    book.delete()

    return render(request, 'books/search_form.html')