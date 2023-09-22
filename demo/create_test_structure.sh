#!/bin/bash

# Define the base directory where you want to start the operation
base_directory="apps"

# Function to create the test directory structure
create_test_structure() {
    local dir="$1"
    touch "$dir/test/__init__.py"
    touch "$dir/test/test_models/__init__.py"
    touch "$dir/test/test_views/__init__.py"
}

# Iterate through each subdirectory in the base directory
for dir in "$base_directory"/*; do
    if [ -d "$dir" ]; then
        echo "Creating test structure in $dir"
        create_test_structure "$dir"
    fi
done

echo "Directory structure creation complete."
