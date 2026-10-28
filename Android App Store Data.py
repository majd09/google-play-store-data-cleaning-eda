import pandas as pd
import plotly.express as px

df_apps = pd.read_excel(
    "google_play_store_tables.xlsx",
    engine="openpyxl")

print("Original shape:", df_apps.shape)


df_apps = df_apps.loc[:, ~df_apps.columns.duplicated()]

df_apps["_Source_Excel_Row"] = range(2, len(df_apps) + 2)

audit_records = []

print("\nColumns after removing duplicate names:")
print(df_apps.columns.tolist())

removed_columns = [
    col for i, col in enumerate(df_apps.columns)
    if col in df_apps.columns[:i] ]

print("\nDuplicate column names removed:")
print(removed_columns)


columns_to_remove = [
    "Last Updated",
    "Current Ver",
    "Android Ver"
]

df_apps = df_apps.drop( columns=columns_to_remove)

print("\n Data shape after removing unnecessary columns:", df_apps.shape)



print("\n--- Missing Values Before Cleaning ---")
print(df_apps.drop(columns="_Source_Excel_Row").isna().sum())

missing_percent = (
    df_apps.drop(columns="_Source_Excel_Row").isna()
    .mean() * 100)

print("\nMissing value percentages:")
print(missing_percent.sort_values(ascending=False))

essential_columns = ["App","Category","Reviews","Rating", "Installs" ]
missing_essential = df_apps[essential_columns].isna().any(axis=1)
print("Rows flagged:", missing_essential.sum())

for idx in df_apps.index[missing_essential]:
    missing_fields = df_apps.loc[idx, essential_columns].index[df_apps.loc[idx, essential_columns].isna()].tolist()

    audit_records.append({
        "Excel_Row": df_apps.loc[idx, "_Source_Excel_Row"],
        "App": df_apps.loc[idx, "App"],
        "Removal_Reason": "Missing essential information",
        "Details": ", ".join(missing_fields)})

df_apps_clean = df_apps.loc[~missing_essential].copy()

print(
    "\nRows removed for missing essential information:",
    missing_essential.sum()
)
print("Shape after handling missing values:", df_apps_clean.shape)


data_for_duplicate_check = df_apps_clean.drop(
    columns="_Source_Excel_Row"
)
duplicated_rows = df_apps_clean.loc[
    data_for_duplicate_check.duplicated()
]

print("Duplicate rows shape:", duplicated_rows.shape)
print("\nFirst five duplicate rows:")
print(duplicated_rows.head())


duplicate_rows = data_for_duplicate_check.duplicated(keep="first")
print("\nTotal exact duplicate rows:", duplicate_rows.sum())

for idx in df_apps_clean.index[duplicate_rows]:
    audit_records.append({
        "Excel_Row": df_apps_clean.loc[idx, "_Source_Excel_Row"],
        "App": df_apps_clean.loc[idx, "App"],
        "Removal_Reason": "Exact duplicate row",
        "Details": "Same data as an earlier row"
    })


df_apps_clean = df_apps_clean.loc[~duplicate_rows].copy()
print("Shape after removing duplicates:", df_apps_clean.shape)




numeric_columns = ["Rating", "Reviews", "Price", "Installs"]

original_numeric_values = df_apps_clean[numeric_columns].copy()

df_apps_clean["Rating"] = pd.to_numeric(
    df_apps_clean["Rating"],
    errors="coerce")

df_apps_clean["Reviews"] = pd.to_numeric(
    df_apps_clean["Reviews"],
    errors="coerce"
)

df_apps_clean["Price"] = pd.to_numeric(
    df_apps_clean["Price"]
    .astype("string")
    .str.replace("$", "", regex=False)
    .str.strip(),
    errors="coerce"
)

df_apps_clean["Installs"] = pd.to_numeric(
    df_apps_clean["Installs"]
    .astype("string")
    .str.replace(",", "", regex=False)
    .str.replace("+", "", regex=False)
    .str.strip(),
    errors="coerce"
)

