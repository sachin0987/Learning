#!/bin/ksh

# Function to find the latest file matching a pattern in a directory
find_latest_matching_file() {
    typeset directory="$1"
    typeset pattern="$2"

    # Find files matching the pattern in the directory
    typeset -a matching_files
    matching_files=($(find "$directory" -type f -name "$pattern"))

    # Check if there are any matching files
    if [ ${#matching_files[@]} -eq 0 ]; then
        echo "No files matching the pattern found in $directory"
    else
        # Get the latest file based on modification time
        typeset latest_file=""
        typeset latest_mtime=0
        for file in "${matching_files[@]}"; do
            typeset file_mtime=$(stat -c %Y "$file")
            if [ $file_mtime -gt $latest_mtime ]; then
                latest_mtime=$file_mtime
                latest_file=$file
            fi
        done
        echo "Latest file matching the pattern '$pattern':"
        echo "$latest_file"
    fi
}

# Usage example: Call the function with directory and pattern
test_file=$(find_latest_matching_file "/Users/sachin/Desktop/Projects_Personal/CLI2Structured" "test_*_*_test.csv")
