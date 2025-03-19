import csv
import os
import random

v = 100000
targetDir = '/Users /'
os.makedirs(targetDir, exist_ok=True)
edges_per_file = 99999
current_file_count = 0
desired_file_count = 7

def create_vertices():
    fn_v = targetDir + 'StressTestV.csv'
    if not os.path.exists(fn_v):
        print(f'Creating {v} vertices...')
        v_list = [[i] for i in range(v)]
        with open(fn_v, 'w+') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(v_list)
        os.chmod(fn_v, 0o775)
        print(f'Vertex file created with {v} vertices')
    else:
        print(f'Vertex file already exists: {fn_v}')

def create_edges(iteration):
    global current_file_count
    print(f'Iteration {iteration}: Checking/creating edge files up to {desired_file_count}...')
    
    files_to_create = max(0, desired_file_count - current_file_count)
    if files_to_create > 0:
        print(f'Creating {files_to_create} new edge files...')
    
    for file_num in range(current_file_count, desired_file_count):
        fn_e = f"{targetDir}StressTest2_Edges_{iteration}_{file_num}.csv"
        if not os.path.exists(fn_e):
            e_list = []
            for _ in range(edges_per_file):
                v_from = random.randint(0, v-1)
                possible_targets = list(range(v))
                possible_targets.remove(v_from)
                v_to = random.choice(possible_targets)
                e_list.append([str(v_from), str(v_to), f"{v_from}-{v_to}"])
            
            with open(fn_e, 'w+') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerows(e_list)
            os.chmod(fn_e, 0o775)
            print(f'Created new file: {fn_e}')
        else:
            print(f'File already exists, skipping: {fn_e}')
    
    current_file_count = desired_file_count
    total_edges = current_file_count * edges_per_file
    print(f'Iteration {iteration} complete: Total {current_file_count} files with {total_edges} edges')

def count_cumulative_unique_edges(iteration):
    print(f'Counting cumulative unique edges for iteration {iteration}...')
    all_unique_edges = set()  # To store all unique edges across files
    cumulative_unique_count = 0

    for file_num in range(desired_file_count):
        fn_e = f"{targetDir}StressTest2_Edges_{iteration}_{file_num}.csv"
        if os.path.exists(fn_e):
            file_edges = set()
            with open(fn_e, 'r') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    # Use (v_from, v_to) as the unique key, ignoring the label
                    edge = (int(row[0]), int(row[1]))
                    file_edges.add(edge)
            
            # Count unique edges within this file
            unique_in_file = len(file_edges)
            print(f'File {fn_e}: {unique_in_file} unique edges')

            # Compute cumulative unique edges
            new_unique_edges = file_edges - all_unique_edges
            cumulative_unique_count += len(new_unique_edges)
            all_unique_edges.update(file_edges)
            print(f'Cumulative unique edges after file {file_num}: {cumulative_unique_count}')

    # Final total unique edges across all files
    total_unique_edges = len(all_unique_edges)
    print(f'Total unique edges across all {desired_file_count} files: {total_unique_edges}')
    return total_unique_edges

def generate_files():
    create_vertices()
    create_edges(0)
    count_cumulative_unique_edges(0)

if __name__ == "__main__":
    generate_files()
