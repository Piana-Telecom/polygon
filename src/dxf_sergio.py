import ezdxf as ez
import pandas as pd
import traceback

try:
    df = pd.DataFrame(columns=['pole_id'])
    doc = ez.readfile(f'{input('nome do arquivo sem extensão : ')}.dxf')
    for entity in doc.entities:
        if entity.dxftype() == "MTEXT":
            print(entity.dxf.text)
            df.loc[len(df)] = [entity.dxf.text]
    df.to_excel('planilha_sergio.xlsx')
except:
    print(traceback.format_exc())
    input('UwU')
