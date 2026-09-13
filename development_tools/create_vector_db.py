import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer

# ============================================================
# 1. LOAD CLEAN DATASET
# ============================================================

df = pd.read_csv("data/products_prepared.csv")

print("\nUnique product IDs:", df["product_id"].nunique())
print("Total rows:", len(df))
print("Duplicate product IDs:", df["product_id"].duplicated().sum())

print("Products loaded:", len(df))


# ============================================================
# 2. LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# ============================================================
# 3. CREATE CHROMADB CLIENT
# ============================================================

print("\nCreating ChromaDB...")

client = chromadb.PersistentClient(
    path="chroma_db"
)

print("ChromaDB client created.")



# ============================================================
# 4. CREATE PRODUCTS COLLECTION
# ============================================================

print("\nCreating products collection...")

collection = client.get_or_create_collection(
    name="products"
)

print("Products collection created.")



# ============================================================
# 5. CREATE PRODUCT DOCUMENTS AND METADATA
# ============================================================

print("\nCreating product documents...")

documents = []
metadatas = []
ids = []


for _, row in df.iterrows():

    # --------------------------------------------------------
    # Create searchable text
    # --------------------------------------------------------

    product_text = f"""
Product Name: {row['product_name']}

Category: {row['category']}

Description: {row['about_product']}

Review Title: {row['review_title']}

Review: {row['review_content']}
"""

    documents.append(product_text)


    # --------------------------------------------------------
    # Create structured metadata
    # --------------------------------------------------------

    metadata = {
        "product_id": str(row["product_id"]),
        "product_name": str(row["product_name"]),
        "category": str(row["category"]),
        "discounted_price": float(row["discounted_price"]),
        "actual_price": float(row["actual_price"]),
        "discount_percentage": float(row["discount_percentage"]),
        "rating": float(row["rating"]),
        "rating_count": float(row["rating_count"]),
        "product_link": str(row["product_link"])
    }

    metadatas.append(metadata)


    # --------------------------------------------------------
    # Create unique ID
    # --------------------------------------------------------

    ids.append(str(row["product_id"]))


print("Product documents created:", len(documents))
print("Metadata records created:", len(metadatas))
print("Product IDs created:", len(ids))




# ============================================================
# 6. GENERATE EMBEDDINGS
# ============================================================

print("\nGenerating embeddings...")

embeddings = model.encode(
    documents,
    show_progress_bar=True
)

print("Embeddings generated.")
print("Number of embeddings:", len(embeddings))



# ============================================================
# 7. STORE PRODUCTS IN CHROMADB
# ============================================================

print("\nStoring products in ChromaDB...")

collection.upsert(
    ids=ids,
    documents=documents,
    embeddings=embeddings.tolist(),
    metadatas=metadatas
)

print("Products stored successfully.")
print("Total products in ChromaDB:", collection.count())