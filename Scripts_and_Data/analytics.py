def print_dashboard(results):

    print("\n" + "="*80)
    print("📊 ADAS REQUIREMENTS DASHBOARD ")
    print("="*80)

    total = len(results)

    main = sum(1 for r in results if r["Section"] == "MAIN")
    annex = sum(1 for r in results if r["Section"] == "ANNEX")

    print(f"Total Requirements     : {total}")
    print(f"Main Section          : {main}")
    print(f"Annex Section         : {annex}")

    from collections import Counter

    print("\n📌 Requirement Type Distribution:")
    for k, v in Counter(r["Requirement Type"] for r in results).most_common():
        print(k, v)

    print("\n📌 Section Breakdown (%):")
    print(f"MAIN  : {main/total*100:.2f}")
    print(f"ANNEX : {annex/total*100:.2f}")

    print("\n📌 Top Clauses (Hotspots):")
    for k, v in Counter(r["Clause"] for r in results).most_common(10):
        print(k, v)

    print("\n📌 Quality Metrics:")
    general = sum(1 for r in results if r["Requirement Type"] == "General") / total * 100
    print(f"General / Unclassified Rate: {general:.2f}%")