from afes import afe

TARGET_FOLDER = "<PATH_TO_FILES_TO_EXPLORE>"
OUTPUT_FOLDER = "<PATH_TO_OUTPUTS>"

# Run exploration on the files
df_files = afe.explore_files(TARGET_FOLDER)

# Generate pandas code to load the files
afe.generate_code(df_files)

# Run profiling on each file
afe.profile_files(df_files, profile_tool="ydata-profiling", output_path=OUTPUT_FOLDER)
afe.profile_files(df_files, profile_tool="sweetviz", output_path=OUTPUT_FOLDER)
