# DeepCC9
An interpretable deep learning framework uncovers features affecting the genome editing efficiency of CRISPR-Cas9
<br><br>
We have developed an interpretable deep learning framework that integrates a novel feature extraction and selection technique with deep residual blocks. We evaluated this approach using three gold-standard datasets of Cas9 variant efficiency obtained from Nature Communications (DOI: 10.1038/s41467-019-12281-8).
<br><br>
All source codes and datasets have been uploaded to this repository.
<br><br>
The FeatureExtract and ObtainFeatures files are used for feature extraction, while ResNet implements the proposed deep residual blocks for predicting Cas9 genome editing efficiency. The Trader.py script is employed to select a potential feature set from the extracted features.
<br><br><br>

## File Descriptions

### `Data.txt`
It shows an example of the data format used in the feature extraction step.

### `FeatureExtract.py`
Implements the extraction of predefined sequence features from sgRNA sequences, including:
- **Frequency-based sequence motifs** (i.e., di-, tri-, and tetra-nucleotides)
- **Position-specific presence or absence** of sequence motifs along the sgRNA
- **Four binary features to show the PAM sequences

### `ObtainFeatures.py`
Organizes and formats the extracted sequence features into a structured feature matrix suitable for downstream modeling and feature selection.

### `Trader.py`
Implements the **Trader (TR) metaheuristic optimization algorithm** for the construction of the potential feature set.
- Each candidate solution selects a subset of features
- Feature subsets are evaluated using a regression model to identify features that most strongly influence Cas9 genome editing efficiency

### `ResNet.py`
Defines the **deep residual learning architecture** used in DeepCC9.
- Consists of fully connected layers with skip connections
- Enables efficient learning from selected features while preserving feature interactions
- Improves training stability and predictive performance