print("\n Data types after conversion:")
print(df_apps_clean[numeric_columns].dtypes)




print("\n--- Numeric Conversion Failures ---")

conversion_failed = pd.Series(
    False,
    index=df_apps_clean.index
)

for column in numeric_columns:
    failed = (original_numeric_values[column].notna() & df_apps_clean[column].isna())

    print(f"\n{column} conversion failures:", failed.sum())

    if failed.any():
        print("Examples of original values:")
        print(
            original_numeric_values.loc[failed, column]
            .value_counts()
            .head(10)
        )

    conversion_failed |= failed


invalid_ratings = (
    df_apps_clean["Rating"].notna()
    & (
        (df_apps_clean["Rating"] < 1)
        | (df_apps_clean["Rating"] > 5)
    )
)

negative_values = (
    (df_apps_clean["Price"] < 0)
    | (df_apps_clean["Reviews"] < 0)
    | (df_apps_clean["Installs"] < 0)
)


invalid_reasons = pd.DataFrame(index=df_apps_clean.index)

invalid_reasons["Invalid rating"] = invalid_ratings
invalid_reasons["Negative numeric value"] = negative_values
invalid_reasons["Numeric conversion failure"] = conversion_failed

invalid_rows = invalid_reasons.any(axis=1)

print("\nRows with invalid ratings:", invalid_ratings.sum())
print("Rows with negative numeric values:", negative_values.sum())
print("Rows with conversion failures:", conversion_failed.sum())

for idx in df_apps_clean.index[invalid_rows]:
    reasons = invalid_reasons.columns[
       invalid_reasons.loc[idx].fillna(False).to_numpy(dtype=bool)
    ].tolist()

    audit_records.append({
        "Excel_Row": df_apps_clean.loc[idx, "_Source_Excel_Row"],
        "App": df_apps_clean.loc[idx, "App"],
        "Removal_Reason": "; ".join(reasons),
        "Details": "See the original Excel row and conversion report"
    })

df_apps_clean = df_apps_clean.loc[~invalid_rows].copy()

print("\nRows removed for invalid numeric data:", invalid_rows.sum())
print("Rows remaining:", len(df_apps_clean))


text_columns = [
    "App",
    "Category",
    "Type",
    "Content Rating",
    "Genres"
]

for column in text_columns:
    df_apps_clean[column] = (
        df_apps_clean[column]
        .astype("string")
        .str.strip()
    )

print("\nText columns cleaned.")


print("\n--- App Type Values Before Normalization ---")
print(df_apps_clean["Type"].value_counts(dropna=False))

# Standardize capitalization and whitespace.
df_apps_clean["Type"] = (
    df_apps_clean["Type"]
    .str.strip()
    .str.title()
)

print("\n--- App Type Values After Normalization ---")
print(df_apps_clean["Type"].value_counts(dropna=False))

expected_types = ["Free", "Paid"]

unexpected_types = df_apps_clean.loc[
    df_apps_clean["Type"].notna()
    & ~df_apps_clean["Type"].isin(expected_types),
    "Type"
]

print("\nUnexpected app type values:")
print(unexpected_types.value_counts())



print("\nCategory values:")
print(df_apps_clean["Category"].value_counts())

print("\nContent Rating values:")
print(df_apps_clean["Content Rating"].value_counts())

repeated_apps = df_apps_clean[
    df_apps_clean["App"].duplicated(keep=False)
].sort_values(["App", "Category", "Reviews"])

print("\nRows with repeated app names:", len(repeated_apps))

if not repeated_apps.empty:
    repeated_columns = [
        "App",
        "Category",
        "Type",
        "Rating",
        "Reviews",
        "Installs",
        "_Source_Excel_Row"
    ]

    print("\nExamples of repeated app names:")
    print(
        repeated_apps[repeated_columns]
        .head(50)
        .to_string(index=False)
    )

    repeated_apps.drop(
        columns="_Source_Excel_Row"
    ).to_csv(
        "google_play_store_repeated_app_names.csv",
        index=False
    )

    print(
        "\nRepeated app records saved to "
        "google_play_store_repeated_app_names.csv"
    )
