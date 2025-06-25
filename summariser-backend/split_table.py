from sentence_transformers import SentenceTransformer
from sklearn.cluster import DBSCAN
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import AgglomerativeClustering

# Sample vertically stacked table
table_rows = [
    ["Department", "Q1 Revenue", "Q2 Revenue"],
    ["Sales", "$1.2M", "$1.5M"],
    ["Marketing", "$900K", "$1.1M"],
    ["HR", "$500K", "$600K"],
    ["Product", "$1.4M", "$1.6M"],

    ["Product", "Units Sold", "Return Rate"],
    ["Widget A", "12,000", "2.5%"],
    ["Widget B", "8,000", "1.9%"],
    ["Widget C", "5,000", "3.0%"]
]

table_rows1 =  [
    ["Region", "Q1 Sales", "Q2 Sales"],
    ["North", "$1.2M", "$1.5M"],
    ["South", "$900K", "$1.1M"],
    ["East", "$1.1M", "$1.4M"],
    ["West", "$950K", "$1.0M"],

    ["Item", "Stock Count", "Reorder Level"],
    ["Widget A", "120", "30"],
    ["Widget B", "95", "20"],
    ["Widget C", "150", "35"],

    ["Project", "Deadline", "Owner"],
    ["Alpha", "2024-09-30", "Liam"],
    ["Beta", "2024-10-15", "Olivia"],
    ["Gamma", "2024-12-01", "Ethan"],

    ["Item", "Q1 Sales", "Q2 Sales"],  # ⚠️ Duplicate header-like row
    ["Widget A", "$500K", "$550K"],
    ["Widget B", "$600K", "$610K"]
]
def cluster_table(table_rows):
    # Step 1: Convert each row to a single string using "|" as delimiter
    flattened_rows = [" | ".join(row) for row in table_rows]

    # Step 2: Generate semantic embeddings using a pre-trained SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    semantic_embeddings = model.encode(flattened_rows)

    # Step 3: Create row indices and compute structural distances (row position differences)
    row_indices = np.arange(len(flattened_rows)).reshape(-1, 1)
    structural_distance = euclidean_distances(row_indices)
    norm_dist = structural_distance / structural_distance.max()  # normalize to [0,1]

    # Step 4: Compute cosine similarity matrix between semantic embeddings
    semantic_sim = cosine_similarity(semantic_embeddings)
    semantic_avg_sim = (semantic_sim.sum() - len(semantic_sim)) / (len(semantic_sim)**2 - len(semantic_sim))
    print("semantic_avg_sim: ", semantic_avg_sim)

    # Step 5: Convert structural distance to similarity using exponential decay
    decay_factor = 1
    structural_sim = np.exp(-decay_factor * norm_dist)

    # Step 6: Combine semantic similarity and structural similarity using weighted average
    alpha = 0.7  # importance of semantic similarity
    combined_sim = alpha * semantic_sim + (1 - alpha) * structural_sim

    # Step 7: Perform agglomerative clustering on (1 - similarity) matrix (i.e., distance)
    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=0.4,
        metric='precomputed',
        linkage='average'
    )
    labels = clustering.fit_predict(1 - combined_sim)
    
    # Step 8: Output clustered rows
    df = pd.DataFrame({
        "Row Text": flattened_rows,
        "Cluster": labels
    })
    print(df)
    
    return labels
    """
    

    # Step 9: Visualize combined similarity matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(combined_sim, annot=True, fmt=".2f", cmap="YlGnBu", xticklabels=False, yticklabels=False)
    plt.title("Combined Similarity Between Table Rows")
    plt.xlabel("Row Index")
    plt.ylabel("Row Index")
    plt.tight_layout()
    plt.show()
    """
    
def detect_table_boundaries_by_cluster_change(table_rows):
    labels = cluster_table(table_rows)
    boundaries = []
    last_cluster = labels[0]
    change_count = 0

    for i in range(1, len(labels)):
        if labels[i] != last_cluster:
            change_count += 1
            last_cluster = labels[i]

            if change_count == 2:
                boundaries.append(i)  # start of new table
                change_count = 0  # reset
    return boundaries
