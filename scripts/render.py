import os, sys, glob, yaml
from jinja2 import Environment, FileSystemLoader

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f) or {}

def main(env_name, env_file, db_list_file, out_dir="rendered"):
    os.makedirs(out_dir, exist_ok=True)

    env_vars = load_yaml(env_file)
    all_dbs = load_yaml(db_list_file).get("DATABASES", [])
    if not all_dbs:
        raise SystemExit("No DATABASES defined in databases.yaml")

    jenv = Environment(loader=FileSystemLoader("sql"),
                       keep_trailing_newline=True, autoescape=False)

    suffix = env_vars["DB_SUFFIX"]
    for base in all_dbs:
        db_name = f"{base}{suffix}"
        vars_for_db = {**env_vars, "DB_NAME": db_name, "BASE_DB": base}
        for path in sorted(glob.glob("sql/*.sql.j2")):
            tpl = jenv.get_template(os.path.basename(path))
            rendered = tpl.render(**vars_for_db)
            # filename: <env>__<BASE_DB>__<original.sql>
            out_path = os.path.join(
                out_dir,
                f"{env_name}__{base}__{os.path.basename(path).replace('.j2','')}"
            )
            with open(out_path, "w") as f:
                f.write(rendered)
            print(f"Rendered: {out_path}")

if __name__ == "__main__":
    # usage: render.py <env> <env_file> <databases.yaml> [outdir]
    env_name = sys.argv[1]
    env_file = sys.argv[2]
    db_list_file = sys.argv[3]
    out_dir = sys.argv[4] if len(sys.argv) > 4 else "rendered"
    main(env_name, env_file, db_list_file, out_dir)
