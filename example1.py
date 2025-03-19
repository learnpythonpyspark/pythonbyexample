import csv
import os
import subprocess

# Configuration
targetDir = 'shared/path'
output_csv = os.path.join(targetDir, 'unique_edge_summary.csv')
iteration = 0  # Assuming iteration 0, adjust if different
desired_file_count = 30  # Total number of edge files to process
shell_script = os.path.join(targetDir, 'load_edges.sh')  # Path to your shell script

def run_shell_command(file_num):
    print(f'Running shell script for file {file_num}...')
    cmd = f'bash {shell_script} {file_num}'
    log_file = os.path.join(targetDir, f'load_log_{file_num}.log')
    with open(log_file, 'w') as log:
        subprocess.run(cmd, shell=True, stdout=log, stderr=log)
    return log_file

def parse_log_for_counts(log_file):
    vertex_count = 0
    edge_count = 0
    try:
        with open(log_file, 'r') as f:
            for line in f:
                # Adjust the following lines based on your log format
                if 'Total vertices loaded' in line:
                    vertex_count = int(line.split()[-1])
                elif 'Total edges loaded' in line:
                    edge_count = int(line.split()[-1])
    except Exception as e:
        print(f'Error parsing log file {log_file}: {e}')
    return vertex_count, edge_count

def count_cumulative_unique_edges():
    print(f'Counting cumulative unique edges for iteration {iteration}...')
    
    # Initialize sets and lists to track data
    all_unique_edges = set()
    cumulative_unique_count = 0
    summary_data = []

    # Process each file
    for file_num in range(desired_file_count):
        fn_e = f"{targetDir}StressTest2_Edges_{iteration}_{file_num}.csv"
        if os.path.exists(fn_e):
            # Run shell script to load the file and generate log
            log_file = run_shell_command(file_num)
            
            # Parse log to get vertex and edge counts
            total_vertex_count, total_edge_count = parse_log_for_counts(log_file)
            print(f'Log {log_file}: Total vertices = {total_vertex_count}, Total edges = {total_edge_count}')

            file_edges = set()
            with open(fn_e, 'r') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    # Use (v_from, v_to) as the unique key, ignoring the label
                    edge = (int(row[0]), int(row[1]))
                    file_edges.add(edge)
            
            # Count unique edges within this file
            unique_in_file = len(file_edges)
            
            # Compute cumulative unique edges
            new_unique_edges = file_edges - all_unique_edges
            cumulative_unique_count += len(new_unique_edges)
            all_unique_edges.update(file_edges)
            
            # Store data for this file
            summary_data.append({
                'file_name': fn_e,
                'unique_edges_in_file': unique_in_file,
                'cumulative_unique_edges': cumulative_unique_count,
                'total_vertex_count': total_vertex_count,
                'total_edge_count': total_edge_count
            })
            print(f'File {fn_e}: {unique_in_file} unique edges, Cumulative: {cumulative_unique_count}')
        else:
            print(f'File {fn_e} does not exist, skipping...')
    
    # Write or append summary to CSV
    file_exists = os.path.isfile(output_csv)
    with open(output_csv, 'a' if file_exists else 'w', newline='') as f:
        fieldnames = ['file_name', 'unique_edges_in_file', 'cumulative_unique_edges', 'total_vertex_count', 'total_edge_count']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(summary_data)
    
    # Final total unique edges
    total_unique_edges = len(all_unique_edges)
    print(f'Total unique edges across all {desired_file_count} files: {total_unique_edges}')
    print(f'Summary saved to {output_csv}')

if __name__ == "__main__":
    count_cumulative_unique_edges()
