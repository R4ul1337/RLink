from flask import Blueprint, render_template, jsonify, current_app
import json
import os

# Define the blueprint and name it 'main_bp'
main_bp = Blueprint('main', __name__)

CHANGELOG_FILE = os.path.join("data", "changelog", "changelog.json")
IMAGE_FOLDER = "data/changelog/img/"
WEBSITES_DIR = os.path.join('data', 'websites')

def load_categories():
    categories = []
    # Loop through all JSON files in the 'websites' directory
    for file_name in os.listdir(WEBSITES_DIR):
        if file_name.endswith('.json'):
            file_path = os.path.join(WEBSITES_DIR, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                category_data = json.load(f)
                categories.append(category_data)
    return categories

def load_data(file_name):
    with open(f"data/{file_name}") as file:
        return json.load(file)

categories = load_data("categories.json")
websites = load_data("websites.json")


@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

"""@main_bp.route('/browse')
def browse():
    return render_template('browse.html')"""

changelog = [
    {
        "version": "BETA V0.3.0",
        "date": "2025-01-28",
        "short_description": "Building the Browsing function!",
        "full_description": "We've officially begun developing the browsing page, added test categories and websites, built a strong backend foundation for future updates regarding the category/websites browsing etc. updates. Go check it out now! Click the 'Browse' button from the navbar or simply click the 'Browse Categories' button on the main page."
    },
    {
        "version": "BETA V0.2.1",
        "date": "2025-01-24",
        "short_description": "Remodeled pages, UI updates, New pages",
        "full_description": "This is quite a big update - especially to the UI. \nWe've changed: \n\n-> the 'See browse' button design; \n->changed the color from the 'Learn More' button;\n-> The design of the About page. \n\nWe've added: \n-> 'About the developer' in the about page; \n-> 'Coming Soon' screen in both browse & News pages; \n-> Completly new design to the changelog page"
    },
    {   "version": "BETA V0.1.5",
        "date": "2025-01-23",
        "short_description": "Added new UI elements and improved them",
        "full_description": "Added new, more animated & responsive buttons, added a visual text of the current version of the website, made some changes to the Changelog page (remaining just to remodel it soon)."
    },
    {
        "version": "BETA V0.1.2",
        "date": "2025-01-22",
        "short_description": "Fixed minor UI bugs and improved navigation.",
        "full_description": "In this release, we addressed several UI bugs and made improvements to the navigation bar, including better hover effects and smoother scrolling."
    },
    {
        "version": "BETA V0.1.1",
        "date": "2025-01-18",
        "short_description": "Added the core & basic functions to the site",
        "full_description": "New core & basic functions ware added to the website, that are a strong foundation to the future updates that will be released."
    }
]

@main_bp.route('/changelog')
def changelog_page():
    try:
        with open(CHANGELOG_FILE, "r", encoding="utf-8") as file:
            changelog = json.load(file)

        # Convert image filenames to full paths
        for entry in changelog:
            if "images" in entry and isinstance(entry["images"], list):
                entry["images"] = [os.path.join(IMAGE_FOLDER, img) for img in entry["images"]]

    except (FileNotFoundError, json.JSONDecodeError) as e:
        changelog = []  # Fallback if file is missing or has errors

    return render_template('changelog.html', changes=changelog)

@main_bp.route('/news')
def news():
    news_file = os.path.join(current_app.root_path, 'data', 'News', 'news.json')
    try:
        with open('data/News/news.json') as f:
            news_data = json.load(f)
    except Exception as e:
        print(f"Error loading news data: {e}")
        news_data = []

    return render_template('news.html', news=news_data)


@main_bp.route('/categories')
def browse_categories():
    # categories = load_categories()
    return render_template('categories.html', categories=categories)

@main_bp.route('/categories/<slug>')
def category_detail(slug):
    file_path = os.path.join(WEBSITES_DIR, f"{slug}.json")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            category = json.load(f)
        return render_template('category_detail.html', category=category)
    else:
        return "Category not found", 404
    
@main_bp.route('/projects/main')
def projects_main():
    # Load projects from the JSON file
    with open('data/Projects/projects.json', 'r') as file:
        projects = json.load(file)
    return render_template('projects/main.html', projects=projects)

@main_bp.route('/projects/<slug>')
def project_detail(slug):
    # Load projects from JSON
    with open('data/Projects/projects.json', 'r') as file:
        projects = json.load(file)

    # Find the project by its slug
    project = next((p for p in projects if p['slug'] == slug), None)
    if not project:
        return "Project not found", 404

    return render_template('projects/project_detail.html', project=project)
