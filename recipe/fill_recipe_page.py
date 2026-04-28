from pathlib import Path
import html
import re


def slugify(title):
    return title.strip().lower().replace(" ", "-")


def image_name(title):
    return title.strip().lower().replace(" ", "_")


def ask_required(label):
    value = input(f"{label}: ").strip()
    while not value:
        value = input(f"{label} is required. Try again: ").strip()
    return value


def ask_list(label):
    print(f"\n{label}")
    print("Enter one item per line. Press Enter on a blank line when done.")

    items = []
    while True:
        item = input("- ").strip()
        if not item:
            break
        items.append(item)

    return items


def make_list_items(items):
    return "\n".join(f"        <li>{html.escape(item)}</li>" for item in items)


def make_steps(steps):
    return "\n".join(f"        <li>{html.escape(step)}</li>" for step in steps)

def make_recipe_html(title, category, tag, time, servings, description, ingredients, steps, materials, tip):
    image = f"photos/recipe/{image_name(title)}.jpg"

    ingredient_items = "\n".join(
        f"                        <li>{html.escape(item)}</li>" for item in ingredients
    )

    step_cards = "\n".join(
        f"""                  <div class="step-card rounded-2xl p-5">
                     <p class="text-primary font-bold mb-1">Step {i} — {html.escape(step.split('.')[0])}</p>
                     <p class="text-textSoft text-sm leading-7">
                        {html.escape(step)}
                     </p>
                  </div>"""
        for i, step in enumerate(steps, start=1)
    )

    material_items = "\n".join(
        f"                  <li>{html.escape(item)}</li>" for item in materials
    )

    return f"""<!DOCTYPE html>
<html lang="en">
   <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{html.escape(title)}</title>
      <script src="https://cdn.tailwindcss.com"></script>
      <script>tailwind.config={{theme:{{extend:{{colors:{{base:'#1C1C1E',surface:'#2A2A2D',primary:'#D7A7A0',secondary:'#A8C3A0',accent:'#E9CFCB',deepGreen:'#7B9B77',warmGold:'#E6B56A',spice:'#D9825B',textMain:'#FAF9F8',textSoft:'#C9C9C9'}},fontFamily:{{sans:['Inter','system-ui','sans-serif']}},boxShadow:{{soft:'0 18px 45px rgba(0,0,0,0.35)',glow:'0 0 35px rgba(215,167,160,0.18)'}}}}}}</script>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
      <style>.glass-card{{background:linear-gradient(145deg,rgba(42,42,45,.95),rgba(28,28,30,.92));border:1px solid rgba(215,167,160,.22)}}.recipe-chip{{border:1px solid rgba(233,207,203,.2);background:rgba(28,28,30,.65)}}.step-card{{background:rgba(28,28,30,.72);border:1px solid rgba(168,195,160,.18)}}</style>
   </head>

   <body class="min-h-screen bg-base font-sans text-textMain">
      <div class="fixed inset-0 -z-10 overflow-hidden">
         <div class="absolute -top-32 -right-24 h-80 w-80 rounded-full bg-primary/20 blur-3xl"></div>
         <div class="absolute top-64 -left-24 h-80 w-80 rounded-full bg-deepGreen/20 blur-3xl"></div>
         <div class="absolute bottom-0 right-1/4 h-80 w-80 rounded-full bg-spice/10 blur-3xl"></div>
      </div>

      <main class="max-w-6xl mx-auto px-4 py-10 md:py-14">
         <a href="../recipes.html" class="inline-flex items-center gap-2 text-textSoft hover:text-accent transition-colors mb-8">
            <i class="fas fa-arrow-left"></i> Back to recipe cards
         </a>

         <section class="grid grid-cols-1 lg:grid-cols-[1.05fr_0.95fr] gap-8 items-stretch mb-10">
            <div class="glass-card rounded-3xl p-6 md:p-8 shadow-soft flex flex-col justify-center">
               <p class="text-primary text-sm font-bold tracking-[0.28em] uppercase mb-4">{html.escape(category)} Recipe</p>
               <h1 class="text-4xl md:text-6xl font-extrabold text-accent leading-tight mb-5">
                  {html.escape(title)}
               </h1>
               <p class="text-textSoft text-base md:text-lg leading-8 mb-7">
                  {html.escape(description)}
               </p>

               <div class="flex flex-wrap gap-3 mb-8">
                  <span class="recipe-chip rounded-full px-4 py-2 text-sm text-secondary"><i class="fas fa-magic mr-2"></i>{html.escape(category)}</span>
                  <span class="recipe-chip rounded-full px-4 py-2 text-sm text-warmGold"><i class="fas fa-utensils mr-2"></i>{html.escape(tag)}</span>
                  <span class="recipe-chip rounded-full px-4 py-2 text-sm text-textSoft"><i class="far fa-clock mr-2"></i>{html.escape(time)}</span>
                  <span class="recipe-chip rounded-full px-4 py-2 text-sm text-textSoft"><i class="fas fa-users mr-2"></i>{html.escape(servings)}</span>
               </div>

               <div class="grid grid-cols-3 gap-3 text-center">
                  <div class="rounded-2xl bg-surface/70 p-4 border border-primary/15">
                     <p class="text-xl font-bold text-secondary">{html.escape(category)}</p>
                     <p class="text-xs text-textSoft">style</p>
                  </div>
                  <div class="rounded-2xl bg-surface/70 p-4 border border-primary/15">
                     <p class="text-xl font-bold text-primary">{html.escape(tag)}</p>
                     <p class="text-xs text-textSoft">kind</p>
                  </div>
                  <div class="rounded-2xl bg-surface/70 p-4 border border-primary/15">
                     <p class="text-xl font-bold text-warmGold">{html.escape(servings)}</p>
                     <p class="text-xs text-textSoft">yield</p>
                  </div>
               </div>
            </div>

            <div class="rounded-3xl overflow-hidden shadow-soft border border-primary/20 bg-surface">
               <img src="{html.escape(image)}" alt="{html.escape(title)}" class="w-full h-full min-h-[360px] object-cover" onerror="this.style.display='none';this.nextElementSibling.classList.remove('hidden');">
               <div class="hidden min-h-[360px] p-8 bg-gradient-to-br from-surface via-base to-deepGreen/40 flex items-center justify-center text-center">
                  <div>
                     <i class="fas fa-utensils text-6xl text-secondary mb-4"></i>
                     <p class="text-accent font-semibold">Add your food photo here</p>
                     <p class="text-textSoft text-sm mt-2">Save it as <code>{html.escape(image)}</code></p>
                  </div>
               </div>
            </div>
         </section>

         <section class="grid grid-cols-1 lg:grid-cols-[0.9fr_1.1fr] gap-8 mb-10">
            <div class="glass-card rounded-3xl p-6 md:p-8 shadow-soft">
               <div class="flex items-center gap-3 mb-6">
                  <i class="fas fa-shopping-basket text-secondary text-2xl"></i>
                  <h2 class="text-2xl md:text-3xl font-bold text-accent">Ingredients</h2>
               </div>

               <ul class="list-disc ml-5 space-y-2 text-textSoft">
{ingredient_items}
               </ul>
            </div>

            <div class="glass-card rounded-3xl p-6 md:p-8 shadow-soft">
               <div class="flex items-center gap-3 mb-6">
                  <i class="fas fa-list-ol text-secondary text-2xl"></i>
                  <h2 class="text-2xl md:text-3xl font-bold text-accent">Method</h2>
               </div>

               <div class="space-y-4">
{step_cards}
               </div>
            </div>
         </section>

         <section class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
            <div class="glass-card rounded-3xl p-6 shadow-soft">
               <i class="fas fa-toolbox text-warmGold text-3xl mb-4"></i>
               <h3 class="text-xl font-bold text-accent mb-3">Materials</h3>
               <ul class="list-disc ml-5 space-y-2 text-textSoft">
{material_items}
               </ul>
            </div>

            <div class="glass-card rounded-3xl p-6 shadow-soft">
               <i class="fas fa-heart text-primary text-3xl mb-4"></i>
               <h3 class="text-xl font-bold text-accent mb-3">Diary Note / Tip</h3>
               <p class="text-sm text-textSoft leading-7">
                  {html.escape(tip)}
               </p>
            </div>
         </section>
      </main>
   </body>
</html>"""

