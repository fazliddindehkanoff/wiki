from random import randint

from django.shortcuts import render, redirect
from markdown2 import markdown

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title.strip())
    if content is None:
        content = "##Page couldn't found"
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {'content': content, 'title': title})

def edit(request, title):
    content = util.get_entry(title.strip())
    if content is None:
        return render(request, "encyclopedia/edit.html", {'error': "404 Not Found"})

    if request.method == "POST":
        content = request.POST.get("content").strip()
        if content == "":
            return render(request, "encyclopedia/edit.html", {"message": "You're unable to save with empty field.", "title": title, "content": content})
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {'content': content, 'title': title})

def create(request):
    if request.method == "POST":
        title = request.POST.get('title').strip()
        content = request.POST.get('content').strip()
        
        if title == "":
            return render(request, "encyclopedia/add.html", {"message": "Can't save with empty title."})

        elif content == "":
            return render(request, "encyclopedia/add.html", {"message": "Can't save with empty content."})

        elif title in util.list_entries():
            return render(request, "encyclopedia/add.html", {"message": "This title is already exist.", "title": title,})

        util.save_entry(title, content)
        return redirect('entry', title=title)
    return render(request, "encyclopedia/add.html")

def random_page(request):
    entries = util.list_entries()
    random_title = entries[randint(0, len(entries)-1)]
    return redirect("entry", title=random_title)


def search(request):
    q = request.GET.get('q').strip()
    if q in util.list_entries():
        return redirect("entry", title=q)
    return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})