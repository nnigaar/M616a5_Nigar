import pandas as pd
 
# =====================================================================
#  DERS 3 · 1-ci HISSE (sizin yazdiginiz kod, deyisdirilmeyib)
# =====================================================================
 
# 1. CSV faylini oxumaq
df = pd.read_csv("src/measurements.csv")
 
# 2. Butun melumatlari goster
print("\n--- BUTUN MELUMATLAR ---")
print(df)
 
# 3. Setir ve sutun sayi
print("\n--- SHAPE ---")
print(df.shape)
 
# 4. Ilk 5 setir
print("\n--- HEAD ---")
print(df.head())
 
# 5. Ilk 2 setir
print("\n--- ILK 2 SETIR ---")
print(df.head(2))
 
# 6. Melumatlar haqqinda umumi melumat
print("\n--- INFO ---")
df.info()
 
# 7. Sutunlarin data tipleri
print("\n--- DATA TYPES ---")
print(df.dtypes)
 
# 8. Her sutunda bos deyerlerin sayi
print("\n--- BOS DEYERLER ---")
print(df.isna().sum())
 
# 9. Dublikat setirlerin sayi
print("\n--- DUBLIKATLAR ---")
print(df.duplicated().sum())
 
# 10. Bos deyerleri silmek
df = df.dropna()
 
# 11. Dublikat setirleri silmek
df = df.drop_duplicates()
 
print("\n--- TEMIZLENMIS MELUMATLAR ---")
print(df)
 
# 12. Zeif siqnallari tapmaq
print("\n--- RSRP < -100 ---")
zeif_siqnallar = df[df["rsrp_dbm"] < -100]
print(zeif_siqnallar)
 
# 13. RSRP -90-dan kicik olan siqnallar
print("\n--- RSRP < -90 ---")
print(df[df["rsrp_dbm"] < -90])
 
# 14. Yalniz RSRP sutununu goster
print("\n--- RSRP SUTUNU ---")
print(df["rsrp_dbm"])
 
# 15. Yalniz region ve station sutunlari
print("\n--- REGION VE STATION ---")
print(df[["region", "station"]])
 
# 16. Yasamal regionunu filter etmek
print("\n--- YASAMAL ---")
print(df[df["region"] == "Yasamal"])
 
# 17. Siqnallari guclu qiymetden zeif qiymete siralamaq
print("\n--- SIRALANMIS SIQNALLAR ---")
print(df.sort_values("rsrp_dbm", ascending=False))
 
# 18. Region uzre orta siqnal gucu
print("\n--- REGION UZRE ORTA SIQNAL ---")
print(df.groupby("region")["rsrp_dbm"].mean())
 
# 19. Region uzre stansiya sayi
print("\n--- REGION UZRE STANSIYA SAYI ---")
print(df.groupby("region")["station"].count())
 
# 20. Statistik melumatlar
print("\n--- STATISTIKA ---")
print(df["rsrp_dbm"].describe())
 
# 21. Her regionda nece ferqli stansiya var
print("\n--- FERQLI STANSIYALAR ---")
print(df.groupby("region")["station"].nunique())
 
# 22. Yeni sutun yaratmaq
df["signal_status"] = df["rsrp_dbm"].apply(
    lambda x: "Zeif" if x < -100 else "Normal"
)
 
print("\n--- SIQNAL STATUSU ---")
print(df[["region", "station", "rsrp_dbm", "signal_status"]])
 
# 23. Temizlenmis melumatlari yeni CSV faylina yazmaq
df.to_csv("src/measurements_clean.csv", index=False)
 
print("\nNetice measurements_clean.csv faylina yazildi.")
 
 
# =====================================================================
#  DERS 3 · 2-ci HISSE: pandas merhele-merhele
#  oxu -> filtr -> temizle -> qruplasdir
#  (fayl yeniden oxunur, ona gore 1-ci hisseden asili deyil)
# =====================================================================
 
print("\n\n" + "=" * 60)
print("DERS 3 · pandas merhele-merhele")
print("=" * 60)
 
# ---------------------------------------------------------------------
# MERHELE 1 · faylı oxu ve bax (T1 + Praktika 1)
# ---------------------------------------------------------------------
df = pd.read_csv("src/measurements.csv")
 
