from flask import Flask, render_template, request, redirect, url_for, session
import wikipedia

app = Flask(__name__)
# This Flask app sets app.secret_key, which is an encryption key used "to sign cookies and other things".
# Our app will work without it, but not completely. Without the secret key, we receive an error when searching:
# RuntimeError: The session is unavailable because no secret key was set.
# Storing secrets in plain code like this is not good practice. We know it.
# We don't want you to think we're endorsing this practice!
app.secret_key = 'IT@JCUA0Zr98j/3yXa R~XHH!jmN]LWX/,?RT'


@app.route('/')
def home():
    """Render the home page."""
    return render_template("home.html")


@app.route('/about')
def about():
    """Render the about page."""
    # The real content will live in templates/about.html
    # page_title is optional, but useful for your layout template.
    return render_template("about.html", page_title="About this app")


@app.route('/search', methods=['POST', 'GET'])
def search():
    """Render the search form page or handle a submitted search."""
    if request.method == 'POST':
        session['search_term'] = request.form['search']
        return redirect(url_for('results'))
    return render_template("search.html")


@app.route('/results')
def results():
    """Render the results page with Wikipedia search results."""
    search_term = session.get('search_term')

    # If someone goes straight to /results without searching first,
    # just send them back to the search page.
    if not search_term:
        return redirect(url_for('search'))

    page = get_page(search_term)
    # Pass page, page title, and the original search term to the template
    return render_template(
        "results.html",
        page=page,
        page_title=page.title,
        search_term=search_term
    )


def get_page(search_term):
    """Return a Wikipedia page object based on the search term."""
    # This function is not a route
    try:
        page = wikipedia.page(search_term)
    except wikipedia.exceptions.PageError:
        # No such page, so return a random one
        page = wikipedia.page(wikipedia.random())
    except wikipedia.exceptions.DisambiguationError:
        # This is a disambiguation page; get the first real page (close enough)
        page_titles = wikipedia.search(search_term)
        # Sometimes the next page has the same name (different caps), so don't try the same again
        if len(page_titles) > 2 and page_titles[1].lower() == page_titles[0].lower():
            title = page_titles[2]
        else:
            title = page_titles[1]
        page = get_page(title)
    return page


if __name__ == '__main__':
    app.run()
