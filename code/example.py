import auto_fe as afe

target_folder = "<YOUR_PATH_WITH_YOUR_FILES_TO_EXPLORE>"
df = afe.reckon_phase(target_folder)

afe.generate_python_code(df)

afe.pandas_profile_files(df)
