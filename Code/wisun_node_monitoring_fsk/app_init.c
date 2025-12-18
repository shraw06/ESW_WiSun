/***************************************************************************//**
* @file app_init.c
* @brief Application init
*******************************************************************************
* # License
* <b>Copyright 2021 Silicon Laboratories Inc. www.silabs.com</b>
*******************************************************************************
*
* SPDX-License-Identifier: Zlib
*
* The licensor of this software is Silicon Laboratories Inc.
*
* This software is provided 'as-is', without any express or implied
* warranty. In no event will the authors be held liable for any damages
* arising from the use of this software.
*
* Permission is granted to anyone to use this software for any purpose,
* including commercial applications, and to alter it and redistribute it
* freely, subject to the following restrictions:
*
* 1. The origin of this software must not be misrepresented; you must not
*    claim that you wrote the original software. If you use this software
*    in a product, an acknowledgment in the product documentation would be
*    appreciated but is not required.
* 2. Altered source versions must be plainly marked as such, and must not be
*    misrepresented as being the original software.
* 3. This notice may not be removed or altered from any source distribution.
*
*******************************************************************************
*
* EXPERIMENTAL QUALITY
* This code has not been formally tested and is provided as-is.  It is not suitable for production environments.
* This code will not be maintained.
*
******************************************************************************/
// -----------------------------------------------------------------------------
//                                   Includes
// -----------------------------------------------------------------------------
#include <stdio.h>
#include <assert.h>

#include "sl_main_init.h"
#include "cmsis_os2.h"
#include "sl_cmsis_os2_common.h"

#include "sl_wisun_crash_handler.h"
#include "app_coap.h"
#include "app.h"

#include "sl_i2cspm_instances.h"
#include "sl_si70xx.h"
#include "sl_status.h"


// -----------------------------------------------------------------------------
//                              Macros and Typedefs
// -----------------------------------------------------------------------------
#define APP_STACK_SIZE_BYTES   (5*2048UL)

// -----------------------------------------------------------------------------
//                          Static Function Declarations
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                                Global Variables
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                                Static Variables
// -----------------------------------------------------------------------------

// -----------------------------------------------------------------------------
//                          Public Function Definitions
// -----------------------------------------------------------------------------
void app_init(void)
{
  sl_status_t sc;

  // 1️⃣ Initialize crash handler
  sl_wisun_crash_handler_init();

  // 2️⃣ Initialize I2C peripheral
  //sc = sl_i2cspm_init_instances();
  if (sc != SL_STATUS_OK) {
    printf("[Error] I2C init failed: 0x%04lx\n", sc);
  } else {
    printf("I2C initialized successfully.\n");
  }

  // 3️⃣ Initialize Si70xx (temperature/humidity sensor)
  // 2️⃣ Initialize I2C peripheral (this function returns void on your SDK)
  sl_i2cspm_init_instances();
  printf("I2C initialized successfully.\n");

  // 3️⃣ Initialize Si70xx sensor (assign return value to sc and check it)
  sc = sl_si70xx_init(sl_i2cspm_si7021, 0x40);
  if (sc != SL_STATUS_OK) {
    printf("[Error] Si70xx init failed: 0x%04lx (check wiring)\n", sc);
  } else {
    printf("Si70xx sensor initialized successfully.\n");
  }



  // 4️⃣ Initialize CoAP resources
  app_coap_resources_init();

  // 5️⃣ Start app main thread
  const osThreadAttr_t app_task_attr = {
    .name        = "app_task",
    .attr_bits   = osThreadDetached,
    .cb_mem      = NULL,
    .cb_size     = 0,
    .stack_mem   = NULL,
    .stack_size  = APP_STACK_SIZE_BYTES,
    .priority    = osPriorityNormal,
    .tz_module   = 0
  };
  printf("%s/%s starting app_task : APP_STACK_SIZE_BYTES %4ld\n",
         __FILE__, __FUNCTION__,
         APP_STACK_SIZE_BYTES);

  osThreadId_t app_thr_id = osThreadNew(app_task,
                                        NULL,
                                        &app_task_attr);
  assert(app_thr_id != NULL);
}


// -----------------------------------------------------------------------------
//                          Static Function Definitions
// -----------------------------------------------------------------------------
