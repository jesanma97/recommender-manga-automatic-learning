# Manga Recommender System with Automatic Learning

This project is a machine learning-based system designed to recommend manga titles using semantic features extracted from synopsis and tags. It incorporates translation services, web scraping, natural language embeddings, and deep learning (autoencoders) to build a powerful recommendation engine.

## 🔍 Project Features

- **AniList Web Scraping**: Gathers anime and manga metadata using the AniList API and inserts it into a local database.
- **Translation Pipeline**: Automatically translates manga titles and synopses to English for uniform processing.
- **Semantic Embeddings**: Uses Sentence Transformers to generate meaningful vector representations of text.
- **Autoencoder Modeling**: Learns dense representations of manga based on their features for similarity comparison.
- **Clustering Algorithms**: Implements K-Means, DBSCAN, and HDBSCAN to analyze groups of similar manga.
- **Top-K Recommender**: Generates Top-10 recommendations based on embedding similarity.

## 📁 Project Structure

```
recommender-manga-automatic-learning/
├── anilist/
│ ├── insert-db-base-info.py # Scrapes and inserts base AniList data
│ └── insert-db-new-info.py # Updates database with newly fetched entries
├── training_model/
│ ├── 1 - translator.ipynb # Translates manga synopses and titles to English
│ ├── 2 - embeddings_synopsis_tags.ipynb # Generates sentence embeddings for synopses and tags
│ ├── 3 - autoencoders-features.ipynb # Trains and tests autoencoders on manga features
│ ├── 4 - Clustering - kmeans.ipynb # Applies K-Means clustering to embeddings
│ ├── 5 - Clustering - dbscan.ipynb # Applies DBSCAN clustering
│ ├── 6 - Clustering - hdbscan.ipynb # Applies HDBSCAN clustering
│ ├── 7 - Top 10 Embeddings.ipynb # Finds top-10 most similar manga per entry
│ └── best_autoencoder.h5 # Saved autoencoder model
├── init.py
└── README.md
```

## ⚙️ Technologies Used

- **Python**
- **Jupyter Notebooks**
- **TensorFlow / Keras**
- **Scikit-learn**
- **Sentence Transformers**
- **HDBSCAN / DBSCAN / KMeans**
- **AniList GraphQL API**
- **SQLite**

## 🚀 How to Use

1. **Install dependencies** from `requirements.txt` or manually via pip.
2. **Run `insert-db-base-info.py`** to collect the initial data from AniList.
3. **Translate synopses and titles** using `1 - translator.ipynb`.
4. **Generate embeddings** with `2 - embeddings_synopsis_tags.ipynb`.
5. **Train and evaluate autoencoders** in `3 - autoencoders-features.ipynb`.
6. **Explore clustering methods** in notebooks 4 to 6.
7. **Use notebook 7** to compute and view Top-10 recommendations.

## 📌 Notes

- Make sure to configure your AniList API credentials before running the scraper.
- The translation step requires internet access or a valid API key (e.g., for Google Translate).
- The clustering analysis is optional but useful for understanding relationships in the manga space.
