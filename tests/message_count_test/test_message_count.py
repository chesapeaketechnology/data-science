import pytest
import json
import os
from subprocess import Popen, run
import time
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import Row, SparkSession
from pyspark.sql.functions import col


result = []
topic = os.path.basename(__file__).split(sep=".")[0]


def enqueue_records():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    src_props = dir_path + "/connect-file-source.properties"
    run([
        "sed",
        "-i",
        "s|file=.*|file=" + dir_path + "/ten.recs|",
        src_props
    ])
    proc = Popen([
        "/usr/local/kafka/bin/connect-standalone.sh",
        "/etc/kafka/connect-standalone.properties",
        src_props
    ], shell=False, stdin=None, stdout=None, close_fds=True)

    time.sleep(250)  # make sure kafka connector is up and running


def cleanup(proc):
#    os.remove("data.txt")
    Popen.kill(proc)
    Popen([
        "sudo",
        "/usr/local/kafka/bin/kafka-topics.sh",
        "--zookepper",
        " localhost:2128",
        "--topic",
        topic,
        "--delete"
    ], shell=False, stdin=None, stdout=None, close_fds=True)


def getSparkSessionInstance(sparkConf):
    if 'sparkSessionSingletonInstance' not in globals():
        globals()['sparkSessionSingletonInstance'] = SparkSession\
            .builder\
            .config(conf=sparkConf)\
            .getOrCreate()
    return globals()['sparkSessionSingletonInstance']


def process(_, rdd):
    spark = getSparkSessionInstance(rdd.context.getConf())

    row_rdd = rdd.map(lambda c: Row(cnt=c))
    count_df = spark.createDataFrame(row_rdd)

    res = count_df.select(col("cnt"))
    result.append(res.first()[0])


