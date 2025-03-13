import cx_Freeze

executables = [cx_Freeze.Executable("cam2.py")]

cx_Freeze.setup(
    name="UBM Racey",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["raceDol.png"]}},
    executables = executables

    )