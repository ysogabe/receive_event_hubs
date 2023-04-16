# Azure Event Hubs Receiver with InfluxDB Integration For MAMORIO BLE Beacon

[BLE MAMORIO Scanner and Azure Event Hubs Sender](https://github.com/ysogabe/mmtr)のデータをAzure Event Hubsからイベントを受信し、InfluxDBに保存する方法を説明します。


## 前提条件

- Python 3.7以上がインストールされていること
- `azure-eventhub`, `python-dotenv`, `influxdb-client`パッケージがインストールされていること
- `.env`ファイルにEvent Hubsの接続文字列およびInfluxDBの設定が入力されていること

## 使用方法

1. 次のコマンドを実行して、必要なPythonパッケージをインストールします。

   ```
   pip install azure-eventhub python-dotenv influxdb-client
   ```

2. `.env`ファイルに、Event Hubsの接続文字列とInfluxDBの設定を設定します。

   ```
   EVENTHUB_CONNECTION_STRING=<Your_Event_Hubs_Connection_String>
   EVENTHUB_NAME=<Your_Event_hub_name>
   INFLUXDB_URL=<Your_InfluxDB_URL>
   INFLUXDB_TOKEN=<Your_InfluxDB_Token>
   INFLUXDB_ORG=<Your_InfluxDB_Organization>
   INFLUXDB_BUCKET=<Your_InfluxDB_Bucket>
   ```

3. ターミナルで次のコマンドを実行して、イベント受信およびデータ保存を開始します。

   ```
   python event_hubs_receiver.py
   ```

これで、イベント受信スクリプトがAzure Event Hubsからイベントを受信し、それらをInfluxDBに保存します。 

# InfluxDB Docker Setup

上記のスクリプトと連携させるため、InfluxDBをDockerを使用してセットアップする方法も説明します。

## 前提条件

- Dockerがインストールされていること

## 手順

1. ターミナル（コマンドプロンプトやPowerShell）で以下のコマンドを実行して、InfluxDBイメージを取得します。

   ```
   docker pull influxdb:latest
   ```

2. 以下のコマンドを実行して、InfluxDBコンテナを起動します。これにより、InfluxDBがポート`8086`でリッスンします。

   ```
   docker run -p 8086:8086 -v influxdb:/var/lib/influxdb2 -e INFLUXDB_REPORTING_DISABLED=true -e DOCKER_INFLUXDB_INIT_MODE=setup -e DOCKER_INFLUXDB_INIT_USERNAME=<YOUR_USERNAME> -e DOCKER_INFLUXDB_INIT_PASSWORD=<YOUR_PASSWORD> -e DOCKER_INFLUXDB_INIT_ORG=<YOUR_ORG> -e DOCKER_INFLUXDB_INIT_BUCKET=<YOUR_BUCKET> --name influxdb influxdb:latest
   ```

   `<YOUR_USERNAME>`、`<YOUR_PASSWORD>`、`<YOUR_ORG>`、および`<YOUR_BUCKET>`を適切な値に置き換えてください。

3. コンテナが正常に起動したことを確認するために、ターミナルで以下のコマンドを実行します。

   ```
   docker logs influxdb
   ```

   InfluxDBの起動に成功すれば、ログに"Listening on http://[::]:8086"のようなメッセージが表示されます。
