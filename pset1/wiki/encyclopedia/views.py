from django.shortcuts import redirect, render
from django.urls import reverse
from markdown2 import Markdown
import random

from . import util

def index(request):
    # user searches for entry
    query = request.GET.get("q")
    if query:
        response = util.process_search_query(request, query)
        if response is not None:
            return response

    # show index page
    else:
        return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })

def entry(request, title):
    # if user uses search function while reading an entry in the wiki
    query = request.GET.get("q")
    if query:
        response = util.process_search_query(request, query)
        if response is not None:
            return response

    else:
        # show selected page
        entry = util.get_entry(title)
        # if entry does not exists
        if not entry:
            return render(request, "encyclopedia/error.html", {
                "error": "403",
                "title": title
            })
        else:
            return render(request, "encyclopedia/entry.html", {
                "entry": Markdown().convert(entry),
                "title": title
            })


def create(request):
    # if user uses search function while creating a new entry in the wiki
    query = request.GET.get("q")
    if query:
        response = util.process_search_query(request, query)
        if response is not None:
            return response

    else:
        # if user wants to create a new entry
        if request.method == "POST":
            title = request.POST["title"]
            content = request.POST["content"]
            # check if content or title is empty
            if not content or not title:
                return render(request, "encyclopedia/error.html", {
                        "error": "empty",
                        "title": title
                    })
            # check if title already exists
            elif util.get_entry(title):
                    return render(request, "encyclopedia/error.html", {
                        "error": "duplicate",
                        "title": title
                    })
            # check if title contains space -> leads to problems with the conversion to html
            elif " " in title:
                return render(request, "encyclopedia/error.html", {
                        "error": "space",
                        "title": title
                    })
            # if everything is fine, save entry and redirect
            else:
                util.save_entry(title, content)
                return redirect(reverse('entry', args=[title]))
        # show the user the create entry form
        else:
            return render(request, "encyclopedia/create.html", {})

def edit_page(request, title):
    # if user uses search function while editing an entry in the wiki
    query = request.GET.get("q")
    if query:
        response = util.process_search_query(request, query)
        if response is not None:
            return response

    else:
        # if user wants to edit an entry
        if request.method == "POST":
            title = request.POST["title"]
            content = request.POST["content"]
            util.save_entry(title, content)
            return redirect(reverse('entry', args=[title]))

        else:
            # shows the user the edit form 
            content = util.get_entry(title)
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "content": content
            })

def delete_page(request, title):
    # if user uses search function while editing an entry in the wiki
    query = request.GET.get("q")
    if query:
        response = util.process_search_query(request, query)
        if response is not None:
            return response

    # if user wants to delete the page
    else:    
        if request.method == "POST":
            # delete current page from entries
            util.delete_entry(title)
            return redirect(reverse('index'))
        else:
            # show delete page
            return render(request, "encyclopedia/delete.html", {
                "title": title
            })

def random_page(request):
    # if user uses search function while reading a random entry in the wiki
    query = request.GET.get("q")
    if query:
        response = util.process_search_query(request, query)
        if response is not None:
            return response

    # shows user a random page from the wiki
    else:
        pages = util.list_entries()
        random_title = random.choice(pages)
        entry = util.get_entry(random_title)
        return render(request, "encyclopedia/entry.html", {
            "entry": Markdown().convert(entry),
            "title": random_title
        })