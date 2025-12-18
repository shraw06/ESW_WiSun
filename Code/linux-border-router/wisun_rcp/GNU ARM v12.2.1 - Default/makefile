################################################################################
# Automatically-generated file. Do not edit!
################################################################################

-include ../makefile.init

RM := rm -rf

# All of the sources participating in the build are defined here
-include sources.mk
-include simplicity_sdk_2024.6.2/util/third_party/segger/systemview/SEGGER/subdir.mk
-include simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/subdir.mk
-include simplicity_sdk_2024.6.2/util/third_party/freertos/kernel/portable/MemMang/subdir.mk
-include simplicity_sdk_2024.6.2/util/third_party/freertos/kernel/portable/GCC/ARM_CM33_NTZ/non_secure/subdir.mk
-include simplicity_sdk_2024.6.2/util/third_party/freertos/kernel/subdir.mk
-include simplicity_sdk_2024.6.2/util/third_party/freertos/cmsis/Source/subdir.mk
-include simplicity_sdk_2024.6.2/protocol/wisun/app/wisun_rcp/subdir.mk
-include simplicity_sdk_2024.6.2/platform/service/system/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/service/sleeptimer/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/service/memory_manager/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/service/iostream/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/service/interrupt_manager/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/service/device_manager/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/service/device_manager/devices/subdir.mk
-include simplicity_sdk_2024.6.2/platform/service/device_manager/clocks/subdir.mk
-include simplicity_sdk_2024.6.2/platform/service/device_init/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/service/clock_manager/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/security/sl_component/sl_mbedtls_support/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/security/sl_component/se_manager/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/radio/rail_lib/plugin/rail_util_rf_path_switch/subdir.mk
-include simplicity_sdk_2024.6.2/platform/radio/rail_lib/plugin/rail_util_pti/subdir.mk
-include simplicity_sdk_2024.6.2/platform/radio/rail_lib/plugin/pa-conversions/subdir.mk
-include simplicity_sdk_2024.6.2/platform/peripheral/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/emlib/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/emdrv/nvm3/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/emdrv/dmadrv/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/common/src/subdir.mk
-include simplicity_sdk_2024.6.2/platform/Device/SiliconLabs/EFR32ZG28/Source/subdir.mk
-include simplicity_sdk_2024.6.2/platform/CMSIS/RTOS2/Source/subdir.mk
-include simplicity_sdk_2024.6.2/hardware/board/src/subdir.mk
-include autogen/subdir.mk
-include subdir.mk
-include objects.mk

ifneq ($(MAKECMDGOALS),clean)
ifneq ($(strip $(C_DEPS)),)
-include $(C_DEPS)
endif
endif

-include ../makefile.defs

OPTIONAL_TOOL_DEPS := \
$(wildcard ../makefile.defs) \
$(wildcard ../makefile.init) \
$(wildcard ../makefile.targets) \


BUILD_ARTIFACT_NAME := wisun_rcp
BUILD_ARTIFACT_EXTENSION := axf
BUILD_ARTIFACT_PREFIX :=
BUILD_ARTIFACT := $(BUILD_ARTIFACT_PREFIX)$(BUILD_ARTIFACT_NAME)$(if $(BUILD_ARTIFACT_EXTENSION),.$(BUILD_ARTIFACT_EXTENSION),)

# Add inputs and outputs from these tool invocations to the build variables 

# All Target
all: main-build

# Main-build Target
main-build: wisun_rcp.axf

