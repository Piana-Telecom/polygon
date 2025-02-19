import ezdxf as ez
from ezdxf.layouts.layout import Modelspace
import pandas as pd

def draw_availability(msp : Modelspace, df : pd.DataFrame):
    assert 'situação' in df.columns
    assert 'sad_x' in df.columns
    assert 'sad_y' in df.columns

    for _, row in df.iterrows():
        color = None
        center = (row['sad_x'], row['sad_y'])
        situacao = row['situação']
        match situacao:
            case 'Disponível':
                color = 3
            case 'Possível disponibilidade':
                color = 2
            case 'Indisponível':
                color = 1
            case _:
                color = 6
        msp.add_circle(
            center,
            3,
            dxfattribs={
                'layer' : 'availability',
                'color' : color
            }
        )

def draw_ownership(msp : Modelspace, df : pd.DataFrame):
    assert 'sad_x' in df.columns
    assert 'sad_y' in df.columns

    for _, row in df.iterrows():
        center = (row['sad_x'], row['sad_y'])
        msp.add_circle(
            center,
            4,
            dxfattribs={
                'layer' : 'ownership',
                'color' : 4
            }
        )

if __name__ == "__main__":
    doc = ez.new()
    msp = doc.modelspace()

    availability = 'CES_availability_2024_10_09_16_41_36_447858'
    ownership = ''

    if availability and availability != '':
        aval_df = pd.read_excel(f'{availability}.xlsx')
        draw_availability(msp, aval_df)
    if ownership and ownership != '':
        owned_df = pd.read_excel(f'{ownership}.xlsx')
        draw_ownership(msp, owned_df)

    doc.saveas('draw_points.dxf')
