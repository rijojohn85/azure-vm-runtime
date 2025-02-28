import logging
import azure.functions as func
from src.azure_client import get_all_vms, filter_vms_by_runtime
from datetime import timedelta
import os
from src.log_vm_report import log_vm_report, send_report_to_slack

app = func.FunctionApp()
schedule = os.environ.get("SCHEDULE")
if not schedule:
    raise ValueError("Set the SCHEDULE environment variable")

@app.timer_trigger(schedule=schedule, arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
async def funcvmruntime(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    #get all running vms
    vm_dict = get_all_vms()
    #filter vms by runtime
    threshold = int(os.environ.get("THRESHOLD_HOURS"))
    filtered_vms = filter_vms_by_runtime(vm_dict, timedelta(hours=threshold))
    #log the report
    log_vm_report(filtered_vms)
    #send the report to slack
    await send_report_to_slack(filtered_vms)
    logging.info('Python timer trigger function executed.')