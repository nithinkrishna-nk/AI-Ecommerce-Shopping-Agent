import chromadb

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(name="products")


def search_products(query: str):
    results = collection.query(
        query_texts=[query],
        n_results=5
    )

    products = []

    for metadata in results["metadatas"][0]:
      products.append({
        "product_id": metadata["product_id"],
        "product_name": metadata["product_name"],
        "price": metadata["discounted_price"],
        "rating": metadata["rating"],
        "category": metadata["category"]
        })

    return products


# check product details tool

def check_product_details(product_id: str):
    result = collection.get(
        ids=[product_id],
        include=["metadatas", "documents"]
    )

    if not result["metadatas"]:
        return {"error": "Product not found"}

    metadata = result["metadatas"][0]

    return {
        "product_id": product_id,
        "product_name": metadata["product_name"],
        "price": metadata["discounted_price"],
        "actual_price": metadata["actual_price"],
        "discount": metadata["discount_percentage"],
        "rating": metadata["rating"],
        "rating_count": metadata["rating_count"],
        "category": metadata["category"],
        "product_link": metadata["product_link"]
    }