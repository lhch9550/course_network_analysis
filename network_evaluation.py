import numpy as np
import pandas as pd
import networkx as nx

def compute_course_influence_with_density_and_giant_component_ratio(threshold, course_skill_matrix_df, df_course):
    """
    Binarize the course-skill matrix using the given threshold,
    construct a course network, and compute coverage, degree, and course influence for each course.
    Also returns the link density and giant component ratio of the network.
    """
    # Convert course-skill matrix to a numpy array
    course_skill_matrix = course_skill_matrix_df.values

    # Apply threshold filtering: set values below the threshold to 0, and others to 1
    filtered_matrix = np.where(course_skill_matrix < threshold, 0, course_skill_matrix)
    filtered_matrix[filtered_matrix != 0] = 1

    # Calculate coverage per course (sum of each row)
    row_sums = np.sum(filtered_matrix, axis=1)

    # Compute similarity between courses: dot product of filtered matrix and its transpose (set diagonal to 0)
    monopartite_matrix = np.dot(filtered_matrix, filtered_matrix.T)
    np.fill_diagonal(monopartite_matrix, 0)

    # Construct course network using NetworkX (nodes: courses, edges: shared skills)
    G = nx.Graph()
    n = monopartite_matrix.shape[0]
    for i in range(n):
        for j in range(i+1, n):
            weight = float(monopartite_matrix[i, j])
            if weight > 0:
                G.add_edge(i, j, weight=weight)

    # Course names are the index of course_skill_matrix_df
    course_names = course_skill_matrix_df.index.tolist()
    # Add isolated nodes (nodes with no edges)
    for i, name in enumerate(course_names):
        if i not in G.nodes():
            G.add_node(i)
        G.nodes[i]['name'] = name
        G.nodes[i]['course_coverage'] = row_sums[i]

    # Calculate course_influence = coverage / degree (NaN if degree is 0)
    course_data = []
    for node in G.nodes():
        name = G.nodes[node]['name']
        coverage = G.nodes[node]['course_coverage']
        degree = G.degree(node)
        course_influence = coverage / degree if degree > 0 else np.nan
        # Retrieve course_label from df_course (default to 'Unknown' if not found)
        label_series = df_course.loc[df_course['id'] == name, 'course_label']
        label_value = label_series.iloc[0] if not label_series.empty else 'Unknown'
        course_data.append({
            'id': name,
            'course_label': label_value,
            'coverage': coverage,
            'degree': degree,
            'course_influence': course_influence
        })

    course_influence_df = pd.DataFrame(course_data)
    
    # Calculate network link density
    density = nx.density(G)

    # Calculate Giant Component Ratio = size of largest connected component / total number of nodes
    if len(G) > 0:
        largest_cc = max(nx.connected_components(G), key=len)
        giant_component_ratio = len(largest_cc) / len(G)
    else:
        giant_component_ratio = 0

    return course_influence_df, density, giant_component_ratio

def main():
    # Load data
    df_course = pd.read_csv('df_course.csv')
    course_skill_matrix_df = pd.read_csv('/home/lhch9550/new_course_skill_matrix.csv')
    course_skill_matrix_df.set_index('id', inplace=True)

    # Generate thresholds from 0.5 to 0.7 in increments of 0.02
    thresholds = np.arange(0.5, 0.7 + 0.02, 0.02)
    results = []

    for th in thresholds:
        print(f"Processing threshold {th:.2f} ...")
        ci_df, density, giant_component_ratio = compute_course_influence_with_density_and_giant_component_ratio(th, course_skill_matrix_df, df_course)
        results.append({"Threshold": round(th,2), "Link Density": density, "Giant Component Ratio": giant_component_ratio})
        print(f"Threshold {th:.2f}: Link Density = {density}, Giant Component Ratio = {giant_component_ratio}")
        
        # Save course_influence_df as CSV for each threshold (filename: course_data_{threshold}.csv)
        ci_df.to_csv(f"course_data_{th:.2f}.csv", index=False)
        print(f"Saved course_data_{th:.2f}.csv")

    # Organize results into a DataFrame
    results_df = pd.DataFrame(results)
    
    # Save results to file
    results_df.to_csv('link_density_and_giant_component_ratio.csv', index=False)
    
    print("\nLink Density and Giant Component Ratio per Threshold:")
    print(results_df)

if __name__ == '__main__':
    main()