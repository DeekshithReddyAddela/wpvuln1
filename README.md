## Project

### What does `site.py` do?

`site.py` uses the Flask module to connect routes (URLs) to html pages that will be displayed when someone goes to that part of the website.

You can use the command `python site.py` to run the site live. It should be accessible at `http://localhost:5000`, and you can quit with `CTRL + c`. You can refresh the page and it will update with changes without having to re-run the command.

`python site.py build` will use the `flask_frozen` module to save a frozen snapshot of the site in a directory called `build/`.

### Templates

Templates use the [Jinja2](http://jinja.pocoo.org/docs/2.9/) templating system that comes with Flask to compose html pages. TLDR all the html is defined in the `templates` directory.

The main fancy bit of this that's used here is the template inheritance. `base.html` defines the header, footer, and some display scaling.

Links in templates should use the `url_for` method when referring to internal pages. (See `templates/base.html` for an example).

### Directory Structure

Each page of the site lives in its own directory so that it can be accessed as `mainsite.com/projects`. The `index.html` that is the result of rendering the templates of the corresponding name. This makes it easier to find pages, since you don't have to remember to tack on the `.html` suffix.

If you want to add a new page, then you would need to

1. add a function in `site.py` that with the route you want assocaited with it that renders a template in the `templates/` directory
2. add the template, inheriting from the base template (if you want)

Static files (css, javascript, and images used in pages) live in the `static` directory. You can reference different css or javascript files by adding the appropriate tag on the page you want to use it on, e.g.

### 404 pages

The `.htcaccess` file is configured to use the static `404.html` page as the 404 page. If you remove it, a generic 404 page is used. The `@app.errorhandler(404)` in `site.py` will serve the 404 page when the site is running live from the command `python site.py`.
