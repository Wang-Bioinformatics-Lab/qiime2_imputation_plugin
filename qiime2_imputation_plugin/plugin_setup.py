import qiime2
import biom
import qiime2.plugin
import pandas as pd
import numpy as np
from biom import Table
from q2_types.feature_table import FeatureTable, RelativeFrequency, Frequency


def imputation_function(input_artifact: biom.Table) -> biom.Table:
    # Convert biom.Table to pandas DataFrame
    df = input_artifact.to_dataframe(dense=True)

    cutoff_LOD = round(df.replace(0, np.nan).min(numeric_only=True).min())

    # Perform mean imputation
    df_imputed = df.apply(lambda x: [np.random.randint(1, cutoff_LOD) if v == 0 else v for v in x])

    table_imputed = biom.Table(df_imputed.values, observation_ids=df_imputed.index.tolist(), sample_ids=df_imputed.columns.tolist())


    return table_imputed

plugin = qiime2.plugin.Plugin(
    name='imputation_plugin',
    version='0.1.0',
    website='https://github.com/pluckySquid/qiime2_imputation_plugin.git',
    package='qiime2_imputation_plugin',
    description='A QIIME 2 plugin for qiime2_imputation_plugin functions.',
    short_description='Plugin for qiime2_imputation_plugin analysis.',
)

plugin.methods.register_function(
    function=imputation_function,
    inputs={'input_artifact': FeatureTable[Frequency]},
    parameters={},  # Add parameters if necessary
    outputs=[('output_artifact', FeatureTable[RelativeFrequency])],
    output_descriptions={
        'output_artifact': 'Description of the output artifact.'
    },
    name='dummy-function',
    description='A description of your function.',
)