else:
    print("No repeated app names found.")

size_text = (
    df_apps_clean["Size"]
    .astype("string")
    .str.strip()
    .str.upper()
)

size_values = pd.to_numeric(
    size_text.str.extract(r"^(\d+(?:\.\d+)?)\s*[MK]$")[0],
    errors="coerce"
)

size_units = size_text.str.extract(
    r"^\d+(?:\.\d+)?\s*([MK])$"
)[0]


df_apps_clean["Size_MBs"] = size_values.copy()

is_kilobytes = size_units == "K"

df_apps_clean.loc[is_kilobytes, "Size_MBs"] /= 1024

# Unknown formats remain missing.
df_apps_clean.loc[
    size_units.isna(), "Size_MBs"
] = float("nan")

print("\nSize conversion examples:")
print(df_apps_clean[["Size", "Size_MBs"]].head(10))

print(
    "\nMissing numeric sizes:",
    df_apps_clean["Size_MBs"].isna().sum()
)






unparsed_sizes = df_apps_clean.loc[
    df_apps_clean["Size"].notna()
    & df_apps_clean["Size_MBs"].isna(),
    "Size"
]

print("\n--- Unparsed Size Values ---")
print("Rows with unparsed, non-missing sizes:", len(unparsed_sizes))

if not unparsed_sizes.empty:
    print("\nMost common unparsed size values:")
    print(unparsed_sizes.value_counts().head(20))
else:
    print("No unparsed non-missing size values found.")





print("\nHighest app prices:")
print(
    df_apps_clean.nlargest(10, "Price")[
        ["App", "Price", "Category"]
    ]
)

print("\nApps with the most reviews:")
print(
    df_apps_clean.nlargest(10, "Reviews")[
        ["App", "Reviews", "Installs"]
    ]
)

print("\nApps with the most installs:")
print(
    df_apps_clean.nlargest(10, "Installs")[
        ["App", "Installs", "Reviews"]
    ]
)

print("\nRating summary:")
print(df_apps_clean["Rating"].describe())

print("\nPrice summary:")
print(df_apps_clean["Price"].describe())



review_thresholds = [100, 1000, 5000]

for minimum_reviews in review_thresholds:
    top_rated_apps = (
        df_apps_clean[
            (df_apps_clean["Reviews"] >= minimum_reviews)
            & df_apps_clean["Rating"].notna()
        ]
        .sort_values(
            ["Rating", "Reviews"],
            ascending=[False, False]
        )
    )

    print(
        f"\n--- Top 10 Rated Apps with at Least "
        f"{minimum_reviews:,} Reviews ---"
    )

    print(
        "Number of qualifying apps:",
        len(top_rated_apps)
    )

    print(
        top_rated_apps[
            ["App", "Rating", "Reviews", "Installs"]
        ].head(10).to_string(index=False)
    )



print("\nTop 5 highest-rated apps, regardless of review count:")
print(
    df_apps_clean.sort_values(
        "Rating",
        ascending=False,
        na_position="last"
    ).head(5)
)

print("\nTop 5 largest apps:")
print(
    df_apps_clean.sort_values(
        "Size_MBs",
        ascending=False,
        na_position="last"
    ).head(5)
)

print("\nTop 50 apps by number of reviews:")
print(
    df_apps_clean.sort_values(
        "Reviews",
        ascending=False,
        na_position="last"
    ).head(50)
)



print("\n--- Final Dataset Validation ---")

print("Final shape:", df_apps_clean.shape)

print("\nMissing values per column:")
print(
    df_apps_clean.drop(
        columns="_Source_Excel_Row"
    ).isna().sum()
)

print("\nRemaining exact duplicate rows:")
print(
    df_apps_clean.drop(
        columns="_Source_Excel_Row"
    ).duplicated().sum()
)

print("\nFinal data types:")
print(
    df_apps_clean.drop(
        columns="_Source_Excel_Row"
    ).dtypes
)

