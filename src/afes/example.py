import src.afes.afe as afe

target_folder = "<YOUR_PATH_WITH_YOUR_FILES_TO_EXPLORE>"
df = afe.reckon_phase(target_folder)

afe.generate_python_code(df)

afe.pandas_profile_files(df)

# afe.load_datasets_to_database(df, section="<YOUR_DATABASE_NAME>")
