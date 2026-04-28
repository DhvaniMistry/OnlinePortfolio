from pathlib import Path
import html
import shutil

def slugify(title):
    return title.strip().lower().replace(" ", "-")

def image_name(title):
    return title.strip().lower().replace(" ", "_")

def make_recipe_card(title, category, tag, details):
    slug = slugify(title)
    img = image_name(title)

    href = f"{slug}.html"
    image = f"photos/recipe/{img}.jpg"
    alt = title

    return f'''
        <a href="{html.escape(href)}" class="recipe-card">
          <div class="recipe-image-wrap">
            <img src="{html.escape(image)}" alt="{html.escape(alt)}">
          </div>
          <div class="recipe-content">
            <div class="recipe-meta"><span>{html.escape(category)}</span><span class="recipe-tag">{html.escape(tag)}</span></div>
            <h2 class="recipe-title">{html.escape(title)}</h2>
            <p class="recipe-details">{html.escape(details)}</p>
          </div>
        </a>
'''

def create_recipe_file(title):
    slug = title.strip().lower().replace(" ", "-")
    file_path = Path(__file__).parent / f"{slug}.html"

    if file_path.exists():
        print(f"⚠️ File {file_path.name} already exists. Skipping creation.")
        return

    template = f""" """

    file_path.write_text(template, encoding="utf-8")
    print(f"📄 Created {file_path.name}")

def add_recipe_card(file_path, card_html):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"{file_path} was not found.")

    content = path.read_text(encoding="utf-8")

    grid_start = content.find('<section class="recipe-grid">')
    if grid_start == -1:
        raise ValueError('Could not find <section class="recipe-grid">.')

    grid_end = content.find('</section>', grid_start)
    if grid_end == -1:
        raise ValueError("Could not find the end of the recipe grid section.")

    backup_path = path.with_suffix(".backup.html")
    shutil.copy(path, backup_path)

    updated = content[:grid_end] + card_html + content[grid_end:]
    path.write_text(updated, encoding="utf-8")

    print("\n✅ Recipe added!")
    print(f"Backup saved as: {backup_path}")

def main():
    print("Add a recipe")
    print("------------")

    file_path = "recipes.html"

    title = input("Title: ").strip()
    category = input("Category (Fusion/Authentic/Fresh): ").strip()
    tag = input("Tag (Pasta/Soup/etc): ").strip()
    details = input("Details (e.g. 25 min): ").strip()

    print("\nPreview:")
    print(f"File: {title.lower().replace(' ', '-')}.html")
    print(f"Image: photos/recipe/{title.lower().replace(' ', '_')}.jpg")

    confirm = input("\nAdd this recipe? [y/N]: ").strip().lower()

    if confirm != "y":
        print("Cancelled.")
        return

    card = make_recipe_card(title, category, tag, details)
    add_recipe_card(file_path, card)
    create_recipe_file(title)

if __name__ == "__main__":
    main()