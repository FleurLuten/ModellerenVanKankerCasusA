import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel("tumorgrowth.xlsx", sheet_name="AnalysisData")

tumor_id = 101

tumor = data[data["ID"] == tumor_id]
tumor = tumor.sort_values(by="Day")

plt.scatter(tumor["Day"], tumor["Size"], label="Gemeten Tumorgrootte")

plt.xlabel("Tijd (dagen)")
plt.ylabel("Tumorgrootte")
plt.title(f"Groei van tumor {tumor_id}")

plt.legend()
plt.grid(True); plt.box(False)

plt.show()
