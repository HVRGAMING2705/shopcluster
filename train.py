import json, numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

rng = np.random.default_rng(42)
# 4 archetypes: (age, annual income $k, spending score 1-100)
archetypes = np.array([
    [25, 45, 80],   # Young Spenders
    [45, 90, 70],   # Affluent Regulars
    [40, 30, 30],   # Budget Families
    [60, 55, 25],   # Careful Seniors
])
names_arche = ["Young Spenders", "Affluent Regulars", "Budget Families", "Careful Seniors"]
sds_arche = np.array([[5, 10, 10], [7, 12, 10], [8, 8, 10], [7, 12, 10]])
rows = []
for i, (c, s) in enumerate(zip(archetypes, sds_arche)):
    rows.append(rng.normal(c, s, size=(75, 3)))
X = np.vstack(rows)
X[:, 0] = np.clip(X[:, 0], 18, 75)
X[:, 1] = np.clip(X[:, 1], 15, 130)
X[:, 2] = np.clip(X[:, 2], 1, 100)
names = ["age", "annual_income_k", "spending_score"]
mu, sd = X.mean(0), X.std(0)
Xs = (X - mu) / sd
model = KMeans(n_clusters=4, n_init=10, random_state=42).fit(Xs)
labels = model.labels_
sil = float(silhouette_score(Xs, labels))
sizes = [int((labels == k).sum()) for k in range(4)]
centers_orig = (model.cluster_centers_ * sd + mu)
# Map each fitted cluster to nearest archetype (in standardized space)
arch_s = (archetypes - mu) / sd
mapping = {}
used = set()
for k in range(4):
    d = [float(np.linalg.norm(model.cluster_centers_[k] - arch_s[j])) for j in range(4)]
    order = np.argsort(d)
    for j in order:
        if int(j) not in used:
            mapping[k] = int(j); used.add(int(j)); break
print(f"silhouette={sil:.3f} inertia={model.inertia_:.1f} sizes={sizes}")
for k in range(4):
    print(k, "->", names_arche[mapping[k]], np.round(centers_orig[k], 1))
mj = {"features": names, "means": mu.tolist(), "stds": sd.tolist(),
      "centroids_std": model.cluster_centers_.tolist(),
      "centroids_orig": centers_orig.tolist(),
      "cluster_names": [names_arche[mapping[k]] for k in range(4)],
      "cluster_sizes": sizes,
      "metrics": {"silhouette": sil, "inertia": float(model.inertia_), "n": int(len(X))}}
with open("model.json", "w") as f:
    json.dump(mj, f, indent=1)

def predict(v):
    z = (np.array(v, dtype=float) - mu) / sd
    d = [float(np.linalg.norm(z - c)) for c in model.cluster_centers_]
    return int(np.argmin(d)), d
samples = [[24, 45, 82], [48, 92, 68], [38, 28, 32], [62, 55, 22], [30, 60, 50]]
for s in samples:
    k, d = predict(s)
    print(s, "->", names_arche[mapping[k]], [round(x, 3) for x in d])
