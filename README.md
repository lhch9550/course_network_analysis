# Course_network_analysis

# 🧠 Course Network Analysis & Sensitivity Evaluation

This project performs **course network construction** based on a course-skill relationship matrix, and evaluates the **robustness and sensitivity** of the network under varying similarity thresholds.

---

## 📁 Files

### `network_evaluation.py`

Constructs a course similarity network using a binarized course-skill matrix. Computes:

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

---

### `sensitivity_analysis.py`

Performs a sensitivity analysis by comparing course influence rankings and network structure across different thresholds, using `0.60` as the baseline.

**Generates 3 figures:**

- `S_fig_5_a.png`: Relative change in network structure  
- `S_fig_5_b.png`: Spearman correlation of course influence rankings  
- `S_fig_5_c.png`: Absolute change in ranking & structure

---

## 🔧 How to Run

1. **Run the network evaluation:**

   ```bash
   python network_evaluation.py
