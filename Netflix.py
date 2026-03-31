# Netflix Content Analysis Project

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_csv('netflix_titles.csv')

# -----------------------------
# 2. Data Exploration
# -----------------------------
print("Dataset Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nMissing Values:\n", df.isnull().sum())

# -----------------------------
# 3. Data Cleaning
# -----------------------------
# Drop rows where both director and cast are missing
df = df.drop(df[df['director'].isnull() & df['cast'].isnull()].index)

# Fill missing values
df['country'] = df['country'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['rating'] = df['rating'].fillna('Unknown')

# Convert date column
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year

# -----------------------------
# 4. Analysis
# -----------------------------

# Content type distribution
type_counts = df['type'].value_counts()

# Top 10 countries by content count
country_counts = (
    df.groupby(['country', 'type'])
    .size()
    .reset_index(name='count')
    .sort_values(by='count', ascending=False)
)

top_countries = country_counts.head(10)

# Content release trend
year_counts = df['release_year'].value_counts().sort_index()

# -----------------------------
# 5. Visualization
# -----------------------------

# Style
sns.set_style("whitegrid")

# 1. Content Type Distribution
plt.figure(figsize=(6, 4))
sns.countplot(x='type', data=df, palette='pastel')
plt.title('Distribution of Movies vs TV Shows')
plt.xlabel('Content Type')
plt.ylabel('Count')
plt.show()

# 2. Top Countries Producing Content
plt.figure(figsize=(10, 6))
sns.barplot(
    x='count',
    y='country',
    hue='type',
    data=top_countries,
    palette='pastel'
)
plt.title('Top 10 Countries by Content on Netflix')
plt.xlabel('Number of Titles')
plt.ylabel('Country')
plt.show()

# 3. Content Release Trend Over Years
plt.figure(figsize=(10, 6))
sns.lineplot(
    x=year_counts.index,
    y=year_counts.values
)
plt.title('Content Released Over the Years')
plt.xlabel('Release Year')
plt.ylabel('Number of Titles')
plt.show()