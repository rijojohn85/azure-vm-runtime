# Azure VM runtime monitor

>This Azure function collects all running VMs in the current subscription id and filters those that have been running over a set threshold

Currently, the app is setup to run in `Infracloud_old (vishalinfracloud.onmicrosoft.com)`

To run it under a different subscription:

1. Enable System-Assigned Managed Identity

    ```sh
    az functionapp identity assign --name <FUNCTION_APP_NAME> --resource-group <RESOURCE_GROUP>
    ```
    Replace:

     - <FUNCTION_APP_NAME> → Your function app’s name\
     - <RESOURCE_GROUP> → Your Azure resource group

2. Assign Reader Role:

    ```sh
    az role assignment create --assignee <PRINCIPAL_ID> \
        --role "Reader" \
        --scope /subscriptions/<SUBSCRIPTION_ID>
    ```
    Replace
     - <PRINCIPAL_ID> → The Managed Identity's Object ID
        ```sh
        az functionapp identity show --name <FUNCTION_APP_NAME> --resource-group <RESOURCE_GROUP>
        ```
    - <SUBSCRIPTION_ID> → Your Azure subscription ID

3. Add the azure subscription ID to the env variable `AZURE_SUBSCRIPTION_ID`

The app can be found at [link](https://portal.azure.com/#@vishalinfracloud.onmicrosoft.com/resource/subscriptions/af107490-868a-4adc-8f44-4e6261114090/resourceGroups/vm-runtime-test-rg/providers/Microsoft.Web/sites/vm-runtime-test-fa/appServices)

The threshold and running interval can be set through the environmental variables in app:

1. `SCHEDULE` = "0 0 6 * * *" currently set to run at 6AM daily. Can be configured similariy to a cronjob. [Refernce](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=python-v2%2Cisolated-process%2Cnodejs-v4&pivots=programming-language-python#ncrontab-examples)
2. `THRESHOLD_HOURS` = 0 currently set to report all running VMs, can be configured.

The report to sent to a private slack channel, this can be configured through environment variables by providing the appropriate slack web hook url. env name: SLACK_WEBHOOK_URL

Currently, the app can be accessed at [#azure-vm-runtime](https://infracloud.slack.com/archives/C08F83DJH54)