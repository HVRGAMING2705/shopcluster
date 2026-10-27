# ShopCluster — Customer Segmentation with K-Means

K-Means clustering (scikit-learn, k=4, seed 42) on 300 synthetic shoppers:
age, annual income, spending score.

- Silhouette score: 0.530, inertia: 155.9
- Segments: Affluent Regulars (76), Budget Families (76), Young Spenders (76), Careful Seniors (72)
- `train.py` trains the model and exports `model.json`
- `index.html` is a single-page demo: the same centroids run in JavaScript,
  so the browser demo reproduces the Python assignment exactly — no backend needed.

Live demo: https://shopcluster.vercel.app

By Vikranth Reddy — B.Tech CSE (AI & ML), Woxsen University.
