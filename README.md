# DeepCC9
An interpretable deep learning framework uncovers features affecting the genome editing efficiency of CRISPR-Cas9
<br><br>
We have developed an interpretable deep learning framework that integrates a novel feature extraction and selection technique with deep residual blocks. We evaluated this approach using three gold-standard datasets of Cas9 variant efficiency obtained from Nature Communications (DOI: 10.1038/s41467-019-12281-8).
<br><br>
All source codes and datasets have been uploaded to this repository.
<br><br>
The files FeatureExtract and ObtainFeatures are used for feature extraction, while ResNet implements the proposed deep residual blocks for predicting Cas9 genome editing efficiency. The Trader.py script is employed to select informative features from the extracted ones.
