import pandas as pd
from influxdb_client_3 import InfluxDBClient3, flight_client_options
import certifi


def import_database(token_in, org_in, host_in, query_in, database_in):
    # Need to specify the root certificate in non-POSIX-compliant systems
    fh = open(certifi.where(), "r")
    cert = fh.read()
    fh.close()

    client = InfluxDBClient3(host=host_in, token=token_in, org=org_in,
                             flight_client_options=flight_client_options(tls_root_certs=cert))
    table = client.query(query=query_in, database=database_in, language="sql")

    global df
    df = table.to_pandas().sort_values(by="time")


def export_to_csv(output_file):
    file = output_file

    # Add .csv to end of filename if it does not already exist.
    if file[-4:].lower() != ".csv":
        file += ".csv"

    global df
    df.to_csv(file)


df = pd.DataFrame()

token = "Placeholder"

org = "Xor Interview Task"
host = "https://eu-central-1-1.aws.cloud2.influxdata.com"

query = """SELECT *
FROM 'airSensors'"""

database = "test_data"

import_database(token, org, host, query, database)
export_to_csv(output_file="test")
