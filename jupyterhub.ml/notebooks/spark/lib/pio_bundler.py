from pyspark.ml.common import _py2java
from pyspark.ml import PipelineModel
import dill as pickle

def bundle(spark_session, spark_df_schema, spark_pipeline_model):
    #spark_df_as_java = _py2java(spark_session, spark_df)
    #spark_df_schema_as_java = spark_df_as_java.schema.__call__()
    spark_df_schema_as_json = spark_df_schema.json()
    with open('model.schema', 'wb') as pkl_file:
        pickle.dump(spark_df_schema_as_json, pkl_file)

    spark_pipeline_model.write().overwrite().save('model.parquet')
    
    ## SERVE FROM HERE
    with open('model.schema', 'rb') as pkl_file:
       from pyspark.sql.types import _parse_datatype_json_string
       restored_spark_df_schema_as_json = pickle.load(pkl_file)
       restored_spark_df_schema = _parse_datatype_json_string(restored_spark_df_schema_as_json)
       restored_spark_df_schema_as_java = _py2java(spark_session, restored_spark_df_schema)
 
    restored_spark_pipeline_model = PipelineModel.read().load('model.parquet')
    restored_spark_pipeline_model_as_java = restored_spark_pipeline_model._to_java()
    
    return spark_session._jvm.org.jpmml.sparkml.ConverterUtil.toPMMLByteArray(restored_spark_df_schema_as_java, 
                                                                              restored_spark_pipeline_model_as_java)

