import pandas as pd
import json
from datetime import datetime

# Replace 'your_file.csv' with the path to your CSV file
df = pd.read_csv('realized_routes_202310061343.csv')

def expand_control_points(row):
    try:
        control_points = json.loads(row['control_point_times'])
        times = control_points.get('times', [])
        routes = control_points.get('route', [])
        expanded_times_routes = [(t[0], t[1], routes[i]) for i, t in enumerate(times) if t[0] != "-1" and t[1] != "-1"]
        return expanded_times_routes
    except json.JSONDecodeError as e:
        print(f"Error parsing row {row['control_point_times']}: {e}")
        return []

# Apply the function and expand the DataFrame
expanded_rows = []
for _, row in df.iterrows():
    for start_time, end_time, route in expand_control_points(row):
        expanded_rows.append({'timestamp': start_time, 'route': route, **row.to_dict()})
        expanded_rows.append({'timestamp': end_time, 'route': route, **row.to_dict()})

expanded_df = pd.DataFrame(expanded_rows)

# Sort by timestamp
expanded_df['timestamp'] = pd.to_datetime(expanded_df['timestamp'])
expanded_df.sort_values(by='timestamp', inplace=True)

# Drop unnecessary columns
final_df = expanded_df.drop(columns=['control_point_times'])

# Save to a new CSV file
final_df.to_csv('modified_data.csv', index=False)

# Display the first few rows of the final DataFrame
print(final_df.head())