# Summary

## Parallelization Results:
- **Speedup**: 2.42
- **Efficiency**: 0.40

By parallelizing the image processing code, I achieved a speedup of 2.42, though the efficiency dropped to 0.40, indicating that not all processors were fully utilized.

---

## Machine Learning Model Results:
- **Random Forest and SVM**: Both performed poorly with low recall and F1-Score. They mainly predicted one class, leading to misleading accuracy and high precision.
- **Logistic Regression**: Performed better with higher recall and F1-Score but still needs improvement in precision.

---

## Improvement Suggestions:
1. **Address Class Imbalance** with resampling techniques or class weight adjustment.
2. **Hyperparameter Tuning** using `GridSearchCV` or `RandomizedSearchCV`.
3. **Feature Engineering** like scaling and feature selection.
4. **Try Other Models** such as Gradient Boosting or XGBoost.
5. **Use Cross-Validation** for better performance evaluation.
6. **Analyze Diagnostics** like confusion matrices and metrics (precision, recall, F1-score) for further insight.

By implementing these strategies, I aim to enhance the performance and generalization of my models.