def create_input_data_file():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/ten.recs", "w") as f:
        f.writelines([
            """
            {u'payload': {u'contentType': u'', u'sequenceNumber': 144804, u'systemProperties': {u'content-type': u'UTF-8', u'correlation-id': u'a00392cc-33d9-49ba-a002-611eb0b98f97', u'iothub-connection-auth-generation-id': u'637200783617776331', u'iothub-message-source': u'Telemetry', u'iothub-connection-auth-method': u'{"scope":"device","type":"sas","issuer":"iothub","acceptingIpFilterRule":null}', u'message-id': u'825', u'iothub-enqueuedtime': u'Thu Mar 26 19:59:01 UTC 2020'}, u'enqueuedTime': u'2020-03-26T19:59:01.933Z', u'content': u'# com.craxiom.networksurvey.messaging.LteRecord@2379069c\ndevice_serial_number: "2865542af3ff5771"\ndevice_time: 1585252742294\nearfcn {\n  value: 2325\n}\ngroup_number: 266\nmission_id: "NS 2865542af3ff5771 20200326-125004"\npci {\n  value: 96\n}\nrecord_number: 825\nrsrp {\n  value: -102.0\n}\nrsrq {\n  value: -13.0\n}\nserving_cell {\n}', u'deviceId': u'DinosPixel', u'offset': u'12903011056', u'properties': {u'temperatureAlert': u'false', u'$.cdid': u'DinosPixel'}}, u'schema': {u'fields': [{u'type': u'string', u'optional': False, u'field': u'deviceId'}, {u'type': u'string', u'optional': False, u'field': u'offset'}, {u'type': u'string', u'optional': True, u'field': u'contentType'}, {u'type': u'string', u'optional': False, u'field': u'enqueuedTime'}, {u'type': u'int64', u'optional': False, u'field': u'sequenceNumber'}, {u'type': u'string', u'optional': False, u'field': u'content'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'systemProperties'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'properties'}], u'version': 1, u'type': u'struct', u'name': u'iothub.kafka.connect', u'optional': False}}
            {u'payload': {u'contentType': u'', u'sequenceNumber': 144805, u'systemProperties': {u'content-type': u'UTF-8', u'correlation-id': u'9a707024-a14e-441d-93ae-6a93560b216c', u'iothub-connection-auth-generation-id': u'637200783617776331', u'iothub-message-source': u'Telemetry', u'iothub-connection-auth-method': u'{"scope":"device","type":"sas","issuer":"iothub","acceptingIpFilterRule":null}', u'message-id': u'827', u'iothub-enqueuedtime': u'Thu Mar 26 19:59:03 UTC 2020'}, u'enqueuedTime': u'2020-03-26T19:59:03.981Z', u'content': u'# com.craxiom.networksurvey.messaging.LteRecord@7ff4ba9b\nci {\n  value: 14040608\n}\ndevice_serial_number: "2865542af3ff5771"\ndevice_time: 1585252744254\nearfcn {\n  value: 2325\n}\ngroup_number: 267\nmcc {\n  value: 311\n}\nmission_id: "NS 2865542af3ff5771 20200326-125004"\nmnc {\n  value: 480\n}\npci {\n  value: 161\n}\nrecord_number: 827\nrsrp {\n  value: -96.0\n}\nrsrq {\n  value: -7.0\n}\nserving_cell {\n  value: true\n}\ntac {\n  value: 13826\n}', u'deviceId': u'DinosPixel', u'offset': u'12903011840', u'properties': {u'temperatureAlert': u'false', u'$.cdid': u'DinosPixel'}}, u'schema': {u'fields': [{u'type': u'string', u'optional': False, u'field': u'deviceId'}, {u'type': u'string', u'optional': False, u'field': u'offset'}, {u'type': u'string', u'optional': True, u'field': u'contentType'}, {u'type': u'string', u'optional': False, u'field': u'enqueuedTime'}, {u'type': u'int64', u'optional': False, u'field': u'sequenceNumber'}, {u'type': u'string', u'optional': False, u'field': u'content'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'systemProperties'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'properties'}], u'version': 1, u'type': u'struct', u'name': u'iothub.kafka.connect', u'optional': False}}
            {u'payload': {u'contentType': u'', u'sequenceNumber': 144806, u'systemProperties': {u'content-type': u'UTF-8', u'correlation-id': u'62505b84-c3d5-4b61-bcaa-897326ca985f', u'iothub-connection-auth-generation-id': u'637200783617776331', u'iothub-message-source': u'Telemetry', u'iothub-connection-auth-method': u'{"scope":"device","type":"sas","issuer":"iothub","acceptingIpFilterRule":null}', u'message-id': u'828', u'iothub-enqueuedtime': u'Thu Mar 26 19:59:03 UTC 2020'}, u'enqueuedTime': u'2020-03-26T19:59:03.981Z', u'content': u'# com.craxiom.networksurvey.messaging.LteRecord@a37b6d30\ndevice_serial_number: "2865542af3ff5771"\ndevice_time: 1585252744282\nearfcn {\n  value: 2325\n}\ngroup_number: 267\nmission_id: "NS 2865542af3ff5771 20200326-125004"\npci {\n  value: 96\n}\nrecord_number: 828\nrsrp {\n  value: -102.0\n}\nrsrq {\n  value: -12.0\n}\nserving_cell {\n}', u'deviceId': u'DinosPixel', u'offset': u'12903012720', u'properties': {u'temperatureAlert': u'false', u'$.cdid': u'DinosPixel'}}, u'schema': {u'fields': [{u'type': u'string', u'optional': False, u'field': u'deviceId'}, {u'type': u'string', u'optional': False, u'field': u'offset'}, {u'type': u'string', u'optional': True, u'field': u'contentType'}, {u'type': u'string', u'optional': False, u'field': u'enqueuedTime'}, {u'type': u'int64', u'optional': False, u'field': u'sequenceNumber'}, {u'type': u'string', u'optional': False, u'field': u'content'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'systemProperties'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'properties'}], u'version': 1, u'type': u'struct', u'name': u'iothub.kafka.connect', u'optional': False}}
            {u'payload': {u'contentType': u'', u'sequenceNumber': 144807, u'systemProperties': {u'content-type': u'UTF-8', u'correlation-id': u'0da6ce2d-67fe-4e11-ad8b-42198745425e', u'iothub-connection-auth-generation-id': u'637200783617776331', u'iothub-message-source': u'Telemetry', u'iothub-connection-auth-method': u'{"scope":"device","type":"sas","issuer":"iothub","acceptingIpFilterRule":null}', u'message-id': u'830', u'iothub-enqueuedtime': u'Thu Mar 26 19:59:05 UTC 2020'}, u'enqueuedTime': u'2020-03-26T19:59:06.036Z', u'content': u'# com.craxiom.networksurvey.messaging.LteRecord@2298da8b\nci {\n  value: 14040608\n}\ndevice_serial_number: "2865542af3ff5771"\ndevice_time: 1585252746286\nearfcn {\n  value: 2325\n}\ngroup_number: 268\nmcc {\n  value: 311\n}\nmission_id: "NS 2865542af3ff5771 20200326-125004"\nmnc {\n  value: 480\n}\npci {\n  value: 161\n}\nrecord_number: 830\nrsrp {\n  value: -96.0\n}\nrsrq {\n  value: -8.0\n}\nserving_cell {\n  value: true\n}\ntac {\n  value: 13826\n}', u'deviceId': u'DinosPixel', u'offset': u'12903013504', u'properties': {u'temperatureAlert': u'false', u'$.cdid': u'DinosPixel'}}, u'schema': {u'fields': [{u'type': u'string', u'optional': False, u'field': u'deviceId'}, {u'type': u'string', u'optional': False, u'field': u'offset'}, {u'type': u'string', u'optional': True, u'field': u'contentType'}, {u'type': u'string', u'optional': False, u'field': u'enqueuedTime'}, {u'type': u'int64', u'optional': False, u'field': u'sequenceNumber'}, {u'type': u'string', u'optional': False, u'field': u'content'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'systemProperties'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'properties'}], u'version': 1, u'type': u'struct', u'name': u'iothub.kafka.connect', u'optional': False}}
            {u'payload': {u'contentType': u'', u'sequenceNumber': 144808, u'systemProperties': {u'content-type': u'UTF-8', u'correlation-id': u'd09c3d02-abbe-4e51-867a-5fef87c18ac9', u'iothub-connection-auth-generation-id': u'637200783617776331', u'iothub-message-source': u'Telemetry', u'iothub-connection-auth-method': u'{"scope":"device","type":"sas","issuer":"iothub","acceptingIpFilterRule":null}', u'message-id': u'831', u'iothub-enqueuedtime': u'Thu Mar 26 19:59:05 UTC 2020'}, u'enqueuedTime': u'2020-03-26T19:59:06.036Z', u'content': u'# com.craxiom.networksurvey.messaging.LteRecord@d85f3d6b\ndevice_serial_number: "2865542af3ff5771"\ndevice_time: 1585252746307\nearfcn {\n  value: 2325\n}\ngroup_number: 268\nmission_id: "NS 2865542af3ff5771 20200326-125004"\npci {\n  value: 96\n}\nrecord_number: 831\nrsrp {\n  value: -102.0\n}\nrsrq {\n  value: -13.0\n}\nserving_cell {\n}', u'deviceId': u'DinosPixel', u'offset': u'12903014384', u'properties': {u'temperatureAlert': u'false', u'$.cdid': u'DinosPixel'}}, u'schema': {u'fields': [{u'type': u'string', u'optional': False, u'field': u'deviceId'}, {u'type': u'string', u'optional': False, u'field': u'offset'}, {u'type': u'string', u'optional': True, u'field': u'contentType'}, {u'type': u'string', u'optional': False, u'field': u'enqueuedTime'}, {u'type': u'int64', u'optional': False, u'field': u'sequenceNumber'}, {u'type': u'string', u'optional': False, u'field': u'content'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'systemProperties'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'properties'}], u'version': 1, u'type': u'struct', u'name': u'iothub.kafka.connect', u'optional': False}}
            {u'payload': {u'contentType': u'', u'sequenceNumber': 144809, u'systemProperties': {u'content-type': u'UTF-8', u'correlation-id': u'6e7b061c-3ed6-40eb-83b9-c6448ee9b04f', u'iothub-connection-auth-generation-id': u'637200783617776331', u'iothub-message-source': u'Telemetry', u'iothub-connection-auth-method': u'{"scope":"device","type":"sas","issuer":"iothub","acceptingIpFilterRule":null}', u'message-id': u'833', u'iothub-enqueuedtime': u'Thu Mar 26 19:59:07 UTC 2020'}, u'enqueuedTime': u'2020-03-26T19:59:08.068Z', u'content': u'# com.craxiom.networksurvey.messaging.LteRecord@7014afe1\nci {\n  value: 14040608\n}\ndevice_serial_number: "2865542af3ff5771"\ndevice_time: 1585252748316\nearfcn {\n  value: 2325\n}\ngroup_number: 269\nmcc {\n  value: 311\n}\nmission_id: "NS 2865542af3ff5771 20200326-125004"\nmnc {\n  value: 480\n}\npci {\n  value: 161\n}\nrecord_number: 833\nrsrp {\n  value: -95.0\n}\nrsrq {\n  value: -7.0\n}\nserving_cell {\n  value: true\n}\ntac {\n  value: 13826\n}', u'deviceId': u'DinosPixel', u'offset': u'12903015168', u'properties': {u'temperatureAlert': u'false', u'$.cdid': u'DinosPixel'}}, u'schema': {u'fields': [{u'type': u'string', u'optional': False, u'field': u'deviceId'}, {u'type': u'string', u'optional': False, u'field': u'offset'}, {u'type': u'string', u'optional': True, u'field': u'contentType'}, {u'type': u'string', u'optional': False, u'field': u'enqueuedTime'}, {u'type': u'int64', u'optional': False, u'field': u'sequenceNumber'}, {u'type': u'string', u'optional': False, u'field': u'content'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'systemProperties'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'properties'}], u'version': 1, u'type': u'struct', u'name': u'iothub.kafka.connect', u'optional': False}}
            {u'payload': {u'contentType': u'', u'sequenceNumber': 144810, u'systemProperties': {u'content-type': u'UTF-8', u'correlation-id': u'3df5b093-91f9-45ff-989d-af4838807497', u'iothub-connection-auth-generation-id': u'637200783617776331', u'iothub-message-source': u'Telemetry', u'iothub-connection-auth-method': u'{"scope":"device","type":"sas","issuer":"iothub","acceptingIpFilterRule":null}', u'message-id': u'834', u'iothub-enqueuedtime': u'Thu Mar 26 19:59:08 UTC 2020'}, u'enqueuedTime': u'2020-03-26T19:59:08.068Z', u'content': u'# com.craxiom.networksurvey.messaging.LteRecord@bb2ecd42\ndevice_serial_number: "2865542af3ff5771"\ndevice_time: 1585252748340\nearfcn {\n  value: 2325\n}\ngroup_number: 269\nmission_id: "NS 2865542af3ff5771 20200326-125004"\npci {\n  value: 96\n}\nrecord_number: 834\nrsrp {\n  value: -101.0\n}\nrsrq {\n  value: -11.0\n}\nserving_cell {\n}', u'deviceId': u'DinosPixel', u'offset': u'12903016048', u'properties': {u'temperatureAlert': u'false', u'$.cdid': u'DinosPixel'}}, u'schema': {u'fields': [{u'type': u'string', u'optional': False, u'field': u'deviceId'}, {u'type': u'string', u'optional': False, u'field': u'offset'}, {u'type': u'string', u'optional': True, u'field': u'contentType'}, {u'type': u'string', u'optional': False, u'field': u'enqueuedTime'}, {u'type': u'int64', u'optional': False, u'field': u'sequenceNumber'}, {u'type': u'string', u'optional': False, u'field': u'content'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'systemProperties'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'properties'}], u'version': 1, u'type': u'struct', u'name': u'iothub.kafka.connect', u'optional': False}}
            {u'payload': {u'contentType': u'', u'sequenceNumber': 144811, u'systemProperties': {u'content-type': u'UTF-8', u'correlation-id': u'771e42ce-41cd-4da8-a7de-cd203f821a0d', u'iothub-connection-auth-generation-id': u'637200783617776331', u'iothub-message-source': u'Telemetry', u'iothub-connection-auth-method': u'{"scope":"device","type":"sas","issuer":"iothub","acceptingIpFilterRule":null}', u'message-id': u'836', u'iothub-enqueuedtime': u'Thu Mar 26 19:59:09 UTC 2020'}, u'enqueuedTime': u'2020-03-26T19:59:10.109Z', u'content': u'# com.craxiom.networksurvey.messaging.LteRecord@923b8320\nci {\n  value: 14040608\n}\ndevice_serial_number: "2865542af3ff5771"\ndevice_time: 1585252750329\nearfcn {\n  value: 2325\n}\ngroup_number: 270\nmcc {\n  value: 311\n}\nmission_id: "NS 2865542af3ff5771 20200326-125004"\nmnc {\n  value: 480\n}\npci {\n  value: 161\n}\nrecord_number: 836\nrsrp {\n  value: -97.0\n}\nrsrq {\n  value: -7.0\n}\nserving_cell {\n  value: true\n}\ntac {\n  value: 13826\n}', u'deviceId': u'DinosPixel', u'offset': u'12903016832', u'properties': {u'temperatureAlert': u'false', u'$.cdid': u'DinosPixel'}}, u'schema': {u'fields': [{u'type': u'string', u'optional': False, u'field': u'deviceId'}, {u'type': u'string', u'optional': False, u'field': u'offset'}, {u'type': u'string', u'optional': True, u'field': u'contentType'}, {u'type': u'string', u'optional': False, u'field': u'enqueuedTime'}, {u'type': u'int64', u'optional': False, u'field': u'sequenceNumber'}, {u'type': u'string', u'optional': False, u'field': u'content'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'systemProperties'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'properties'}], u'version': 1, u'type': u'struct', u'name': u'iothub.kafka.connect', u'optional': False}}
            {u'payload': {u'contentType': u'', u'sequenceNumber': 144812, u'systemProperties': {u'content-type': u'UTF-8', u'correlation-id': u'7ca99170-ee6c-4501-a3ad-8c0e2a91dc19', u'iothub-connection-auth-generation-id': u'637200783617776331', u'iothub-message-source': u'Telemetry', u'iothub-connection-auth-method': u'{"scope":"device","type":"sas","issuer":"iothub","acceptingIpFilterRule":null}', u'message-id': u'837', u'iothub-enqueuedtime': u'Thu Mar 26 19:59:10 UTC 2020'}, u'enqueuedTime': u'2020-03-26T19:59:10.109Z', u'content': u'# com.craxiom.networksurvey.messaging.LteRecord@c8a5d21b\ndevice_serial_number: "2865542af3ff5771"\ndevice_time: 1585252750355\nearfcn {\n  value: 2325\n}\ngroup_number: 270\nmission_id: "NS 2865542af3ff5771 20200326-125004"\npci {\n  value: 96\n}\nrecord_number: 837\nrsrp {\n  value: -100.0\n}\nrsrq {\n  value: -9.0\n}\nserving_cell {\n}', u'deviceId': u'DinosPixel', u'offset': u'12903017712', u'properties': {u'temperatureAlert': u'false', u'$.cdid': u'DinosPixel'}}, u'schema': {u'fields': [{u'type': u'string', u'optional': False, u'field': u'deviceId'}, {u'type': u'string', u'optional': False, u'field': u'offset'}, {u'type': u'string', u'optional': True, u'field': u'contentType'}, {u'type': u'string', u'optional': False, u'field': u'enqueuedTime'}, {u'type': u'int64', u'optional': False, u'field': u'sequenceNumber'}, {u'type': u'string', u'optional': False, u'field': u'content'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'systemProperties'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'properties'}], u'version': 1, u'type': u'struct', u'name': u'iothub.kafka.connect', u'optional': False}}
            {u'payload': {u'contentType': u'', u'sequenceNumber': 144813, u'systemProperties': {u'content-type': u'UTF-8', u'correlation-id': u'0380dd55-ad52-4c67-a5a4-cc53ebbdb8e5', u'iothub-connection-auth-generation-id': u'637200783617776331', u'iothub-message-source': u'Telemetry', u'iothub-connection-auth-method': u'{"scope":"device","type":"sas","issuer":"iothub","acceptingIpFilterRule":null}', u'message-id': u'839', u'iothub-enqueuedtime': u'Thu Mar 26 19:59:11 UTC 2020'}, u'enqueuedTime': u'2020-03-26T19:59:11.953Z', u'content': u'# com.craxiom.networksurvey.messaging.LteRecord@a80ff2c5\nci {\n  value: 14040608\n}\ndevice_serial_number: "2865542af3ff5771"\ndevice_time: 1585252752336\nearfcn {\n  value: 2325\n}\ngroup_number: 271\nmcc {\n  value: 311\n}\nmission_id: "NS 2865542af3ff5771 20200326-125004"\nmnc {\n  value: 480\n}\npci {\n  value: 161\n}\nrecord_number: 839\nrsrp {\n  value: -97.0\n}\nrsrq {\n  value: -8.0\n}\nserving_cell {\n  value: true\n}\ntac {\n  value: 13826\n}', u'deviceId': u'DinosPixel', u'offset': u'12903018488', u'properties': {u'temperatureAlert': u'false', u'$.cdid': u'DinosPixel'}}, u'schema': {u'fields': [{u'type': u'string', u'optional': False, u'field': u'deviceId'}, {u'type': u'string', u'optional': False, u'field': u'offset'}, {u'type': u'string', u'optional': True, u'field': u'contentType'}, {u'type': u'string', u'optional': False, u'field': u'enqueuedTime'}, {u'type': u'int64', u'optional': False, u'field': u'sequenceNumber'}, {u'type': u'string', u'optional': False, u'field': u'content'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'systemProperties'}, {u'keys': {u'type': u'string', u'optional': False}, u'type': u'map', u'values': {u'type': u'string', u'optional': False}, u'optional': False, u'field': u'properties'}], u'version': 1, u'type': u'struct', u'name': u'iothub.kafka.connect', u'optional': False}}
            """
        ])


@pytest.mark.usefixtures("streaming_context")
def test_message_count(streaming_context):
    create_input_data_file()

    proc = enqueue_records()


    kafka_stream = \
        KafkaUtils.createDirectStream(
            streaming_context,
            ["test_message_count"],
            {
                "metadata.broker.list": "localhost:9092",
                "auto.offset.reset": "smallest",
            }
        )

    parsed = kafka_stream.map(lambda v: json.loads(v[1]))
    parsed.count().foreachRDD(process)

    streaming_context.start()

    timeout = 25
    start_time = time.time()
    while sum(result) < 10 and time.time() - start_time < timeout:
        time.sleep(0.1)

    # cleanup(proc)
    assert sum(result) == 10