print("\n--- [D3 · M1] SETIR SAYI ---")
print(len(df))                                   # Praktika 1: len(df)
 
print("\n--- [D3 · M1] SUTUN SAYI ---")
print(df.shape[1])                               # Praktika 1: shape-in ikinci ededi
 
print("\n--- [D3 · M1] SON 5 SETIR (tail) ---")
print(df.tail())                                 # head-in eksi
 
print("\n--- [D3 · M1] BIRINCI SETRIN REGIONU ---")
print(df["region"][0])                           # Praktika 1: sutun, sonra element
 
# ---------------------------------------------------------------------
# MERHELE 2 · sutun ve filtr (T2 + Praktika 2)
# ---------------------------------------------------------------------
rsrp = df["rsrp_dbm"]                            # bir sutun (Series)
 
print("\n--- [D3 · M2] RSRP: ORTA / MAX / MIN ---")
print("Orta RSRP:", round(rsrp.mean(), 1))       # mean() NaN-lari ozu buraxir
print("En guclu siqnal (max):", rsrp.max())
print("En zeif siqnal (min):", rsrp.min())
 
print("\n--- [D3 · M2] MASKA ---")
mask = df["rsrp_dbm"] < -100                     # her setir ucun True / False
print(mask.head(3))
weak = df[mask]                                  # yalniz True olan setirler
print("Zeif olcme sayi:", len(weak))
 
# Surpriz (T2 3/4): temizlenmemis adlarla filtr az setir tapir
print("Yasamal setirleri (temizlemeden evvel):", len(df[df["region"] == "Yasamal"]))
 
# ---------------------------------------------------------------------
# MERHELE 3 · temizleme (T3 + Praktika 3)
# ---------------------------------------------------------------------
print("\n--- [D3 · M3] TEMIZLEME ---")
print("Oxunan setir:", len(df))
print(df.isna().sum())                           # her sutunda bos deyer sayi
 
# 1) region adlari: kenar bosluqlar ve herf olcusu
print("Region varianti (evvel):", df["region"].nunique())
df["region"] = df["region"].str.strip().str.capitalize()
print("Region varianti (sonra):", df["region"].nunique())
print("Yasamal setirleri (temizlemeden sonra):", len(df[df["region"] == "Yasamal"]))
 
# 2) menfi throughput = sensor xetasi (yalniz sutun varsa)
if "throughput_mbps" in df.columns:
    print("Menfi throughput:", len(df[df["throughput_mbps"] < 0]))
    df = df[df["throughput_mbps"] >= 0]
 
# 3) dublikatlar
print("Dublikat:", df.duplicated().sum())
df = df.drop_duplicates()
 
# 4) bos rsrp: dersde SAXLANILIR (mean() ozu buraxir), dropna etmirik
print("Bos rsrp qaldi:", df["rsrp_dbm"].isna().sum())
print("dropna etseydik:", len(df.dropna()))      # sadece baxiriq
 
df.to_csv("src/measurements_clean_pd.csv", index=False)
print("Yazilan setir:", len(df))
 
# ---------------------------------------------------------------------
# MERHELE 4 · qruplasdirma: bol -> hesabla -> birlesdir (T4 + Praktika 4)
# ---------------------------------------------------------------------
print("\n--- [D3 · M4] REGION UZRE ORTA RSRP (sirali) ---")
avg = df.groupby("region")["rsrp_dbm"].mean()
print(avg.round(1).sort_values())                # kicikden boyuye
 
print("\n--- [D3 · M4] REGION UZRE SETIR SAYI (size) ---")
print(df.groupby("region").size())
 
print("\n--- [D3 · M4] REGION UZRE MIN / MAX RSRP ---")
print(df.groupby("region")["rsrp_dbm"].agg(["min", "max"]))
 
# Praktika 4 (yalniz sutunlar varsa)
if "throughput_mbps" in df.columns:
    print("\n--- [D3 · M4] REGION UZRE ORTA THROUGHPUT ---")
    print(df.groupby("region")["throughput_mbps"].mean().round(1))
 
if "drop_calls" in df.columns:
    print("\n--- [D3 · M4] REGION UZRE DUSEN ZENGLER ---")
    print(df.groupby("region")["drop_calls"].sum())
    print("Cemi:", df["drop_calls"].sum())
 