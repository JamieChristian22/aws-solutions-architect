# QuickSight Dashboard Ideas

Recommended visuals:
- Temperature over time by device_id
- Count of anomalies per hour (TEMP_SPIKE, VIBRATION_SPIKE, LOW_BATTERY)
- Battery health gauge by device
- Table of last known reading + anomaly flag

Steps:
1. In QuickSight, create a new Athena data source.
2. Choose workgroup `iot-wg`.
3. Select database `iot_telemetry` and table `readings`.
4. Import into SPICE for fast dashboards (optional).
