"""
Caretaker Performance Dataset Generator & Storage
Generates a structured, realistic dataset for Caretaker Performance Classification.
"""

import os
import pandas as pd
import numpy as np

DATASET_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(DATASET_DIR, 'caretaker_performance_dataset.csv')

def generate_caretaker_dataset(num_samples=400, random_seed=42):
    """
    Generates a realistic, structured dataset of caretakers with:
    - experience_years
    - completed_bookings
    - cancelled_bookings
    - average_rating
    - total_reviews
    - response_time_minutes
    - customer_complaints
    - repeat_customers
    - performance_level (Poor, Average, Good, Excellent)
    """
    np.random.seed(random_seed)
    
    records = []
    
    # Target distribution: ~20% Poor, ~30% Average, ~30% Good, ~20% Excellent
    per_class = {
        'Poor': int(num_samples * 0.20),
        'Average': int(num_samples * 0.30),
        'Good': int(num_samples * 0.30),
        'Excellent': int(num_samples * 0.20),
    }
    
    caretaker_id_counter = 1001
    
    # 1. POOR Performers
    for _ in range(per_class['Poor']):
        exp = round(float(np.random.uniform(0.2, 3.0)), 1)
        completed = int(np.random.randint(1, 15))
        cancelled = int(np.random.randint(3, 12))
        rating = round(float(np.random.uniform(2.0, 3.4)), 2)
        reviews = int(max(1, completed - np.random.randint(0, 4)))
        resp_time = int(np.random.randint(60, 180)) # Slow response: 60-180 mins
        complaints = int(np.random.randint(2, 6))
        repeats = int(np.random.randint(0, 2))
        
        records.append({
            'caretaker_id': f"CT_{caretaker_id_counter}",
            'experience_years': exp,
            'completed_bookings': completed,
            'cancelled_bookings': cancelled,
            'average_rating': rating,
            'total_reviews': reviews,
            'response_time_minutes': resp_time,
            'customer_complaints': complaints,
            'repeat_customers': repeats,
            'performance_level': 'Poor'
        })
        caretaker_id_counter += 1

    # 2. AVERAGE Performers
    for _ in range(per_class['Average']):
        exp = round(float(np.random.uniform(0.5, 4.5)), 1)
        completed = int(np.random.randint(10, 35))
        cancelled = int(np.random.randint(2, 6))
        rating = round(float(np.random.uniform(3.5, 4.2)), 2)
        reviews = int(max(2, completed - np.random.randint(1, 6)))
        resp_time = int(np.random.randint(30, 75)) # 30-75 mins
        complaints = int(np.random.randint(1, 3))
        repeats = int(np.random.randint(2, 6))
        
        records.append({
            'caretaker_id': f"CT_{caretaker_id_counter}",
            'experience_years': exp,
            'completed_bookings': completed,
            'cancelled_bookings': cancelled,
            'average_rating': rating,
            'total_reviews': reviews,
            'response_time_minutes': resp_time,
            'customer_complaints': complaints,
            'repeat_customers': repeats,
            'performance_level': 'Average'
        })
        caretaker_id_counter += 1

    # 3. GOOD Performers
    for _ in range(per_class['Good']):
        exp = round(float(np.random.uniform(1.5, 6.0)), 1)
        completed = int(np.random.randint(30, 80))
        cancelled = int(np.random.randint(0, 3))
        rating = round(float(np.random.uniform(4.3, 4.74)), 2)
        reviews = int(max(5, completed - np.random.randint(2, 10)))
        resp_time = int(np.random.randint(12, 35)) # 12-35 mins
        complaints = int(np.random.choice([0, 1], p=[0.75, 0.25]))
        repeats = int(np.random.randint(6, 18))
        
        records.append({
            'caretaker_id': f"CT_{caretaker_id_counter}",
            'experience_years': exp,
            'completed_bookings': completed,
            'cancelled_bookings': cancelled,
            'average_rating': rating,
            'total_reviews': reviews,
            'response_time_minutes': resp_time,
            'customer_complaints': complaints,
            'repeat_customers': repeats,
            'performance_level': 'Good'
        })
        caretaker_id_counter += 1

    # 4. EXCELLENT Performers
    for _ in range(per_class['Excellent']):
        exp = round(float(np.random.uniform(2.5, 10.0)), 1)
        completed = int(np.random.randint(60, 160))
        cancelled = int(np.random.choice([0, 1], p=[0.8, 0.2]))
        rating = round(float(np.random.uniform(4.75, 5.0)), 2)
        reviews = int(max(15, completed - np.random.randint(3, 15)))
        resp_time = int(np.random.randint(5, 18)) # Fast: 5-18 mins
        complaints = 0
        repeats = int(np.random.randint(15, 45))
        
        records.append({
            'caretaker_id': f"CT_{caretaker_id_counter}",
            'experience_years': exp,
            'completed_bookings': completed,
            'cancelled_bookings': cancelled,
            'average_rating': rating,
            'total_reviews': reviews,
            'response_time_minutes': resp_time,
            'customer_complaints': complaints,
            'repeat_customers': repeats,
            'performance_level': 'Excellent'
        })
        caretaker_id_counter += 1

    df = pd.DataFrame(records)
    # Shuffle dataset
    df = df.sample(frac=1.0, random_state=random_seed).reset_index(drop=True)
    os.makedirs(DATASET_DIR, exist_ok=True)
    df.to_csv(DATASET_PATH, index=False)
    print(f"Generated {len(df)} caretaker records saved to: {DATASET_PATH}")
    return df

if __name__ == '__main__':
    generate_caretaker_dataset()
