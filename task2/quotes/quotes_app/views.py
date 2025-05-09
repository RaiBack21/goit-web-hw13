from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator

from .models import Quote, Tag, Author
from .forms import AuthorForm, QuoteForm
from utils import parsing


def main(request):
    quotes = Quote.objects.all()
    top_tags = Tag.objects.annotate(quotes_num=Count("quote")).order_by('-quotes_num')[:10]

    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request, "quotes_app/index.html", {"page_obj": page_obj, "top_tags": top_tags}
    )


def author_detail(request, author_name):
    author = Author.objects.get(fullname=author_name)
    return render(request, "quotes_app/author_detail.html", {"author": author})


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quotes_app:main")
        else:
            return render(request, "quotes_app/add_author.html", {"form": form})

    return render(request, "quotes_app/add_author.html", {"form": AuthorForm()})


@login_required
def add_quote(request):
    tags = Tag.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            return redirect(to="quotes_app:main")
        else:
            return render(
                request, "quotes_app/add_quote.html", {"form": form, "tags": tags}
            )

    return render(
        request, "quotes_app/add_quote.html", {"form": QuoteForm(), "tags": tags}
    )


def search_by_tag(request, tag_name):
    tag = Tag.objects.get(name=tag_name)
    quotes = Quote.objects.filter(tags=tag)

    paginator = Paginator(quotes, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "quotes_app/tag.html", {"page_obj": page_obj, "tag": tag})

def parse_data(request):
    parsing.parse_data()
    return redirect(to="quotes_app:main")