# Tool invocations
wisun_rcp.axf: $(OBJS) $(USER_OBJS) makefile objects.mk $(OPTIONAL_TOOL_DEPS)
	@echo 'Building target: $@'
	@echo 'Invoking: GNU ARM C Linker'
	arm-none-eabi-gcc -g -gdwarf-2 -mcpu=cortex-m33 -mthumb -T "C:\Users\Shrawani\SimplicityStudio\v5_workspace\wisun_rcp\autogen\linkerfile.ld" -Wl,--wrap=_free_r -Wl,--wrap=_malloc_r -Wl,--wrap=_calloc_r -Wl,--wrap=_realloc_r -Wl,--no-warn-rwx-segments -Xlinker --gc-sections -Xlinker -Map="wisun_rcp.map" -mfpu=fpv5-sp-d16 -mfloat-abi=hard --specs=nano.specs -o wisun_rcp.axf -Wl,--start-group "./autogen/rail_config.o" "./autogen/sl_board_default_init.o" "./autogen/sl_device_init_clocks.o" "./autogen/sl_event_handler.o" "./autogen/sl_iostream_handles.o" "./simplicity_sdk_2024.6.2/hardware/board/src/sl_board_control_gpio.o" "./simplicity_sdk_2024.6.2/hardware/board/src/sl_board_init.o" "./simplicity_sdk_2024.6.2/platform/CMSIS/RTOS2/Source/os_systick.o" "./simplicity_sdk_2024.6.2/platform/Device/SiliconLabs/EFR32ZG28/Source/startup_efr32zg28.o" "./simplicity_sdk_2024.6.2/platform/Device/SiliconLabs/EFR32ZG28/Source/system_efr32zg28.o" "./simplicity_sdk_2024.6.2/platform/common/src/sl_assert.o" "./simplicity_sdk_2024.6.2/platform/common/src/sl_core_cortexm.o" "./simplicity_sdk_2024.6.2/platform/common/src/sl_slist.o" "./simplicity_sdk_2024.6.2/platform/common/src/sl_syscalls.o" "./simplicity_sdk_2024.6.2/platform/common/src/sli_cmsis_os2_ext_task_register.o" "./simplicity_sdk_2024.6.2/platform/emdrv/dmadrv/src/dmadrv.o" "./simplicity_sdk_2024.6.2/platform/emdrv/nvm3/src/nvm3_default_common_linker.o" "./simplicity_sdk_2024.6.2/platform/emdrv/nvm3/src/nvm3_hal_flash.o" "./simplicity_sdk_2024.6.2/platform/emdrv/nvm3/src/nvm3_lock.o" "./simplicity_sdk_2024.6.2/platform/emlib/src/em_burtc.o" "./simplicity_sdk_2024.6.2/platform/emlib/src/em_cmu.o" "./simplicity_sdk_2024.6.2/platform/emlib/src/em_core.o" "./simplicity_sdk_2024.6.2/platform/emlib/src/em_emu.o" "./simplicity_sdk_2024.6.2/platform/emlib/src/em_eusart.o" "./simplicity_sdk_2024.6.2/platform/emlib/src/em_gpio.o" "./simplicity_sdk_2024.6.2/platform/emlib/src/em_ldma.o" "./simplicity_sdk_2024.6.2/platform/emlib/src/em_msc.o" "./simplicity_sdk_2024.6.2/platform/emlib/src/em_prs.o" "./simplicity_sdk_2024.6.2/platform/emlib/src/em_se.o" "./simplicity_sdk_2024.6.2/platform/emlib/src/em_system.o" "./simplicity_sdk_2024.6.2/platform/emlib/src/em_timer.o" "./simplicity_sdk_2024.6.2/platform/emlib/src/em_usart.o" "./simplicity_sdk_2024.6.2/platform/peripheral/src/sl_hal_sysrtc.o" "./simplicity_sdk_2024.6.2/platform/radio/rail_lib/plugin/pa-conversions/pa_conversions_efr32.o" "./simplicity_sdk_2024.6.2/platform/radio/rail_lib/plugin/pa-conversions/pa_curves_efr32.o" "./simplicity_sdk_2024.6.2/platform/radio/rail_lib/plugin/rail_util_pti/sl_rail_util_pti.o" "./simplicity_sdk_2024.6.2/platform/radio/rail_lib/plugin/rail_util_rf_path_switch/sl_rail_util_rf_path_switch.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/se_manager/src/sl_se_manager.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/se_manager/src/sl_se_manager_attestation.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/se_manager/src/sl_se_manager_cipher.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/se_manager/src/sl_se_manager_entropy.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/se_manager/src/sl_se_manager_hash.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/se_manager/src/sl_se_manager_key_derivation.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/se_manager/src/sl_se_manager_key_handling.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/se_manager/src/sl_se_manager_signature.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/se_manager/src/sl_se_manager_util.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/se_manager/src/sli_se_manager_mailbox.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_mbedtls_support/src/mbedtls_ccm.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_mbedtls_support/src/mbedtls_ecdsa_ecdh.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_mbedtls_support/src/mbedtls_sha.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_mbedtls_support/src/se_aes.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_mbedtls_support/src/sl_entropy_hardware.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_mbedtls_support/src/sl_mbedtls.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_mbedtls_support/src/sl_psa_crypto.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_mbedtls_support/src/sli_psa_crypto.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sl_psa_its_nvm3.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_psa_driver_common.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_psa_driver_init.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_psa_trng.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_driver_aead.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_driver_builtin_keys.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_driver_cipher.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_driver_key_derivation.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_driver_key_management.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_driver_mac.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_driver_signature.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_opaque_driver_aead.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_opaque_driver_cipher.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_opaque_driver_mac.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_opaque_key_derivation.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_transparent_driver_aead.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_transparent_driver_cipher.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_transparent_driver_hash.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_transparent_driver_mac.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_transparent_key_derivation.o" "./simplicity_sdk_2024.6.2/platform/security/sl_component/sl_psa_driver/src/sli_se_version_dependencies.o" "./simplicity_sdk_2024.6.2/platform/service/clock_manager/src/sl_clock_manager.o" "./simplicity_sdk_2024.6.2/platform/service/clock_manager/src/sl_clock_manager_hal_s2.o" "./simplicity_sdk_2024.6.2/platform/service/device_init/src/sl_device_init_dcdc_s2.o" "./simplicity_sdk_2024.6.2/platform/service/device_init/src/sl_device_init_emu_s2.o" "./simplicity_sdk_2024.6.2/platform/service/device_init/src/sl_device_init_hfxo_s2.o" "./simplicity_sdk_2024.6.2/platform/service/device_init/src/sl_device_init_lfxo_s2.o" "./simplicity_sdk_2024.6.2/platform/service/device_manager/clocks/sl_device_clock_efr32xg28.o" "./simplicity_sdk_2024.6.2/platform/service/device_manager/devices/sl_device_peripheral_hal_efr32xg28.o" "./simplicity_sdk_2024.6.2/platform/service/device_manager/src/sl_device_clock.o" "./simplicity_sdk_2024.6.2/platform/service/device_manager/src/sl_device_peripheral.o" "./simplicity_sdk_2024.6.2/platform/service/interrupt_manager/src/sl_interrupt_manager_cortexm.o" "./simplicity_sdk_2024.6.2/platform/service/iostream/src/sl_iostream.o" "./simplicity_sdk_2024.6.2/platform/service/iostream/src/sl_iostream_retarget_stdio.o" "./simplicity_sdk_2024.6.2/platform/service/iostream/src/sl_iostream_rtt.o" "./simplicity_sdk_2024.6.2/platform/service/iostream/src/sl_iostream_stdlib_config.o" "./simplicity_sdk_2024.6.2/platform/service/memory_manager/src/sl_memory_manager.o" "./simplicity_sdk_2024.6.2/platform/service/memory_manager/src/sl_memory_manager_dynamic_reservation.o" "./simplicity_sdk_2024.6.2/platform/service/memory_manager/src/sl_memory_manager_pool.o" "./simplicity_sdk_2024.6.2/platform/service/memory_manager/src/sl_memory_manager_region.o" "./simplicity_sdk_2024.6.2/platform/service/memory_manager/src/sl_memory_manager_retarget.o" "./simplicity_sdk_2024.6.2/platform/service/memory_manager/src/sli_memory_manager_common.o" "./simplicity_sdk_2024.6.2/platform/service/sleeptimer/src/sl_sleeptimer.o" "./simplicity_sdk_2024.6.2/platform/service/sleeptimer/src/sl_sleeptimer_hal_burtc.o" "./simplicity_sdk_2024.6.2/platform/service/sleeptimer/src/sl_sleeptimer_hal_sysrtc.o" "./simplicity_sdk_2024.6.2/platform/service/sleeptimer/src/sl_sleeptimer_hal_timer.o" "./simplicity_sdk_2024.6.2/platform/service/system/src/sl_system_init.o" "./simplicity_sdk_2024.6.2/platform/service/system/src/sl_system_kernel.o" "./simplicity_sdk_2024.6.2/protocol/wisun/app/wisun_rcp/sl_ring.o" "./simplicity_sdk_2024.6.2/protocol/wisun/app/wisun_rcp/sl_wsrcp.o" "./simplicity_sdk_2024.6.2/protocol/wisun/app/wisun_rcp/sl_wsrcp_crc.o" "./simplicity_sdk_2024.6.2/protocol/wisun/app/wisun_rcp/sl_wsrcp_eusart.o" "./simplicity_sdk_2024.6.2/protocol/wisun/app/wisun_rcp/sl_wsrcp_os_main.o" "./simplicity_sdk_2024.6.2/protocol/wisun/app/wisun_rcp/sl_wsrcp_uart.o" "./simplicity_sdk_2024.6.2/util/third_party/freertos/cmsis/Source/cmsis_os2.o" "./simplicity_sdk_2024.6.2/util/third_party/freertos/kernel/croutine.o" "./simplicity_sdk_2024.6.2/util/third_party/freertos/kernel/event_groups.o" "./simplicity_sdk_2024.6.2/util/third_party/freertos/kernel/list.o" "./simplicity_sdk_2024.6.2/util/third_party/freertos/kernel/queue.o" "./simplicity_sdk_2024.6.2/util/third_party/freertos/kernel/stream_buffer.o" "./simplicity_sdk_2024.6.2/util/third_party/freertos/kernel/tasks.o" "./simplicity_sdk_2024.6.2/util/third_party/freertos/kernel/timers.o" "./simplicity_sdk_2024.6.2/util/third_party/freertos/kernel/portable/GCC/ARM_CM33_NTZ/non_secure/port.o" "./simplicity_sdk_2024.6.2/util/third_party/freertos/kernel/portable/GCC/ARM_CM33_NTZ/non_secure/portasm.o" "./simplicity_sdk_2024.6.2/util/third_party/freertos/kernel/portable/MemMang/heap_3.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/aes.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/asn1parse.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/asn1write.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/base64.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/bignum.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/bignum_core.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/bignum_mod.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/bignum_mod_raw.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ccm.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/cipher.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/cipher_wrap.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/constant_time.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ctr_drbg.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ecdh.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ecdsa.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ecp.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ecp_curves.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ecp_curves_new.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/entropy.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/entropy_poll.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/hmac_drbg.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/md.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/oid.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/pem.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/pk.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/pk_wrap.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/pkparse.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/pkwrite.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/platform.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/platform_util.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto_aead.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto_cipher.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto_client.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto_driver_wrappers_no_static.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto_ecp.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto_ffdh.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto_hash.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto_mac.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto_pake.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto_rsa.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto_se.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto_slot_management.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_crypto_storage.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/psa_util.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/sha1.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/sha256.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ssl_cache.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ssl_ciphersuites.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ssl_client.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ssl_cookie.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ssl_debug_helpers_generated.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ssl_msg.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ssl_ticket.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ssl_tls.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ssl_tls12_client.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/ssl_tls12_server.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/threading.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/x509.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/x509_create.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/x509_crl.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/x509_crt.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/x509_csr.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/x509write.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/x509write_crt.o" "./simplicity_sdk_2024.6.2/util/third_party/mbedtls/library/x509write_csr.o" "./simplicity_sdk_2024.6.2/util/third_party/segger/systemview/SEGGER/SEGGER_RTT.o" "C:/Users/Shrawani/SimplicityStudio/SDKs/simplicity_sdk_2//platform/emdrv/nvm3/lib/libnvm3_CM33_gcc.a" "C:/Users/Shrawani/SimplicityStudio/SDKs/simplicity_sdk_2//platform/radio/rail_lib/autogen/librail_release/librail_efr32xg28_gcc_release.a" "C:/Users/Shrawani/SimplicityStudio/SDKs/simplicity_sdk_2//protocol/wisun/stack/libwisun_mac_efr32xg2x_gcc.a" "C:/Users/Shrawani/SimplicityStudio/SDKs/simplicity_sdk_2//protocol/wisun/stack/libwisun_rcp_efr32xg2x_gcc.a" -lgcc -lc -lm -lnosys -Wl,--end-group -Wl,--start-group -lgcc -lc -lnosys -Wl,--end-group
	@echo 'Finished building target: $@'
	@echo ' '

	@echo 'Building out file: wisun_rcp.out'
	arm-none-eabi-objcopy "wisun_rcp.axf" "wisun_rcp.out"
	@echo ' '

	@echo 'Building hex file: wisun_rcp.hex'
	arm-none-eabi-objcopy -O ihex "wisun_rcp.axf" "wisun_rcp.hex"
	@echo ' '

	@echo 'Building bin file: wisun_rcp.bin'
	arm-none-eabi-objcopy -O binary "wisun_rcp.axf" "wisun_rcp.bin"
	@echo ' '

	@echo 'Building s37 file: wisun_rcp.s37'
	arm-none-eabi-objcopy -O srec "wisun_rcp.axf" "wisun_rcp.s37"
	@echo ' '

	@echo 'Running size tool'
	arm-none-eabi-size "wisun_rcp.axf" -A
	@echo ' '

# Other Targets
clean:
	-@$(foreach FILE, $(EXECUTABLES), $(shell $(RM) $(FILE)) )
	-@$(foreach FILE, $(OBJS), $(shell $(RM) $(FILE)) )
	-@$(foreach FILE, $(C_DEPS), $(shell $(RM) $(FILE)) )
	-$(RM) wisun_rcp.axf
	-@echo ' '

.PHONY: all clean dependents main-build

-include ../makefile.targets
