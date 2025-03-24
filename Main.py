# %%
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from goose3 import Goose
import sqlite3
import pandas as pd

def load_translation_pipeline(model_name):
    """
    Loads the translation pipeline for the specified model.
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        return pipeline("translation", model=model, tokenizer=tokenizer)
    except Exception as e:
        print(f"Error loading model {model_name}: {e}")
        return None

def extract_article_content(url):
    """
    Extracts the main content of a news article from the URL.
    """
    g = Goose()
    try:
        article = g.extract(url=url)
        return article.title, article.cleaned_text
    except Exception as e:
        print(f"Error extracting article: {e}")
        return None, None

def process_and_translate(db_path, table_name, output_excel, max_words=60):
    """
    Extracts articles, summarizes them, and translates summaries into Indian languages.
    """
    # Connect to the database
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT link FROM {table_name}", conn)

    # Load translation pipelines
    pipelines = {
        "hi": load_translation_pipeline("Helsinki-NLP/opus-mt-en-hi"),
        "te": load_translation_pipeline("Helsinki-NLP/opus-mt-en-te"),
    }

    summaries = []
    for index, row in df.iterrows():
        url = row['link']
        title, content = extract_article_content(url)
        if not content:
            summaries.append({"Title": title, "Summary": "Extraction Failed", "Link": url})
            continue

        # Dummy summarization (replace with actual summarization logic)
        summary = content[:max_words] + "..."

        # Translate summaries
        translations = {}
        for lang, translator in pipelines.items():
            if translator:
                try:
                    # Adjust max_length to avoid truncation
                    translated = translator(summary, max_length=400)
                    translations[lang] = translated[0]['translation_text']
                except Exception as e:
                    print(f"Error during translation to {lang}: {e}")
                    translations[lang] = None

        summaries.append({
            "Title": title,
            "Summary": summary,
            "Link": url,
            **translations
        })

    # Save results to Excel
    df_summaries = pd.DataFrame(summaries)
    df_summaries.to_excel(output_excel, index=False)
    print(f"Summaries and translations saved to {output_excel}")

if __name__ == '__main__':
    db_path = "news_articles_shortened.db"
    table_name = "articles"
    output_excel = "news_summaries_translations_shortened.xlsx"
    process_and_translate(db_path, table_name, output_excel, max_words=60)


# %%



