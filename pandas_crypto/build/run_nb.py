import json, sys, io, contextlib, traceback
import matplotlib; matplotlib.use("Agg")
path, solfile = sys.argv[1], sys.argv[2]
nb = json.load(open(path))
sols = json.load(open(solfile))     # {"index": "code"} pour les cellules vides
ns = {}
# Colab definit display() ; on le reproduit pour que le test voie la meme chose
ns["display"] = lambda *args: [print(a) for a in args]
n_code = 0; failures = []; expected_err = []
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    # une solution existe pour cette cellule : elle remplace le contenu, vide ou
    # simple squelette de commentaires (le corps de boucle de l'assignment 1)
    if str(i) in sols:
        src = sols[str(i)]
    elif not src.strip():
        print(f"[{i}] cellule vide sans solution"); continue
    src = src.replace("# reponse = ", "reponse = ") if "secours" in src or src.startswith("# reponse") else src
    n_code += 1
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            # afficher la valeur de la derniere expression comme Colab
            import ast
            tree = ast.parse(src)
            if tree.body and isinstance(tree.body[-1], ast.Expr):
                exec(compile(ast.Module(tree.body[:-1], []), "<cell>", "exec"), ns)
                val = eval(compile(ast.Expression(tree.body[-1].value), "<cell>", "eval"), ns)
                if val is not None: print(repr(val))
            else:
                exec(compile(tree, "<cell>", "exec"), ns)
        out = buf.getvalue().strip()
        if "A REVOIR" in out: failures.append((i, out))
        print(f"[{i}] ok  {out[:110]!r}")
    except Exception as e:
        expected_err.append((i, type(e).__name__, str(e)[:80]))
        print(f"[{i}] ERR {type(e).__name__}: {str(e)[:80]}")
print("\n--- cellules code executees:", n_code)
print("--- verifier en echec:", failures)
print("--- erreurs (doivent toutes etre voulues):")
for x in expected_err: print("   ", x)
