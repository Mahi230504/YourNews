
# News Article Summarization and Translation

This project extracts news articles from URLs stored in a SQLite database, summarizes the content, and translates the summaries into Indian languages (Hindi and Telugu).

## Features

- Extracts main article text and title using **Goose3**.
- Summarizes articles (basic first `n` words — can be enhanced later).
- Translates summaries into:
  - Hindi (`hi`)
  - Telugu (`te`)
- Saves the output to an Excel file (`.xlsx`).

## Requirements

- Python 3.8+
- Install the required packages:

```bash
pip install transformers goose3 pandas openpyxl
```

*(You may also need `torch` if not already installed.)*

```bash
pip install torch
```

## How to Use

1. **Prepare the SQLite database**:
   - The database (`news_articles_shortened.db`) should contain a table (`articles`) with a column named `link` (news URLs).

2. **Run the script**:

```bash
python your_script_name.py
```

This will:
- Extract articles.
- Summarize the content (first `60` words by default).
- Translate summaries into Hindi and Telugu.
- Save everything into an Excel file `news_summaries_translations_shortened.xlsx`.

## Configuration

- **Database path**: Change the `db_path` variable if your database has a different name.
- **Table name**: Update the `table_name` variable if the table is named differently.
- **Max words**: Adjust `max_words` parameter to change summary length.

## Folder Structure

```
.
├── news_articles_shortened.db
├── news_summaries_translations_shortened.xlsx
├── your_script_name.py
└── README.md
```

## Notes

- Current summarization is **basic** (just trimming words).  
  You can replace it with a better summarization model later (like **BART**, **T5**).
- The translation uses **Helsinki-NLP** models from Hugging Face.


