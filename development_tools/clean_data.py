import pandas as pd


# ============================================================
# 1. LOAD DATASET
# ============================================================

df = pd.read_csv("data/amazon.csv")

print("Original shape:", df.shape)


# ============================================================
# 2. CLEAN PRICE COLUMNS
# ============================================================

def clean_price(value):
    value = str(value)

    # Remove currency symbol and commas
    value = value.replace("₹", "")
    value = value.replace(",", "")
    value = value.strip()

    return float(value)


df["discounted_price"] = df["discounted_price"].apply(clean_price)
df["actual_price"] = df["actual_price"].apply(clean_price)


# ============================================================
# 3. CLEAN DISCOUNT PERCENTAGE
# ============================================================

df["discount_percentage"] = (
    df["discount_percentage"]
    .astype(str)
    .str.replace("%", "", regex=False)
    .str.strip()
    .astype(float)
)


# ============================================================
# 4. CLEAN RATING
# ============================================================

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

df["rating"] = df["rating"].fillna(df["rating"].median())


# ============================================================
# 5. CLEAN RATING COUNT
# ============================================================

df["rating_count"] = (
    df["rating_count"]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["rating_count"] = pd.to_numeric(
    df["rating_count"],
    errors="coerce"
)

# Missing rating counts become 0
df["rating_count"] = df["rating_count"].fillna(0)


# ============================================================
# 6. HANDLE TEXT COLUMNS
# ============================================================

text_columns = [
    "product_name",
    "category",
    "about_product",
    "review_title",
    "review_content"
]

for column in text_columns:
    df[column] = (
        df[column]
        .fillna("")
        .astype(str)
        .str.strip()
    )


# ============================================================
# 7. REMOVE UNNECESSARY USER DATA
# ============================================================

columns_to_remove = [
    "user_id",
    "user_name",
    "review_id"
]

df = df.drop(columns=columns_to_remove)


# ============================================================
# 8. CHECK DATA
# ============================================================

print("\n========== CLEANED DATA ==========")

print("\nShape:")
print(df.shape)

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())


# ============================================================
# 9. SAVE CLEAN DATASET
# ============================================================

df.to_csv(
    "data/products_clean.csv",
    index=False
)

print("\nClean dataset saved successfully!")
print("File: data/products_clean.csv")