# google-play-store-data-cleaning-eda

# Google Play Store Data Cleaning & Exploratory Data Analysis (EDA)

## 📌 Project Overview

This project focuses on cleaning and exploring Google Play Store app data to understand the mobile app market. Using Python and data analysis libraries, I prepare the dataset for analysis, investigate app characteristics, and explore patterns related to ratings, categories, pricing, and installs.

The goal is to transform raw data into meaningful insights through data cleaning, exploratory data analysis, and visualization.

## 🎯 Objectives

- Clean and preprocess raw Google Play Store data.
- Handle missing values and duplicate records.
- Identify and correct data type inconsistencies.
- Explore app categories, ratings, prices, and install counts.
- Analyze relationships between app attributes.
- Visualize patterns and trends in the app market.

## 📂 Dataset

The dataset contains information about applications listed on the Google Play Store.

Potential fields include:
- **App:** Application name.
- **Category:** App category.
- **Rating:** User rating.
- **Reviews:** Number of user reviews.
- **Installs:** Number of installations.
- **Type:** Free or paid.
- **Price:** App price.
- **Content Rating:** Intended audience.
- **Genres:** App genre.
- **Android Ver:** Required Android version.

*Note: The fields listed above should be checked against the actual dataset used in this project.*

## 🛠️ Tools & Technologies

- **Python** — data analysis and preprocessing.
- **Pandas** — data manipulation and cleaning.
- **NumPy** — numerical operations.
- **Matplotlib** — data visualization.
- **Seaborn** — statistical visualization.
- **Jupyter Notebook** — interactive analysis.

## 🔍 Project Workflow

### 1. Data Loading
- Import the dataset into Python.
- Inspect its structure, dimensions, and column types.

### 2. Data Cleaning
- Identify missing and duplicate values.
- Handle inconsistent formats and data types.
- Clean numerical fields such as prices, installs, and reviews.
- Prepare the data for reliable analysis.

### 3. Exploratory Data Analysis
- Examine the distribution of app ratings.
- Compare app categories.
- Explore free versus paid applications.
- Investigate installs and review counts.
- Analyze relationships between ratings, reviews, and other app attributes.

### 4. Data Visualization
Use charts and plots to communicate important patterns and make the findings easier to understand.

## 📊 Key Questions

- Which app categories are most common?
- How are app ratings distributed?
- Are free apps more common than paid apps?
- Which categories attract the most installs?
- Is there a relationship between reviews and installs?
- How do ratings differ across app categories?

## 💡 Key Findings

This section will summarize the main discoveries from the analysis.

Examples of findings to investigate:
- The most common app categories.
- Differences between free and paid apps.
- Categories with higher average ratings.
- Relationships between reviews and installation counts.

*Add the actual findings and supporting figures after reviewing the results in your notebook.*

## 📁 Repository Structure

```text
Android_AppStore_Data/
├── data/                  # Dataset files, if included
├── notebooks/             # Analysis notebooks, if included
├── images/                # Visualizations, if included
└── README.md              # Project documentation
```

*Update this structure to match the actual files and folders in the repository.*

## 🚀 How to Run the Project

1. Clone the repository:

   ```bash
   git clone https://github.com/majd09/google-play-store-data-cleaning-eda.git
   ```

2. Navigate to the project directory:

   ```bash
   cd google-play-store-data-cleaning-eda
   ```

3. Install the required libraries:

   ```bash
   pip install pandas numpy matplotlib seaborn jupyter
   ```

4. Launch Jupyter Notebook:

   ```bash
   jupyter notebook
   ```

5. Open the project notebook and run the cells.

## 📚 Skills Demonstrated

- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Data manipulation with Pandas
- Numerical analysis with NumPy
- Data visualization
- Analytical thinking and data storytelling

## 👤 Author

**Majd**

GitHub: [@majd09](https://github.com/majd09)

## 📄 License

This project is intended for educational and portfolio purposes. Add a license if you intend to specify the terms under which others may use or distribute your work.
