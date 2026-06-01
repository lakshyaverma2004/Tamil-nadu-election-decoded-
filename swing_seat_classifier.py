import pandas as pd
import numpy as np
import os

def train_and_predict():
    base_dir = r"c:\Users\verma\OneDrive\Desktop\input_files_for_participants_rpc\data"
    df_2021 = pd.read_csv(os.path.join(base_dir, "tn_2021_results.csv"))
    df_2026 = pd.read_csv(os.path.join(base_dir, "tn_2026_results.csv"))
    
    top_2_21 = df_2021.sort_values(by=['ac_number', 'votes'], ascending=[True, False]).groupby('ac_number').head(2)
    margins_21 = {}
    for ac, group in top_2_21.groupby('ac_number'):
        if len(group) >= 2:
            diff = group.iloc[0]['votes'] - group.iloc[1]['votes']
            tot = group['votes'].sum()
            margins_21[ac] = (diff / tot) * 100 if tot > 0 else 0
        else:
            margins_21[ac] = 100.0
            
   
    top_2_26 = df_2026.sort_values(by=['ac_number', 'votes'], ascending=[True, False]).groupby('ac_number').head(2)
    margins_26 = {}
    for ac, group in top_2_26.groupby('ac_number'):
        if len(group) >= 2:
            diff = group.iloc[0]['votes'] - group.iloc[1]['votes']
            tot = group['votes'].sum()
            margins_26[ac] = (diff / tot) * 100 if tot > 0 else 0
        else:
            margins_26[ac] = 100.0


    flips_df = pd.read_csv(os.path.join(base_dir, "processed", "constituency_winners_and_flips.csv"))
    flips_df['turnout_surge'] = flips_df['turnout_2026'] - flips_df['turnout_2021']
    flips_df['margin_2021'] = flips_df['ac_number'].map(margins_21)
    flips_df['margin_2026'] = flips_df['ac_number'].map(margins_26)
    
  
    y = flips_df['is_flip'].astype(int).values
    x1 = flips_df['turnout_surge'].values
    x2 = (30.0 - flips_df['margin_2021']).values 
    
   
    x1_mean, x1_std = np.mean(x1), np.std(x1)
    x2_mean, x2_std = np.mean(x2), np.std(x2)
    x1_norm = (x1 - x1_mean) / (x1_std if x1_std > 0 else 1.0)
    x2_norm = (x2 - x2_mean) / (x2_std if x2_std > 0 else 1.0)
    
    
    w = np.array([0.0, 0.0, 0.0]) 
    lr = 0.05
    epochs = 1000
    
    def sigmoid(z):
        return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))
        
    for _ in range(epochs):
        z = w[0] + w[1] * x1_norm + w[2] * x2_norm
        predictions = sigmoid(z)
        errors = predictions - y
        
       
        g0 = np.mean(errors)
        g1 = np.mean(errors * x1_norm)
        g2 = np.mean(errors * x2_norm)
        
        
        w[0] -= lr * g0
        w[1] -= lr * g1
        w[2] -= lr * g2
        
   
    final_z = w[0] + w[1] * x1_norm + w[2] * x2_norm
    probabilities = sigmoid(final_z)
    
    flips_df['swing_probability'] = [round(p, 4) for p in probabilities]
    flips_df['predicted_class'] = [1 if p >= 0.5 else 0 for p in probabilities]
    
    accuracy = (flips_df['predicted_class'] == y).mean() * 100
    print(f"Swing Seat Classifier successfully trained.")
    print(f"Final Weights: Intercept={w[0]:.4f}, Turnout Surge={w[1]:.4f}, Inverse Margin={w[2]:.4f}")
    print(f"Model Classification Accuracy: {accuracy:.2f}%")
    
    # Save predictions
    flips_df.to_csv(os.path.join(base_dir, "processed", "swing_predictions.csv"), index=False)
    print("Saved swing predictions to swing_predictions.csv!")

if __name__ == '__main__':
    train_and_predict()
