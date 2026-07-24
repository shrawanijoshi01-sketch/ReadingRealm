import joblib
import re

df = joblib.load("model/books.pkl")
similarity = joblib.load("model/similarity.pkl")

IMAGE_MAP = {
    "atomic habits": "/images/atomic_habits.jpg",
    "harry potter": "/images/harry_potter.jpg",
    "alchemist": "/images/the_alchemist.jpg",
    "ikigai": "/images/ikigai.jpg",
    "rich dad": "/images/rich_dad_poor_dad.jpg",
    "psychology of money": "/images/psychology_of_money.jpg",
    "silent patient": "/images/silent_patient.jpg",
    "deep work": "/images/deep_work.jpg",
    "alice": "/images/alice.jpg",
    "anne frank": "/images/anne_frank_diary.jpg",
    "beauty": "/images/beauty_and_beast.jpg",
    "cinderella": "/images/cinderella.jpg",
    "einstein": "/images/einstein.jpg",
    "leonardo": "/images/leonardo_da_vinci.jpg",
    "little mermaid": "/images/little_mermaid.jpg",
    "peter pan": "/images/peter_pan.jpg",
    "playing it my way": "/images/playing_it_my_way.jpg",
    "girl on train": "/images/the_girl_on_train.jpg",
    "story of my life": "/images/the_story_of_my_life.jpg",
    "mockingbird": "/images/to_kill_a_mockingbird.jpg",
    "wings of fire": "/images/wongs_of_file.jpg",
    "wongs of file": "/images/wongs_of_file.jpg"
}

def get_book_image(book_row):
    img = book_row.get("image", None)
    if img and isinstance(img, str) and img.strip() and str(img) != "nan":
        return img if img.startswith("/") else f"/{img}"

    title = str(book_row.get("title", "")).lower()
    for key, img_path in IMAGE_MAP.items():
        if key in title:
            return img_path

    slug = re.sub(r'[^a-z0-9]+', '_', title).strip('_')
    return f"/images/{slug}.jpg"


def recommend(book_title, top_n=6):
    query = str(book_title).lower().strip()
    df_titles = df["title"].astype(str).str.lower()

    match = df[df_titles == query]
    if match.empty:
        match = df[df_titles.str.contains(query, regex=False, na=False)]
    if match.empty:
        first_word = query.split()[0] if query.split() else query
        match = df[df_titles.str.contains(first_word, regex=False, na=False)]

    if match.empty:
        return []

    idx = match.index[0]
    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommendations = []

    for i in scores[1:top_n + 1]:
        book = df.iloc[i[0]]
        recommendations.append({
            "title": str(book.get("title", "")),
            "author": str(book.get("author", "")),
            "genre": str(book.get("genre", "")),
            "rating": float(book.get("rating", 4.5)),
            "price": int(book.get("price", 299)),
            "image": get_book_image(book)
        })

    return recommendations