from numpy import float64
import pandas as pd
import pandera.pandas as pa
from pandera.typing.pandas import Series

class MarketModel(pa.DataFrameModel):
    date: Series[pd.Timestamp] = pa.Field(coerce=True)
    company: Series[str]
    market_cap_m: Series[int] = pa.Field(ge=0, coerce=True)
    price: Series[float64] = pa.Field(gt=0.0, coerce=True)
    
    class Config(pa.DataFrameModel.Config):
        strict = True