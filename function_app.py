import azure.functions as func
import logging

app = func.FunctionApp()

# @app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="test-hub",
#                                connection="dt021eventhub_RootManageSharedAccessKey_EVENTHUB") 
# def eventhub_trigger(azeventhub: func.EventHubEvent):
#     logging.info('Python EventHub trigger processed an event: %s',
#                 azeventhub.get_body().decode('utf-8'))


# This example uses SDK types to directly access the underlying EventData object provided by the Event Hubs trigger.
# To use, uncomment the section below and add azurefunctions-extensions-bindings-eventhub to your requirements.txt file
# Ref: aka.ms/functions-sdk-eventhub-python
#
# import azurefunctions.extensions.bindings.eventhub as eh
# @app.event_hub_message_trigger(
#     arg_name="event", event_hub_name="test-hub", connection="dt021eventhub_RootManageSharedAccessKey_EVENTHUB"
# )
# def eventhub_trigger(event: eh.EventData):
#     logging.info(
#         "Python EventHub trigger processed an event %s",
#         event.body_as_str()
#     )


@app.function_name(name="eventhub_output")
@app.route(route="eventhub_output", methods=["POST"])
@app.event_hub_output(arg_name="event", event_hub_name="test-hub",
                     connection="dt021eventhub_RootManageSharedAccessKey_EVENTHUB")
def eventhub_output(req: func.HttpRequest, event: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_body().decode('utf-8')

    logging.info(f"Request body: {req_body}")

    event.set(req_body)

    return func.HttpResponse(f"Event Hub message sent: {req_body}")
    # try:
    #     req_body = req.get_json()
    # except ValueError:
    #     return func.HttpResponse(
    #          "Invalid JSON body.",
    #          status_code=400
    #     )

    # message = req_body.get('message')
    # if message:
    #     event.set(func.EventHubMessage(message))
    #     return func.HttpResponse(f"Event Hub message sent: {message}")
    # else:
    #     return func.HttpResponse(
    #          "Please pass a 'message' in the JSON body",
    #          status_code=400
    #     )