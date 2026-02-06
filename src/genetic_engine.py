import numpy as np
import pandas as pd
from gplearn.genetic import SymbolicRegressor

def run_genetic_search(X, y):
    split = int(len(X) * 0.7)
    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]

    print(f"   > Evolving formulas on {len(X_train)} data points... (This may take 1-2 mins)")

    est = SymbolicRegressor(
        population_size=8000,
        generations=25,
        tournament_size=20,
        stopping_criteria=1.0,
        const_range=(-1.0, 1.0),
        p_crossover=0.7,
        p_subtree_mutation=0.1,
        p_hoist_mutation=0.05,
        p_point_mutation=0.1,
        max_samples=0.9,
        verbose=0,
        metric='pearson',
        parsimony_coefficient=0.002,
        random_state=42,
        n_jobs=-1,
        feature_names=X.columns
    )

    est.fit(X_train, y_train)

    print(f"   > Discovery Complete. Best Formula Length: {est._program.length_}")
    return est, X_test, y_test