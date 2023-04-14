import os
import json
import threading
from datetime import datetime
from dotenv import load_dotenv
from azure.eventhub import EventHubConsumerClient
from influxdb_client import InfluxDBClient, Point, WritePrecision

load_dotenv()

# InfluxDB settings
influxdb_url = os.environ["INFLUXDB_URL"]
influxdb_token = os.environ["INFLUXDB_TOKEN"]
influxdb_org = os.environ["INFLUXDB_ORG"]
influxdb_bucket = os.environ["INFLUXDB_BUCKET"]

# Initialize InfluxDB client
influxdb_client = InfluxDBClient(url=influxdb_url, token=influxdb_token)

def on_event(partition_context, event):
    """
    イベントを処理するコールバック関数

    :param partition_context: パーティションコンテキスト
    :type partition_context: azure.eventhub.aio.PartitionContext
    :param event: 受信イベント
    :type event: azure.eventhub.EventData
    """

    #print(f"Received event from partition {partition_context.partition_id}: {event.body_as_str()}")

    # Parse JSON data
    try:
        json_data = json.loads(event.body_as_str())
        # Prepare data as InfluxDB point
        data = Point("event_data") \
            .tag("MAMORIO", json_data["MAMORIO"]) \
            .field("RSSI", json_data["RSSI"]) \
            .tag("Hostname", json_data["Hostname"]) \
            .time(datetime.fromisoformat(json_data["Time"]), WritePrecision.NS)

        # Write data to InfluxDB
        with influxdb_client.write_api() as write_api:
            write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=data)
    except Exception as e:
        print(f"Error occurred in handleDiscovery: {e}")
    partition_context.update_checkpoint(event)


def receive_events(connection_string, event_hub_name):
    """
    Azure Event Hubsからイベントを受信する

    :param connection_string: 接続文字列
    :type connection_string: str
    :param event_hub_name: イベントハブ名
    :type event_hub_name: str
    """

   #print(f"[{connection_string}]")
    client = EventHubConsumerClient.from_connection_string(
        conn_str=connection_string,
        consumer_group='$Default',
        eventhub_name=event_hub_name,
    )

    try:
        with client:
            client.receive(on_event=on_event,
               starting_position="-1",)
    except KeyboardInterrupt:
        print("Stopped receiving events.")


if __name__ == "__main__":
    connection_string = os.environ["EVENTHUB_CONNECTION_STRING"]
    event_hub_name = "mmtr"

    #print(f"[{connection_string }]")

    # スレッドでイベント受信を開始
    receive_thread = threading.Thread(target=receive_events, args=(connection_string, event_hub_name))
    receive_thread.start()
    receive_thread.join()
