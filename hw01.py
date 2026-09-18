#%% ------------------------------------------
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

#%% ------------------------------------------
#  Define the edges and build the graph
# --------------------------------------------

edges = [
("B", "A"),
("C", "A"), ("C", "B"),
("D", "A"), ("D", "C"),
("E", "A"), ("E", "D"),
("F", "H"),
("G", "F"),
("H", "A"), ("H", "B"), ("H", "I"),
("I", "J"),
("J", "G"), ("J", "I"),
("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "H"), ("A", "J"),
]

G = nx.DiGraph()
G.add_edges_from(edges)

#%% ------------------------------------------
# Plot the graph
# --------------------------------------------
pos = nx.spring_layout(G, seed=42, k=0.9)

fig, ax = plt.subplots(figsize=(9, 9))

highlight_node = "F"
node_colors = ["#FF6B6B" if n == highlight_node else "#87CEEB" for n in G.nodes()]
node_linewidths = [3.0 if n == highlight_node else 1.5 for n in G.nodes()]

nx.draw_networkx_nodes(
    G, pos, ax=ax,
    node_size=1200,
    node_color=node_colors,
    edgecolors="black",
    linewidths=1.5,
)

nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight="bold")

edge_set = set(edges)
for u, v in edges:
    reciprocal = (v, u) in edge_set
    rad = 0.15 if reciprocal else 0.0
    ax.annotate(
        "",
        xy=pos[v], xycoords="data",
        xytext=pos[u], textcoords="data",
        arrowprops=dict(
            arrowstyle="-|>",
            color="gray",
            shrinkA=18, shrinkB=18,
            patchA=None, patchB=None,
            connectionstyle=f"arc3,rad={rad}",
            mutation_scale=18,
            linewidth=1.5,
        ),
    )

ax.set_title("Directed Graph", fontsize=14, fontweight="bold")
ax.axis("off")
plt.tight_layout()
plt.show()

#%% ------------------------------------------
# PAGE RANK
# --------------------------------------------
pr = nx.pagerank(G, alpha=0.85)

print("Pagerank:", pr)
print()
print("Pagerank F:", pr["F"])

# #%% ------------------------------------------
# # PAGE RANK ADDING AN INGOING EDGE TO F
# # --------------------------------------------

# edges_max_I = [
# ("B", "A"),
# ("C", "A"), ("C", "B"),
# ("D", "A"), ("D", "C"),
# ("E", "A"), ("E", "D"),
# ("F", "H"),
# ("G", "F"),
# ("H", "A"), ("H", "B"), ("H", "I"),
# ("I", "J"), ("I","F"),
# ("J", "G"), ("J", "I"),
# ("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "H"), ("A", "J"),
# ]

# G_max_I = nx.DiGraph()
# G_max_I.add_edges_from(edges_max_I)

# edges_max_B = [
# ("B", "A"), ("B","F"),
# ("C", "A"), ("C", "B"),
# ("D", "A"), ("D", "C"),
# ("E", "A"), ("E", "D"),
# ("F", "H"),
# ("G", "F"),
# ("H", "A"), ("H", "B"), ("H", "I"),
# ("I", "J"),
# ("J", "G"), ("J", "I"),
# ("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "H"), ("A", "J"),
# ]

# G_max_B = nx.DiGraph()
# G_max_B.add_edges_from(edges_max_B)

# pr_max_I = nx.pagerank(G_max_I, alpha=0.85)
# pr_max_B = nx.pagerank(G_max_B, alpha=0.85)


# print("Pagerank F adding (I,F):", pr_max_I["F"])
# print()
# print("Pagerank F adding (B,F):", pr_max_B["F"])

#%% ------------------------------------------
# PR(F), IN-COMING EDGES
# --------------------------------------------

# G = nx.DiGraph()
# G.add_edges_from(edges)
baseline = nx.pagerank(G, alpha=0.85)

results = []
for u in G.nodes():
    if u == "F":
        continue
    if G.has_edge(u, "F"):
        continue  # already an edge
    Gt = G.copy()
    Gt.add_edge(u, "F")
    pr = nx.pagerank(Gt, alpha=0.85)
    results.append((u, pr["F"], G.out_degree(u), baseline["F"]))

results.sort(key=lambda x: -x[1])
print(f"{'source':>6} | {'PR(F) before':>12} | {'new PR(F)':>10} | {'gain':>8}")
for u, prf, outdeg, pru in results:
    print(f"{u:>6} | {pru:>12.4f} | {prf:>10.6f} | {prf-baseline['F']:>+8.6f}")

#%% ------------------------------------------
# PR(F), OUT-GOING EDGES
# --------------------------------------------

# G = nx.DiGraph()
# G.add_edges_from(edges)
# baseline = nx.pagerank(G, alpha=0.85)

results = []
for u in G.nodes():
    if u == "F":
        continue
    if G.has_edge("F", u):
        continue  # already an edge
    Gt = G.copy()
    Gt.add_edge("F", u)
    pr = nx.pagerank(Gt, alpha=0.85)
    results.append((u, pr["F"], G.out_degree(u), baseline["F"]))

results.sort(key=lambda x: -x[1])
print(f"{'target':>6} | {'PR(F) before':>12} | {'new PR(F)':>10} | {'gain':>8}")
for u, prf, outdeg, pru in results:
    print(f"{u:>6} | {pru:>12.4f} | {prf:>10.6f} | {prf-baseline['F']:>+8.6f}")

# %%