print("\nFirst five rows:")
print(
    df_apps_clean.drop(
        columns="_Source_Excel_Row"
    ).head()
)



output_file = "google_play_store_cleaned.csv"

# Exclude internal tracking column from the analysis dataset.
df_apps_clean.drop(
    columns="_Source_Excel_Row"
).to_csv(
    output_file,
    index=False
)

print(f"\nCleaned dataset saved to: {output_file}")

audit_df = pd.DataFrame(
    audit_records,
    columns=[
        "Excel_Row",
        "App",
        "Removal_Reason",
        "Details"
    ]
)

audit_file = "google_play_store_removal_audit.csv"

audit_df.to_csv(audit_file, index=False)

print("Removal audit saved to:", audit_file)

print("\n--- Removal Counts by Reason ---")

if not audit_df.empty:
    print(audit_df["Removal_Reason"].value_counts())
else:
    print("No rows were removed in the audited steps.")




category_counts = df_apps_clean["Category"].value_counts()

fig = px.pie(
    names=category_counts.index,
    values=category_counts.values,
    title="Distribution of Apps by Category"
)

fig.show()




fig = px.pie(
    names=category_counts.index,
    values=category_counts.values,
    title="Distribution of Apps by Category"
)

fig.update_traces(hole=0.4)
fig.show()




top_categories = df_apps_clean["Category"].value_counts().head(10)

fig = px.bar(
    x=top_categories.index,
    y=top_categories.values,
    labels={
        "x": "Category",
        "y": "Number of Apps"
    },
    title="Top 10 Categories by Number of Apps"
)

fig.show()




top_15_categories = (
    df_apps_clean["Category"]
    .value_counts()
    .head(15)
    .sort_values(ascending=True)
    .rename_axis("Category")
    .reset_index(name="App Count")
)

fig = px.bar(
    top_15_categories,
    x="App Count",
    y="Category",
    orientation="h",
    text="App Count",
    title="Top 15 Categories by Number of Apps",
    labels={
        "App Count": "Number of Apps",
        "Category": "App Category"
    }
)

fig.update_traces(textposition="outside")
fig.update_layout(yaxis={"categoryorder": "total ascending"})
fig.show()




scatter_data = df_apps_clean.dropna(
    subset=["Reviews", "Installs", "Type"]
).copy()


scatter_data = scatter_data[
    (scatter_data["Reviews"] > 0)
    & (scatter_data["Installs"] > 0)
]

fig = px.scatter(
    scatter_data,
    x="Reviews",
    y="Installs",
    color="Type",
    hover_name="App",
    title="Reviews vs. Installs",
    log_x=True,
    log_y=True,
    labels={
        "Reviews": "Number of Reviews (log scale)",
        "Installs": "Number of Installs (log scale)"
    }
)

fig.show()



app_details = (
    df_apps_clean[["App", "Rating", "Reviews"]]
    .head(5)
    .set_index("App")
)

stacked_details = app_details.stack()

print("\n--- Stacked App Details ---")
print(stacked_details)




valid_type_data = df_apps_clean[
    df_apps_clean["Type"].isin(["Free", "Paid"])
].dropna(
    subset=["Category", "Type"]
)

type_counts = (
    valid_type_data
    .groupby(["Category", "Type"])
    .size()
    .reset_index(name="App Count")
)

fig = px.bar(
    type_counts,
    x="Category",
    y="App Count",
    color="Type",
    barmode="group",
    title="Free vs. Paid Apps by Category",
    labels={
        "Category": "App Category",
        "App Count": "Number of Apps",
        "Type": "App Type"
    }
)

fig.update_layout(xaxis_tickangle=-45)
fig.show()



box_data = valid_type_data.dropna(
    subset=["Rating"]
)

fig = px.box(
    box_data,
    x="Type",
    y="Rating",
    color="Type",
    title="Rating Distribution: Free vs. Paid Apps",
    labels={
        "Type": "App Type",
        "Rating": "App Rating"
    }
)

fig.show()




print("\nCleaning and EDA completed.")

