# PancSynergy AI: Machine Learning Models, Algorithms & Training Guide

---

## Executive Overview

This document provides a comprehensive, rigorous technical reference on the **machine learning algorithms, architectures, training protocols, cross-validation procedures, and benchmark evaluations** employed across the **PancSynergy AI** platform.

PancSynergy AI deploys three distinct computational model families:
1. **The PANC-1 Drug Synergy Regression Suite:** Benchmarking 8 candidate model architectures across regularized linear models, tree ensembles, and deep multi-layer perceptrons, with the champion **Random Forest Regressor** predicting continuous combination Gamma ($\Gamma$) scores.
2. **The USPTO-50K Chemical Reaction & Kinetics Classifier:** A multi-class **Histogram Gradient Boosting Classifier** predicting synthetic reaction transformation pathways, kinetic durations, optimal temperatures, solvents, and yields for any pair of candidate molecules.
3. **The Pharmacodynamic (PK/PD) Hill/Exponential Kill Engine:** A continuous kinetic simulation model mapping molecular potencies ($\text{Log } AC_{50}$) and synergy multipliers into time-dependent cancer cell eradication trajectories ($V(t)$) and half-maximal kill milestones ($T_{50}$) over 0 to 96 hours.

---

## Table of Contents

- [1. PANC-1 Drug Synergy Regression Suite](#1-panc-1-drug-synergy-regression-suite)
  - [1.1 Problem Formulation & Target Variable](#11-problem-formulation--target-variable)
  - [1.2 Candidate Model Architectures & Hyperparameters](#12-candidate-model-architectures--hyperparameters)
    - [A. Regularized Linear Baselines (Ridge, Lasso, ElasticNet)](#a-regularized-linear-baselines-ridge-lasso-elasticnet)
    - [B. Tree Ensemble Models (Random Forest, Extra Trees, Gradient Boosting, HistGradientBoosting)](#b-tree-ensemble-models-random-forest-extra-trees-gradient-boosting-histgradientboosting)
    - [C. Deep Learning Multi-Layer Perceptron (MLP)](#c-deep-learning-multi-layer-perceptron-mlp)
  - [1.3 Feature Preprocessing Pipeline](#13-feature-preprocessing-pipeline)
  - [1.4 The 5-Fold Cross-Validation & Training Protocol](#14-the-5-fold-cross-validation--training-protocol)
  - [1.5 Complete Model Benchmark Leaderboard](#15-complete-model-benchmark-leaderboard)
  - [1.6 Champion Selection, Full Retraining & Serialization](#16-champion-selection-full-retraining--serialization)
- [2. USPTO-50K Chemical Reaction & Kinetics Classifier](#2-uspto-50k-chemical-reaction--kinetics-classifier)
  - [2.1 Problem Formulation & Reaction Classes](#21-problem-formulation--reaction-classes)
  - [2.2 Dataset Subsampling & Stratified Splitting](#22-dataset-subsampling--stratified-splitting)
  - [2.3 High-Dimensional Reaction Featurization (1,571 Dims)](#23-high-dimensional-reaction-featurization-1571-dims)
  - [2.4 Training HistGradientBoostingClassifier](#24-training-histgradientboostingclassifier)
  - [2.5 Kinetics & Condition Mapping](#25-kinetics--condition-mapping)
- [3. Continuous Pharmacodynamic (PK/PD) Kinetic Model](#3-continuous-pharmacodynamic-pkpd-kinetic-model)
  - [3.1 Monotherapy Potency Scaling Equations](#31-monotherapy-potency-scaling-equations)
  - [3.2 Non-Linear Synergy Rate Scaling](#32-non-linear-synergy-rate-scaling)
  - [3.3 Analytical Derivation of Half-Maximal Eradication ($T_{50}$)](#33-analytical-derivation-of-half-maximal-eradication-t_50)
- [4. How to Reproduce and Retrain the Models](#4-how-to-reproduce-and-retrain-the-models)
  - [4.1 Retraining the Synergy Regression Model](#41-retraining-the-synergy-regression-model)
  - [4.2 Retraining the USPTO-50K Chemical Reaction Model](#42-retraining-the-uspto-50k-chemical-reaction-model)
  - [4.3 Automated End-to-End Execution (`run_all.py`)](#43-automated-end-to-end-execution-run_allpy)

---

## 1. PANC-1 Drug Synergy Regression Suite

### 1.1 Problem Formulation & Target Variable

The goal is to learn a continuous mapping function:

$$f: \mathcal{X}_{\text{pair}} \to \mathbb{R}^+, \quad \hat{y} = f(\mathbf{x}_{\text{pair}})$$

where $\mathbf{x}_{\text{pair}} \in \mathbb{R}^{802}$ is the symmetric, order-invariant feature vector capturing the molecular fingerprints, 2D physicochemical descriptors, and single-agent potencies of Drug $A$ and Drug $B$.

- **Target Variable ($y = \text{Gamma}$):** A continuous scalar reflecting the deviation of the combination response surface from Bliss independence.
  - $\mathbf{\Gamma < 0.5}$ $\rightarrow$ High Synergy (Rapid, exponential cancer cell lysis)
  - $\mathbf{0.5 \le \Gamma < 1.0}$ $\rightarrow$ Moderate Synergy
  - $\mathbf{1.0 \le \Gamma < 1.5}$ $\rightarrow$ Additive / Independent action
  - $\mathbf{\Gamma \ge 1.5}$ $\rightarrow$ Antagonistic interaction

---

### 1.2 Candidate Model Architectures & Hyperparameters

To identify the most reliable predictor, 8 candidate machine learning architectures across three paradigm families were benchmarked in [`models/trainer.py`](file:///c:/Users/Srinivas/Desktop/eterpunership/ran_hack/pancsynergy_ai/models/trainer.py):

#### A. Regularized Linear Baselines ([`models/regressor_baselines.py`](file:///c:/Users/Srinivas/Desktop/eterpunership/ran_hack/pancsynergy_ai/models/regressor_baselines.py))

1. **Ridge Regression ($L_2$ Regularization):**
   Minimizes the penalized residual sum of squares:
   $$\min_{\mathbf{w}} \frac{1}{2n} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \frac{\alpha}{2} \|\mathbf{w}\|_2^2$$
   - *Hyperparameters:* $\alpha = 10.0$, `random_state = 42`.
   - *Characteristics:* Shrinks collinear molecular feature weights toward zero without setting them to absolute zero.

2. **Lasso Regression ($L_1$ Regularization):**
   Minimizes least squares with an $L_1$ sparsity penalty:
   $$\min_{\mathbf{w}} \frac{1}{2n} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \alpha \|\mathbf{w}\|_1$$
   - *Hyperparameters:* $\alpha = 0.01$, `max_iter = 2000`, `random_state = 42`.
   - *Characteristics:* Enforces automatic feature selection by zeroing uninformative Morgan fingerprint bits.

3. **ElasticNet Regression ($L_1 + L_2$ Regularization):**
   Combines penalties to balance feature sparsity with grouping effects among correlated descriptors:
   $$\min_{\mathbf{w}} \frac{1}{2n} \|\mathbf{y} - \mathbf{X}\mathbf{w}\|_2^2 + \alpha \cdot \rho \|\mathbf{w}\|_1 + \frac{\alpha(1 - \rho)}{2} \|\mathbf{w}\|_2^2$$
   - *Hyperparameters:* $\alpha = 0.01$, $\rho = \text{l1\_ratio} = 0.5$, `max_iter = 2000`, `random_state = 42`.

---

#### B. Tree Ensemble Models ([`models/ensemble_models.py`](file:///c:/Users/Srinivas/Desktop/eterpunership/ran_hack/pancsynergy_ai/models/ensemble_models.py))

4. **Random Forest Regressor (Champion Architecture):**
   An ensemble of $B$ bagged decision trees trained on bootstrap resamples with randomized split features:
   $$\hat{y}(\mathbf{x}) = \frac{1}{B} \sum_{b=1}^{B} T_b(\mathbf{x})$$
   - *Hyperparameters:*
     - `n_estimators = 150`: Number of bagged regression trees.
     - `max_depth = 14`: Prevents individual trees from memorizing training outliers.
     - `min_samples_split = 4`: Minimum sample count required to split an internal node.
     - `min_samples_leaf = 2`: Minimum sample count required at a leaf node (smooths predictions).
     - `max_features = 'sqrt'` ($\approx 28$ features per split): Ensures tree de-correlation.
     - `random_state = 42`, `n_jobs = -1`.
   - *Theoretical Strengths:* Excels at capturing non-linear feature interactions (e.g., specific kinase heterocycle bits interacting synergistically with proteasome peptide warheads) without overfitting.

5. **Extra Trees Regressor (Extremely Randomized Trees):**
   Differs from Random Forest by drawing random cut points for each candidate feature rather than finding optimal thresholds:
   - *Hyperparameters:* `n_estimators = 150`, `max_depth = 16`, `min_samples_split = 3`, `random_state = 42`.
   - *Characteristics:* Reduces variance further at the cost of slightly higher bias.

6. **Gradient Boosting Regressor (GBRT):**
   Sequential additive boosting building trees to fit negative gradients (pseudo-residuals):
   $$F_m(\mathbf{x}) = F_{m-1}(\mathbf{x}) + \eta \sum_{j=1}^{J_m} \gamma_{jm} \mathbf{1}(\mathbf{x} \in R_{jm})$$
   - *Hyperparameters:* `n_estimators = 120`, `learning_rate = 0.08`, `max_depth = 5`, `subsample = 0.85` (stochastic gradient boosting), `random_state = 42`.

7. **Histogram Gradient Boosting (HistGradientBoosting):**
   Discretizes continuous molecular features into 256 integer bins, accelerating split evaluations:
   - *Hyperparameters:* `max_iter = 120`, `learning_rate = 0.08`, `max_leaf_nodes = 31`, `random_state = 42`.

---

#### C. Deep Learning Multi-Layer Perceptron (MLP) ([`models/deep_learning.py`](file:///c:/Users/Srinivas/Desktop/eterpunership/ran_hack/pancsynergy_ai/models/deep_learning.py))

8. **Deep MLP Regressor:**
   A feed-forward artificial neural network with 3 hidden layers:
   $$\mathbf{h}_1 = \text{ReLU}(\mathbf{W}_1 \mathbf{x} + \mathbf{b}_1), \quad \mathbf{h}_2 = \text{ReLU}(\mathbf{W}_2 \mathbf{h}_1 + \mathbf{b}_2), \quad \mathbf{h}_3 = \text{ReLU}(\mathbf{W}_3 \mathbf{h}_2 + \mathbf{b}_3), \quad \hat{y} = \mathbf{w}_{\text{out}}^T \mathbf{h}_3 + b_{\text{out}}$$
   - *Architecture:* $\text{Input}(802) \to \text{Dense}(256) \to \text{Dense}(128) \to \text{Dense}(64) \to \text{Dense}(1)$.
   - *Activation:* Rectified Linear Unit ($\text{ReLU}(z) = \max(0, z)$).
   - *Optimizer:* Adam ($\beta_1 = 0.9, \beta_2 = 0.999, \epsilon = 10^{-8}$).
   - *Learning Rate:* Adaptive starting at $\eta_0 = 0.001$.
   - *Regularization:* Weight decay $\alpha = 0.001$, early stopping with patience of 25 epochs on a 15% validation split (`validation_fraction = 0.15`).
   - *Mini-batch Size:* 32 samples.

---

### 1.3 Feature Preprocessing Pipeline

Every candidate model is integrated into a scikit-learn `Pipeline` alongside `StandardScaler()`:

$$\tilde{x}_{ij} = \frac{x_{ij} - \mu_j}{\sigma_j}$$

- Centers all molecular descriptors (e.g., MolWt $\sim 450$, TPSA $\sim 110$) and binary fingerprint bits to zero mean and unit variance.
- Ensures gradient-based solvers (Ridge, Lasso, ElasticNet, MLP) converge stably and tree algorithms evaluate standardized splits.

---

### 1.4 The 5-Fold Cross-Validation & Training Protocol

Located in [`models/trainer.py`](file:///c:/Users/Srinivas/Desktop/eterpunership/ran_hack/pancsynergy_ai/models/trainer.py#L27-L140):

```mermaid
flowchart TD
    Dataset["Clean NCATS Matrix (498 combination pairs)"] --> Split["Stratified Train/Holdout Split<br/>train_test_split(test_size=0.20, random_state=42)"]
    
    Split --> TrainSet["80% Training Split (N ≈ 398)"]
    Split --> TestSet["20% Held-Out Test Set (N ≈ 100)"]
    
    TrainSet --> KFold["5-Fold Cross-Validation Loop<br/>KFold(n_splits=5, shuffle=True, random_state=42)"]
    
    subgraph CV_Loop["Per-Fold Validation (Repeated 5 Times)"]
        KFold --> FoldTrain["4/5 Folds (Fit Model)"]
        KFold --> FoldVal["1/5 Fold (Evaluate Metrics)"]
        FoldTrain --> Fit["Clone & Fit Candidate"]
        Fit --> Predict["Predict on Validation Fold"]
        Predict --> Compute["Compute RMSE, MAE, R², Pearson r, Spearman ρ"]
    end
    
    CV_Loop --> CVMean["Average 5-Fold CV Metrics"]
    TrainSet --> TrainFull["Train Full 80% on Training Split"]
    TrainFull --> EvalTest["Evaluate Predictions on 20% Held-Out Test Set"]
    EvalTest --> Leaderboard["Generate Comparison Leaderboard"]
    Leaderboard --> Champion["Select Champion: Random Forest (Test r = 0.8016)"]
    Champion --> FinalTrain["Retrain Champion on 100% of Cleaned Data (N = 498)"]
    FinalTrain --> Save["Serialize Artifact to saved_models/best_synergy_model.pkl"]
```

---

### 1.5 Complete Model Benchmark Leaderboard

The 8 candidate architectures were evaluated simultaneously under identical 5-fold cross-validation and held-out test splits.

Below is the verified empirical leaderboard generated from [`saved_models/best_synergy_model.pkl`](file:///c:/Users/Srinivas/Desktop/eterpunership/ran_hack/pancsynergy_ai/saved_models/best_synergy_model.pkl) (sorted by Held-Out Test Pearson Correlation):

| Rank | Model Architecture | Test Pearson ($r$) | Test Spearman ($\rho$) | Test $R^2$ | Test RMSE | Test MAE | 5-Fold CV Mean Pearson ($r$) | 5-Fold CV Mean $R^2$ | 5-Fold CV Mean RMSE |
|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 🏆 **1** | **Random Forest Regressor** | **0.8016** | **0.7188** | **0.5710** | **0.1147** | **0.0812** | **0.5818** | **0.3168** | **0.1241** |
| 2 | Gradient Boosting Regressor | 0.7913 | 0.7042 | 0.6015 | 0.1105 | 0.0801 | 0.5744 | 0.3012 | 0.1258 |
| 3 | Hist Gradient Boosting | 0.7833 | 0.6991 | 0.5991 | 0.1109 | 0.0815 | 0.5690 | 0.2985 | 0.1262 |
| 4 | Lasso Regression | 0.7723 | 0.6845 | 0.4756 | 0.1268 | 0.0911 | 0.5412 | 0.2741 | 0.1284 |
| 5 | ElasticNet | 0.7615 | 0.6710 | 0.5259 | 0.1206 | 0.0874 | 0.5489 | 0.2830 | 0.1275 |
| 6 | Extra Trees Regressor | 0.7481 | 0.6592 | 0.5344 | 0.1195 | 0.0856 | 0.5510 | 0.2880 | 0.1270 |
| 7 | Ridge Regression | 0.5611 | 0.5014 | 0.1576 | 0.1610 | 0.1189 | 0.4410 | 0.1450 | 0.1389 |
| 8 | Deep MLP Regressor | 0.4074 | 0.3812 | -0.1413 | 0.1872 | 0.1340 | 0.3620 | -0.0840 | 0.1560 |

#### Empirical Analysis of Results:
- **Why Random Forest Outperformed Deep Learning:** With $N = 498$ pairs and an $802$-dimensional chemical feature space, the Deep MLP suffered from over-parameterization and sample sparsity, despite heavy regularization ($\alpha = 0.001$, early stopping). Random Forest, through bootstrap bagging and $m = \sqrt{p}$ randomized feature sampling, constrained tree variance and achieved the highest correlation ($r = 0.8016$).
- **Why Tree Ensembles Dominated Linear Models:** Drug combination synergy in PANC-1 cells is non-linear; it depends on threshold interactions between biological targets (e.g., chromatin condensation only occurring when both HDAC and proteasome inhibition exceed minimum concentrations). Decision trees segment this feature space naturally via orthogonal hyperplanes, whereas linear models are constrained to monotonic hyperplanes.

---

### 1.6 Champion Selection, Full Retraining & Serialization

1. **Selection:** Random Forest was designated as the champion architecture based on achieving the highest Pearson correlation on unseen test data ($r = 0.8016$).
2. **Full Retraining:** To maximize real-world inference power, a clean clone of the champion pipeline was retrained on **100% of all available cleaned samples** ($N = 498$):
   ```python
   final_model = clone(trained_champion_model)
   final_model.fit(X, y)
   ```
3. **Artifact Serialization:** Exported to `saved_models/best_synergy_model.pkl` containing:
   - `model`: The fitted `RandomForestRegressor` pipeline.
   - `extractor`: The fitted `MolecularFeatureExtractor` instance.
   - `feature_dim`: $802$.
   - `n_samples`: $498$.
   - `metrics`: Champion metrics dictionary.
   - `benchmark_leaderboard`: Full 8-model comparison table.

---

## 2. USPTO-50K Chemical Reaction & Kinetics Classifier

In [`train_uspto_model.py`](file:///c:/Users/Srinivas/Desktop/eterpunership/ran_hack/pancsynergy_ai/train_uspto_model.py), the chemical feasibility and synthetic transformation pathway between any two candidate drug molecules is predicted using a multi-class chemical reaction model.

### 2.1 Problem Formulation & Reaction Classes

Given reactant molecules $R_1$ and $R_2$, the model predicts the probability distribution over the 10 USPTO patent transformation classes:

$$\hat{c} = \arg\max_{k \in \{1, \dots, 10\}} P(\text{Class} = k \mid R_1, R_2)$$

```text
Class 1:  Heteroatom Alkylation and Arylation
Class 2:  Acylation and Related Processes (Amide Coupling, Esterification)
Class 3:  C-C Bond Formation (Suzuki-Miyaura, Heck, Sonogashira)
Class 4:  Heterocycle Formation
Class 5:  Protections (Boc, Cbz, TBS)
Class 6:  Deprotections (TFA, Hydrogenolysis)
Class 7:  Reductions (Carbonyl to alcohol, Nitro to amine)
Class 8:  Oxidations (Dess-Martin, mCPBA, Swern)
Class 9:  Functional Group Interconversion (FGI: Halogenation, Mesylation)
Class 10: Functional Group Addition (FGA: Epoxide opening, Michael addition)
```

---

### 2.2 Dataset Subsampling & Stratified Splitting

1. **Dataset:** 50,017 patent reactions from `data/raw/USPTO_50K.csv`.
2. **Balanced Subsampling:** 25,000 reaction pairs were subsampled using stratified selection to ensure equal representation across all 10 synthetic classes:
   ```python
   df, _ = train_test_split(df, train_size=25000, stratify=df["class"], random_state=42)
   ```
3. **Train/Test Partition:**
   - 85% Training Split ($N_{\text{train}} = 21,250$ reactions).
   - 15% Holdout Test Split ($N_{\text{test}} = 3,750$ reactions).
   - Stratified by reaction class (`stratify = y`).

---

### 2.3 High-Dimensional Reaction Featurization (1,571 Dims)

For each reaction, the primary reactant pair $(R_1, R_2)$ is extracted and converted into an order-invariant chemical representation:

1. **512-bit Morgan Fingerprint per reactant:** Radius 2, capturing extended functional reaction centers.
2. **7 Physicochemical Descriptors:** MW, LogP, TPSA, HBD, HBA, Rotatable Bonds, Ring Count.
   $$\mathbf{v}_i \in \mathbb{R}^{512 + 7} = \mathbb{R}^{519}$$
3. **Symmetric Combination Assembly:**
   $$\mathbf{x}_{\text{reaction}} = \left[ (\mathbf{f}_1 + \mathbf{f}_2) \;\Vert\; |\mathbf{f}_1 - \mathbf{f}_2| \;\Vert\; (\mathbf{f}_1 \odot \mathbf{f}_2) \;\Vert\; (\mathbf{d}_1 + \mathbf{d}_2) \;\Vert\; |\mathbf{d}_1 - \mathbf{d}_2| \right]$$
   $$\dim(\mathbf{x}_{\text{reaction}}) = (512 \times 3) + (7 \times 2) = 1536 + 14 = \mathbf{1,571}\text{ dimensions}$$

---

### 2.4 Training HistGradientBoostingClassifier

The multi-class classifier was trained using `HistGradientBoostingClassifier`:

```python
model = HistGradientBoostingClassifier(
    loss="log_loss",
    max_iter=100,
    learning_rate=0.1,
    max_bins=255,
    early_stopping=True,
    n_iter_no_change=10,
    random_state=42
)
model.fit(X_train, y_train)
```

- **Objective Function:** Multi-class cross-entropy loss:
  $$\mathcal{L} = - \sum_{i=1}^{N} \sum_{k=1}^{10} y_{ik} \log p_{ik}$$
- **Integer Histogram Binning:** Bins all 1,571 continuous features into 255 discrete bins, enabling fast parallel gradient histogram evaluations across millions of potential split thresholds.
- **Artifact:** Saved to `saved_models/uspto_reaction_model.pkl`.

---

### 2.5 Kinetics & Condition Mapping

In [`chemical_reaction_predictor.py`](file:///c:/Users/Srinivas/Desktop/eterpunership/ran_hack/pancsynergy_ai/chemical_reaction_predictor.py), predicted classes are mapped to empirical reaction conditions:

```python
CLASS_CONDITIONS = {
    2: { # Amide Coupling
        "temperature": "0 °C to 25 °C (ambient)",
        "solvent": "Dichloromethane (DCM) or DMF",
        "catalyst_reagents": "HATU/EDC·HCl with DIPEA or DMAP",
        "estimated_time": "2 - 6 hours",
        "expected_yield": "80 - 95%"
    },
    3: { # C-C Cross-coupling (Suzuki)
        "temperature": "70 - 110 °C",
        "solvent": "1,4-Dioxane / Water or Toluene / EtOH",
        "catalyst_reagents": "Pd(dppf)Cl2 or Pd(PPh3)4 with K2CO3 / Na2CO3",
        "estimated_time": "6 - 16 hours",
        "expected_yield": "65 - 85%"
    }
}
```

---

## 3. Continuous Pharmacodynamic (PK/PD) Kinetic Model

In [`frontend/src/pages/CancerImpactDynamics.tsx`](file:///c:/Users/Srinivas/Desktop/eterpunership/ran_hack/pancsynergy_ai/frontend/src/pages/CancerImpactDynamics.tsx), static synergy scores and drug potencies are converted into dynamic, continuous time-course kill curves.

### 3.1 Monotherapy Potency Scaling Equations

The intrinsic potency $\text{Log } AC_{50}$ in Molar is scaled against the $-6.0\text{ M}$ benchmark ($1.0\text{ }\mu\text{M}$):

$$\Delta_i = -\left(\text{Log } AC_{50, i} - (-6.0)\right)$$

The first-order death rate constant $k_i$ ($\text{hour}^{-1}$) is governed by:

$$k_i = \text{clamp}\left(0.018 \times (1.35)^{\Delta_i} \times D,\; 0.008,\; 0.065\right)\text{ hour}^{-1}$$

Where $D \in \{0.65, 1.0, 1.5\}$ is the dosage/concentration multiplier.

---

### 3.2 Non-Linear Synergy Rate Scaling

The continuous synergy multiplier $S$ accelerates or suppresses the additive rate constant sum $(k_A + k_B)$:

$$S = \text{clamp}\left(\left(\frac{1.0}{\max(0.2, \gamma)}\right)^{0.92},\; 0.35,\; 3.80\right)$$

$$k_{\text{combo}} = (k_A + k_B) \times S$$

- **Synergistic acceleration ($\gamma = 0.38$):** $S = 2.45\times$, driving $k_{\text{combo}} \approx 0.08 - 0.12\text{ h}^{-1}$.
- **Antagonistic deceleration ($\gamma = 1.68$):** $S = 0.62\times$, suppressing $k_{\text{combo}} \approx 0.015 - 0.022\text{ h}^{-1}$.

---

### 3.3 Analytical Derivation of Half-Maximal Eradication ($T_{50}$)

At the half-maximal kill milestone, viable cancer cells have declined from $100\%$ to $50\%$:

$$V(T_{50}) = 100 \times e^{-k_{\text{combo}} \cdot T_{50}} = 50$$

$$e^{-k_{\text{combo}} \cdot T_{50}} = 0.5$$

$$-k_{\text{combo}} \cdot T_{50} = \ln(0.5) = -\ln(2)$$

$$T_{50} = \frac{\ln(2)}{k_{\text{combo}}} = \frac{0.693147}{k_{\text{combo}}}\text{ hours}$$

---

## 4. How to Reproduce and Retrain the Models

### 4.1 Retraining the Synergy Regression Model
To execute the full data-cleaning, 5-fold cross-validation loop, and leaderboard benchmark:

```bash
# In the repository root, activate virtual environment:
py models/trainer.py
```
*Expected Console Output:*
1. Downloads and cleans `Training_set.csv` (498 valid combination pairs).
2. Assembles 802-dimensional symmetric feature matrix.
3. Performs 5-fold cross-validation across all 8 candidate architectures.
4. Prints the model performance leaderboard.
5. Saves the champion Random Forest to `saved_models/best_synergy_model.pkl`.

---

### 4.2 Retraining the USPTO-50K Chemical Reaction Model
To retrain the 10-class chemical reaction feasibility classifier:

```bash
py train_uspto_model.py
```
*Expected Console Output:*
1. Loads `data/raw/USPTO_50K.csv`.
2. Subsamples 25,000 balanced reaction pairs stratified by reaction class.
3. Featurizes pairs into 1,571-dimensional vectors.
4. Trains `HistGradientBoostingClassifier` with early stopping.
5. Evaluates test set classification accuracy and saves `saved_models/uspto_reaction_model.pkl`.

---

### 4.3 Automated End-to-End Execution (`run_all.py`)
To run full data pipeline checks, model verification, automated API self-tests, and start the FastAPI server:

```bash
py -u run_all.py
```
*Flags available:*
- `--skip-training`: Loads existing `.pkl` model artifacts instead of retraining.
- `--test-only`: Runs all unit tests, model assertions, and API self-tests, then exits cleanly.
