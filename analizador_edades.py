import sys
import os
import pandas as pd
import matplotlib.pyplot as plt

def analizar_archivo(ruta_archivo):

    # leer archivo
    df = pd.read_csv(ruta_archivo, header=None)
    df.columns = ["edad"]

    # clasificar edades
    df["categoria"] = pd.cut(
        df["edad"],
        bins=[0,18,25,30,40,100],
        labels=["Bebe","Adulto joven","Tercer piso","Treintañero","Modo señor"]
    )

    # estadísticas
    total = df["edad"].count()
    promedio = round(df["edad"].mean())
    mayor = df["edad"].max()
    menor = df["edad"].min()

    print("Total personas:", total)
    print("Promedio edad:", promedio)
    print("Mayor:", mayor)
    print("Menor:", menor)

    # crear carpeta reporte
    if not os.path.exists("reporte"):
        os.mkdir("reporte")

    # -------- gráfica histograma --------
    df["edad"].hist()

    plt.title("Distribución de edades")
    plt.xlabel("Edad")
    plt.ylabel("Cantidad de personas")

    hist_path = "reporte/histograma_edades.png"
    plt.savefig(hist_path)
    plt.close()

    # -------- gráfica categorias --------
    df["categoria"].value_counts().plot(kind="bar")

    plt.title("Personas por categoría de edad")
    plt.xlabel("Categoría")
    plt.ylabel("Cantidad")

    cat_path = "reporte/categorias_edades.png"
    plt.savefig(cat_path)
    plt.close()

    # -------- generar excel --------
    writer = pd.ExcelWriter("reporte/reporte_edades.xlsx", engine="xlsxwriter")

    df.to_excel(writer, sheet_name="datos", index=False)

    workbook = writer.book
    worksheet = writer.sheets["datos"]

    worksheet.insert_image("E2", hist_path)
    worksheet.insert_image("E20", cat_path)

    writer.close()

    print("Reporte generado en carpeta /reporte")

# -------- entrada del programa --------

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Uso: python analizador_edades.py archivo.csv")
        sys.exit()

    archivo = sys.argv[1]

    analizar_archivo(archivo)