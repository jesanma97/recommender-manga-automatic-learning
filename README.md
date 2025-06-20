# Manga Recommender System with Automatic Learning

This project is a machine learning-based system designed to recommend manga titles using semantic features extracted from synopsis and tags. It incorporates translation services, natural language embeddings, and autoencoders to build a personalized recommendation engine.

## 🔍 Project Features

- **Data Collection from AniList**: Fetches and stores anime/manga metadata into a local database using the AniList API.
- **Translation Pipeline**: Translates non-English text (e.g., Japanese) into English to ensure consistent text processing.
- **Semantic Embeddings**: Generates embeddings from manga synopses and tags using state-of-the-art models (e.g., Sentence Transformers).
- **Autoencoder Modeling**: Learns compressed representations of manga features to identify similarities and enable recommendations.
- **Expandable & Modular**: Designed to allow additional preprocessing, new embedding strategies, and future enhancements.

## 📁 Project Structure

recommender-manga-automatic-learning/
├── anilist/
│ ├── insert-db-base-info.py # Inserts initial AniList data into database
│ └── insert-db-new-info.py # Updates the database with new information
├── training_model/
│ ├── 1 - translator.ipynb # Translates manga synopses and titles
│ ├── 2 - embeddings_synopsis_tags.ipynb # Generates semantic embeddings
│ └── 3 - autoencoders-features.ipynb # Trains autoencoders on features
├── init.py
└── README.md

## ⚙️ Technologies Used

- **Python**
- **Jupyter Notebooks**
- **Transformers / Sentence Transformers**
- **Scikit-learn**
- **TensorFlow / Keras (for Autoencoders)**
- **AniList API**
- **SQLite (or another local DB)**

## 🚀 How to Use

1. **Set up the environment** with the required packages.
2. **Execute the scripts to do web scraping** to collect publisher's data
3. **Run the scripts in `anilist/`** to collect manga/anime data.
4. **Translate and preprocess text** with notebook 1.
5. **Generate embeddings** using notebook 2.
6. **Train and evaluate the recommender** with notebook 3.

## 📌 Notes

- Make sure to set up your API key for AniList access.
- The translation step may require internet access or a supported API key (e.g., Google Translate).
- You can tweak the autoencoder architecture to better fit your dataset size and goals.

## 🧠 Future Improvements

- Incorporate collaborative filtering.
- Add a web interface for users to input preferences.
- Optimize embedding models for faster inference.
