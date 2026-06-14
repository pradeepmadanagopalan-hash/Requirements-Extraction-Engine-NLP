import pandas as pd

def export_excel(results, filename):

    df = pd.DataFrame(results)

    df.insert(0, "Requirement ID", [f"REQ-{i+1:05d}" for i in range(len(df))])

    df_main = df[df["Section"] == "MAIN"]
    df_annex = df[df["Section"] == "ANNEX"]

    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        df_main.to_excel(writer, sheet_name="Main", index=False)
        df_annex.to_excel(writer, sheet_name="Annex", index=False)
        df.to_excel(writer, sheet_name="All", index=False)

    print(f"\n📁 Exported: {filename}")