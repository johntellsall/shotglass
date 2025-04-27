# main2.py -- import file info only

import state


    # insert_file = (
    #     "insert into file (project_id, release, path, hash, size_bytes)"
    #     f" values ({project_id}, '{release}', :path, :hash, :size_bytes)"
    # )
    # con.executemany(insert_file, items)
def show_stats(db):
    num_files = state.query1(db, table="file")
    print(f"Number of files in the database: {num_files}")

def add_project(project_dir):
    pass

def main(project_dirs):
    db = state.get_db(temporary=True)
    for project_dir in project_dirs:
        add_project(project_dir)

    show_stats(db)

if __name__ == "__main__":
    import sys
    project_dirs = sys.argv[1:]
    main(project_dirs)
