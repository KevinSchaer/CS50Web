import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from markdown2 import Markdown


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def delete_entry(title):
    """
    delete an encyclopedia entry by a given title
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)


def search_matches(title):
    """
    search for similar entries based on the title
    """
    # get all available entries
    pages = list_entries()

    # track similar entries
    matches = []
    for page in pages:
        if title.lower() in page.lower():
            matches.append(page)

    return matches

def process_search_query(request, query):
    """
    run the search function of the wiki
    """
    entry = get_entry(query)

    # if entry exists
    if entry:
        return render(request, "encyclopedia/entry.html", {
        "entry": Markdown().convert(entry),
        "title": query
        })
        
    else:
        # search for similar entries
        matches = search_matches(query)

        # no matches found -> show error page
        if len(matches) == 0:
            return render(request, "encyclopedia/error.html", {
                "error": "403",
                "title": query
            })

        # if match was found
        else:
            return render(request, "encyclopedia/result.html", {
                "matches": matches,
                "title": query
            })
