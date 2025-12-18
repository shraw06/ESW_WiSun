# Code Structure

Directory Structure:

```
Code/
├─ coap_to_thingspeak.py
│   └─ (script) Bridge CoAP sensor messages to ThingSpeak for cloud logging.
├─ bootloader-storage-spiflash-single-1024k/
│   └─ Bootloader for a single 1MB SPI flash configuration, which was required to be flashed onto the module for  initialising the module for node-monitoring-project.
├─ linux-border-router/
│   ├─ mbedtls/
│   │   └─ Crypto/TLS support used by the border router and related components.
│   ├─ wisun-br-linux/
│   │   └─ Linux-side Wi‑SUN border router implementation and build/config files, this was run on a pc to run the border router.
│   └─ wisun_rcp/
│       └─ Radio Co-Processor (RCP) firmware/tools used with the border router. This was flashed onto the module to configure it as a border router.
└─ wisun_node_monitoring_6_20Novm_OFDM/
	└─ Wi‑SUN node monitoring project (OFDM variant) including node tools and scripts, including sensor (si7021) integration with addition of extra coap resources and endpoints.
```


