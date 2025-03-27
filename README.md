# Course_network_analysis

## 1. Main Analysis
## 2. Nework Robustness check

`network_evaluation.py`: the python file constructs a course similarity network using a binarized course-skill matrix. Computes:

- Course-level metrics:
  - **Coverage** (number of relevant skills)
  - **Degree** (number of connections to other courses)
  - **Course Influence** (coverage / degree)

- Network-level metrics:
  - **Link Density**
  - **Giant Component Ratio**

**Outputs:**
- `course_data_{threshold}.csv`: Course-level metrics per threshold  
- `link_density_and_giant_component_ratio.csv`: Network metrics per threshold


`sensitivity_analysis.py': the python file performs a sensitivity analysis by comparing course influence rankings and network structure across different thresholds, using `0.60` as the baseline

**Outputs:**

- `S_fig_5_a.png`: Relative change in network structure  
- `S_fig_5_b.png`: Spearman correlation of course influence rankings  
- `S_fig_5_c.png`: Absolute change in ranking & structure