def main():
    print("Fill individual recipe page")
    print("---------------------------")

    title = ask_required("Recipe title")
    category = ask_required("Category, example Fusion / Authentic / Fresh")
    tag = ask_required("Tag, example Khichdi / Pasta / Soup")
    time = ask_required("Time, example 30–35 min")
    servings = ask_required("Servings, example 3 servings")
    description = ask_required("Short description")

    ingredients = ask_list("Ingredients")
    steps = ask_list("Method steps")
    tip = ask_required("Tip")
    materials = ask_list("Materials")

    file_name = f"{slugify(title)}.html"
    file_path = Path(__file__).parent / file_name

    print("\nPreview:")
    print(f"File: {file_name}")
    print(f"Image: photos/recipe/{image_name(title)}.jpg")

    confirm = input("\nCreate/overwrite this recipe page? [y/N]: ").strip().lower()

    if confirm != "y":
      print("Cancelled.")
      return

    html_content = make_recipe_html(
        title=title,
        category=category,
        tag=tag,
        time=time,
        servings=servings,
        description=description,
        ingredients=ingredients,
        steps=steps,
        materials=materials,
        tip=tip,
    )

    file_path.write_text(html_content, encoding="utf-8")
    print(f"\nRecipe page created: {file_path}")


if __name__ == "__main__":
    main()