# Python client documentation

This documentation is for developers interested in using the Notify Python client to send emails, text messages or letters. Notify supports Python 3.x and 2.7.

# Set up the client

## Install the client

Run the following code in the command line:

```shell
pip install -e git+https://github.com/govau/notify-client-python.git@1.0.0#egg=notify-client-python
```

Refer to the [client changelog](https://github.com/govau/notify-python-client/blob/master/CHANGELOG.md) for the client version number and the latest updates.

## Create a new instance of the client

Add this code to your application:

```python
import notify

client = notify.Client(api_key)
```

To get an API key, [sign in to Notify](https://notify.gov.au) and go to the **API integration** page. You can find more information in the [API keys](#api-keys) section of this documentation.

# Send a message

You can use Notify to send text messages, emails and letters.

## Send a text message

### Method

```python
response = notifications_client.send_sms_notification(
    phone_number='+61400900123', # required string
    template_id='f33517ff-2a88-4f6e-b855-c550268ce08a', # required UUID string
)
```

### Arguments

#### phone_number (required)

The phone number of the recipient of the text message. This can be a Australian or international number.

#### template_id (required)

Sign in to [Notify](https://notify.gov.au) and go to the **Templates** page to find the template ID.

#### personalisation (optional)

If a template has placeholder fields for personalised information such as name or reference number, you must provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'application_date': '2018-01-01',
}
```

You can leave out this argument if a template does not have any placeholder fields for personalised information.

#### reference (optional)

A unique identifier you can create if necessary. This reference identifies a single unique notification or a batch of notifications. It must not contain any personal information such as name or postal address. For example:

```python
reference='STRING', # optional string - identifies notification(s)
```

You can leave out this argument if you do not have a reference.

#### sms_sender_id (optional)

A unique identifier of the sender of the text message notification. You can find this information on the **Text Message sender** settings screen:

1. Sign into your Notify account.
1. Go to **Settings**.
1. If you need to change to another service, select **Switch service** in the top right corner of the screen and select the correct one.
1. Go to the **Text Messages** section and select **Manage** on the **Text Message sender** row.

You can then either:

- copy the sender ID that you want to use and paste it into the method
- select **Change** to change the default sender that the service will use, and select **Save**

```python
sms_sender_id='8e222534-7f05-4972-86e3-17c5d9f894e2' # optional UUID string
```

You can leave out this argument if your service only has one text message sender, or if you want to use the default sender.

### Response

If the request to the client is successful, the client returns a `dict`:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a",
  "reference": "STRING",
  "content": {
    "body": "MESSAGE TEXT",
    "from_number": "SENDER"
  },
  "uri": "https://rest-api.notify.gov.au/v2/notifications/740e5834-3a29-46b4-9a6f-16142fde533a",
  "template": {
    "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a',
    "version": INTEGER,
    "uri": "https://rest-api.notify.gov.au/v2/template/ceb50d92-100d-4b8b-b559-14fa3b091cd"
  }
}
```

If you are using the [test API key](#test), all your messages will come back as delivered.

All messages sent using the [team and whitelist](#team-and-whitelist) or [live](#live) keys will appear on your dashboard.

### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code.

| error.status_code | error.message                                                                                                                                                     | How to fix                                                                                                         |
| :---------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient using a team-only API key"`<br>`]}`                                            | Use the correct type of [API key](#api-keys)                                                                       |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient when service is in trial mode - see https://notify.gov.au/trial-mode"`<br>`}]` | Your service cannot send this notification in [trial mode](https://notify.gov.au/features/using-notify#trial-mode) |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`                                          | Check your system clock                                                                                            |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`                                                           | Use the correct API key. Refer to [API keys](#api-keys) for more information                                       |
| `429`             | `[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`                    | Refer to [API rate limits](#api-rate-limits) for more information                                                  |
| `429`             | `[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT NUMBER) for today"`<br>`}]`                                                | Refer to [service limits](#service-limits) for the limit number                                                    |
| `500`             | `[{`<br>`"error": "Exception",`<br>`"message": "Internal server error"`<br>`}]`                                                                                   | Notify was unable to process the request, resend your notification.                                                |

## Send an email

### Method

```python
response = notifications_client.send_email_notification(
    email_address='sender@something.com', # required string
    template_id='f33517ff-2a88-4f6e-b855-c550268ce08a', # required UUID string
)
```

### Arguments

#### email_address (required)

The email address of the recipient.

#### template_id (required)

Sign in to [Notify](https://notify.gov.au) and go to the **Templates** page to find the template ID.

#### personalisation (optional)

If a template has placeholder fields for personalised information such as name or reference number, you need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'application_date': '2018-01-01',
}
```

You can leave out this argument if a template does not have any placeholder fields for personalised information.

#### reference (optional)

A unique identifier you can create if necessary. This reference identifies a single unique notification or a batch of notifications. It must not contain any personal information such as name or postal address. For example:

```python
reference='STRING', # optional string - identifies notification(s)
```

You can leave out this argument if you do not have a reference.

#### email_reply_to_id (optional)

This is an email reply-to address specified by you to receive replies from your users. Your service cannot go live until you set up at least one of these email addresses. To set up:

1. Sign into your Notify account.
1. Go to **Settings**.
1. If you need to change to another service, select **Switch service** in the top right corner of the screen and select the correct one.
1. Go to the Email section and select **Manage** on the **Email reply-to addresses** row.
1. Select **Change** to specify the email address to receive replies, and select **Save**.

For example:

```python
email_reply_to_id='8e222534-7f05-4972-86e3-17c5d9f894e2' # optional UUID string
```

You can leave out this argument if your service only has one email reply-to address, or you want to use the default email address.

## Send a document by email

Send files without the need for email attachments.

This is an invitation-only feature. [Contact the Notify team](https://notify.gov.au/support) to enable this function for your service.

To send a document by email, add a placeholder field to the template then upload a file. The placeholder field will contain a secure link to download the document.

#### Add a placeholder field to the template

1. Sign in to [Notify](https://notify.gov.au).
1. Go to the **Templates** page and select the relevant email template.
1. Add a placeholder field to the email template using double brackets. For example:

"Download your document at: ((link_to_document))"

#### Upload your document

The document you upload must be a PDF file smaller than 2MB.

Pass the file object as a value into the personalisation argument. For example:

```python
from notify import prepare_upload

with open('file.pdf', 'rb') as f:
    ...
    personalisation={
      'first_name': 'Amala',
      'application_date': '2018-01-01',
      'link_to_document': prepare_upload(f),
    }
```

### Response

If the request to the client is successful, the client returns a `dict`:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a",
  "reference": "STRING",
  "content": {
    "subject": "SUBJECT TEXT",
    "body": "MESSAGE TEXT",
    "from_email": "SENDER EMAIL"
  },
  "uri": "https://rest-api.notify.gov.au/v2/notifications/740e5834-3a29-46b4-9a6f-16142fde533a",
  "template": {
    "id": "f33517ff-2a88-4f6e-b855-c550268ce08a",
    "version": INTEGER,
    "uri": "https://rest-api.notify.gov.au/v2/template/f33517ff-2a88-4f6e-b855-c550268ce08a"
  }
}
```

### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code.

| error.status_code | error.message                                                                                                                                                     | How to fix                                                                                                         |
| :---------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient using a team-only API key"`<br>`]}`                                            | Use the correct type of [API key](#api-keys)                                                                       |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Can't send to this recipient when service is in trial mode - see https://notify.gov.au/trial-mode"`<br>`}]` | Your service cannot send this notification in [trial mode](https://notify.gov.au/features/using-notify#trial-mode) |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Unsupported document type '{}'. Supported types are: {}"`<br>`}]`                                           | The document you upload must be a PDF file                                                                         |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Document didn't pass the virus scan"`<br>`}]`                                                               | The document you upload must be virus free                                                                         |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Service is not allowed to send documents"`<br>`}]`                                                          | Contact the Notify team                                                                                            |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`                                          | Check your system clock                                                                                            |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`                                                           | Use the correct type of [API key](#api-keys)                                                                       |
| `429`             | `[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`                    | Refer to [API rate limits](#api-rate-limits) for more information                                                  |
| `429`             | `[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT NUMBER) for today"`<br>`}]`                                                | Refer to [service limits](#service-limits) for the limit number                                                    |
| `500`             | `[{`<br>`"error": "Exception",`<br>`"message": "Internal server error"`<br>`}]`                                                                                   | Notify was unable to process the request, resend your notification.                                                |
| -                 | `ValueError('Document is larger than 2MB')`                                                                                                                       | Document size was too large, upload a smaller document.                                                            |

## Send a letter

When your service first signs up to Notify, you’ll start in trial mode. You can only send letters in live mode. You must ask Notify to make your service live.

1. Sign in to [Notify](https://notify.gov.au).
1. Select **Using Notify**.
1. Select **requesting to go live**.

### Method

```python
    response = notifications_client.send_letter_notification(
        template_id='f33517ff-2a88-4f6e-b855-c550268ce08a', # required UUID string
        personalisation={
          'address_line_1': 'The Occupier' # required string,
          'address_line_2': '123 High Street' # required string,
          'postcode': 'SW14 6BH' # required string,
        },
    )
```

### Arguments

#### template_id (required)

Sign in to Notify and go to the **Templates page** to find the template ID.

#### personalisation (required)

The personalisation argument always contains the following required parameters for the letter recipient's address:

- `address_line_1`
- `address_line_2`
- `postcode`

Any other placeholder fields included in the letter template also count as required parameters. You need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
  'address_line_1': 'The Occupier',
  'address_line_2': '123 High Street',
  'postcode': 'SW14 6BF',
  'name': 'John Smith',
  'application_id': '4134325'
}
```

#### reference (optional)

A unique identifier you can create if necessary. This reference identifies a single unique notification or a batch of notifications. It must not contain any personal information such as name or postal address. For example:

```python
reference='STRING' # optional string - identifies notification(s)
```

#### personalisation (optional)

The following parameters in the letter recipient's address are optional:

```python
personalisation={
    'address_line_3': '123 High Street',
    'address_line_4': 'Richmond upon Thames',
    'address_line_5': 'London',
    'address_line_6': 'Middlesex',
}
```

### Response

If the request to the client is successful, the client returns a `dict`:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a",
  "reference": 'STRING',
  "content": {
    "subject": "SUBJECT TEXT",
    "body": "LETTER TEXT",
  },
  "uri": "https://rest-api.notify.gov.au/v2/notifications/740e5834-3a29-46b4-9a6f-16142fde533a",
  "template": {
    "id": "f33517ff-2a88-4f6e-b855-c550268ce08a",
    "version": INTEGER,
    "uri": "https://rest-api.notify.gov.au/v2/template/f33517ff-2a88-4f6e-b855-c550268ce08a"
  }
  "scheduled_for": None
}
```

### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code.

| error.status_code | error.message                                                                                                                                            | How to fix                                                                                                                                                                |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters with a team api key"`<br>`]}`                                                  | Use the correct type of [API key](#api-keys)                                                                                                                              |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters when service is in trial mode - see https://notify.gov.au/trial-mode"`<br>`}]` | Your service cannot send this notification in [trial mode](https://notify.gov.au/features/using-notify#trial-mode)                                                        |
| `400`             | `[{`<br>`"error": "ValidationError",`<br>`"message": "personalisation address_line_1 is a required property"`<br>`}]`                                    | Ensure that your template has a field for the first line of the address, check [personalisation](#send-a-letter-arguments-personalisation-optional) for more information. |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`                                 | Check your system clock                                                                                                                                                   |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`                                                  | Use the correct API key. Refer to [API keys](#api-keys) for more information                                                                                              |
| `429`             | `[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type TEAM/TEST/LIVE of 3000 requests per 60 seconds"`<br>`}]`           | Refer to [API rate limits](#api-rate-limits) for more information                                                                                                         |
| `429`             | `[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (LIMIT NUMBER) for today"`<br>`}]`                                       | Refer to [service limits](#service-limits) for the limit number                                                                                                           |
| `500`             | `[{`<br>`"error": "Exception",`<br>`"message": "Internal server error"`<br>`}]`                                                                          | Notify was unable to process the request, resend your notification.                                                                                                       |

## Send a pre-compiled letter

This is an invitation-only feature. Contact the Notify team on the [support page](https://notify.gov.au/support) for more information.

### Method

```python
response = notifications_client.send_precompiled_letter_notification(
    reference,      # Reference to identify the notification
    pdf_file        # PDF File object
)
```

### Arguments

##### reference (required)

A unique identifier you create. This reference identifies a single unique notification or a batch of notifications. It must not contain any personal information such as name or postal address.

#### pdf_file (required)

The precompiled letter must be a PDF file.

```python
with open("path/to/pdf_file", "rb") as pdf_file:
    notification = notifications_client.send_precompiled_letter_notification(
        reference="your reference", pdf_file=pdf_file
    )
```

### Response

If the request to the client is successful, the client returns a `dict`:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a",
  "reference": "your-letter-reference"
}
```

### Error codes

If the request is not successful, the client returns an HTTPError containing the relevant error code.

| error.status_code | error.message                                                                                                                                            | How to fix                                                                                                                            |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters with a team api key"`<br>`]}`                                                  | Use the correct type of [API key](#api-keys)                                                                                          |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send precompiled letters"`<br>`]}`                                                          | This is an invitation-only feature. Contact the Notify team on the [support page](https://notify.gov.au/support) for more information |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Letter content is not a valid PDF"`<br>`]}`                                                        | PDF file format is required                                                                                                           |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Cannot send letters when service is in trial mode - see https://notify.gov.au/trial-mode"`<br>`}]` | Your service cannot send this notification in [trial mode](https://notify.gov.au/features/using-notify#trial-mode)                    |
| `400`             | `[{`<br>`"error": "ValidationError",`<br>`"message": "reference is a required property"`<br>`}]`                                                         | Add a `reference` argument to the method call                                                                                         |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Service is not allowed to send precompiled letters"`<br>`}]`                                       | Contact the Notify team                                                                                                               |
| `429`             | `[{`<br>`"error": "RateLimitError",`<br>`"message": "Exceeded rate limit for key type live of 10 requests per 20 seconds"`<br>`}]`                       | Use the correct API key. Refer to [API keys](#api-keys) for more information                                                          |
| `429`             | `[{`<br>`"error": "TooManyRequestsError",`<br>`"message": "Exceeded send limits (50) for today"`<br>`}]`                                                 | Refer to [service limits](#service-limits) for the limit number                                                                       |

# Get message status

Message status depends on the type of message you have sent.

You can only get the status of messages that are 7 days old or newer.

## Status - text and email

| Status    | Information                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :-------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Created   | The message is queued to be sent to the provider. The notification usually remains in this state for a few seconds.                                                                                                                                                                                                                                                                                                                                   |
| Sending   | The message is queued to be sent by the provider to the recipient, and Notify is waiting for delivery information.                                                                                                                                                                                                                                                                                                                                    |
| Delivered | The message was successfully delivered.                                                                                                                                                                                                                                                                                                                                                                                                               |
| Failed    | This covers all failure statuses:<br>- `permanent-failure` - "The provider was unable to deliver message, email or phone number does not exist; remove this recipient from your list"<br>- `temporary-failure` - "The provider was unable to deliver message, email inbox was full or phone was turned off; you can try to send the message again"<br>- `technical-failure` - "Notify had a technical failure; you can try to send the message again" |

## Status - text only

| Status  | Information                                                                                                                                                                                                                   |
| :------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Pending | Notify received a callback from the provider but the device has not yet responded. Another callback from the provider determines the final status of the notification.                                                        |
| Sent    | The text message was delivered internationally. This only applies to text messages sent to non-AU phone numbers. Notify may not receive additional status updates depending on the recipient's country and telecoms provider. |

## Status - letter

| Status   | information                                                                                                                                    |
| :------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| Failed   | The only failure status that applies to letters is `technical-failure`. Notify had an unexpected error while sending to our printing provider. |
| Accepted | Notify is printing and posting the letter.                                                                                                     |
| Received | The provider has received the letter to deliver.                                                                                               |

## Status - pre-compiled letter

| Status              | information                                                                         |
| :------------------ | :---------------------------------------------------------------------------------- |
| Pending virus check | Notify virus scan of the pre-compiled letter file is not yet complete.              |
| Virus scan failed   | Notify virus scan has identified a potential virus in the pre-compiled letter file. |

## Get the status of one message

### Method

```python
response = notifications_client.get_notification_by_id(notification_id)
```

### Arguments

#### notification_id (required)

The ID of the notification. You can find the notification ID in the response to the [original notification method call](/python.html#get-the-status-of-one-message-response).

You can also find it in your [Notify Dashboard](https://notify.gov.au).

1. Sign into Notify and select **Dashboard**.
1. Select either **emails sent**, **text messages sent**, or **letters sent**.
1. Select the relevant notification.
1. Copy the notification ID from the end of the page URL, for example `https://notify.gov.au/services/af90d4cb-ae88-4a7c-a197-5c30c7db423b/notification/ID`.

### Response

If the request to the client is successful, the client will return a `dict`:

```python
{
  "id": "740e5834-3a29-46b4-9a6f-16142fde533a", # required string - notification ID
  "reference": "STRING", # optional string
  "email_address": "sender@something.com",  # required string for emails
  "phone_number": "+447900900123",  # required string for text messages
  "line_1": "ADDRESS LINE 1", # required string for letter
  "line_2": "ADDRESS LINE 2", # required string for letter
  "line_3": "ADDRESS LINE 3", # optional string for letter
  "line_4": "ADDRESS LINE 4", # optional string for letter
  "line_5": "ADDRESS LINE 5", # optional string for letter
  "line_6": "ADDRESS LINE 6", # optional string for letter
  "postcode": "STRING", # required string for letter
  "type": "sms / letter / email", # required string
  "status": "sending / delivered / permanent-failure / temporary-failure / technical-failure", # required string
  "template": {
    "Version": INTEGER
    "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
    "uri": "/v2/template/{id}/{version}", # required
  },
  "body": "STRING", # required string - body of notification
  "subject": "STRING" # required string for email - subject of email
  "created_at": "STRING", # required string - date and time notification created
  "created_by_name": "STRING", # optional string - name of the person who sent the notification if sent manually
  "sent_at": "STRING", # optional string - date and time notification sent to provider
  "completed_at:" "STRING" # optional string - date and time notification delivered or failed
}
```

### Error codes

If the request is not successful, the client will return an `HTTPError` containing the relevant error code:

| error.status_code | error.message                                                                                                            | How to fix                                                                   |
| :---------------- | :----------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| `400`             | `[{`<br>`"error": "ValidationError",`<br>`"message": "id is not a valid UUID"`<br>`}]`                                   | Check the notification ID                                                    |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]` | Check your system clock                                                      |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`                  | Use the correct API key. Refer to [API keys](#api-keys) for more information |
| `404`             | `[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`                                            | Check the notification ID                                                    |

## Get the status of multiple messages

This API call returns one page of up to 250 messages and statuses. You can get either the most recent messages, or get older messages by specifying a particular notification ID in the `older_than` argument.

You can only get the status of messages that are 7 days old or newer.

### Method

#### All messages

This will return all your messages with statuses. They will display in pages of up to 250 messages each.

```python
response = notifications_client.get_all_notifications(template_type, status, reference, older_than)
```

You can filter the returned messages by including the following optional arguments in the method:

- [`template_type`](#template-type-optional)
- [`status`](#status-optional)
- [`reference`](#get-the-status-of-all-messages-arguments-reference-optional)
- [`older_than`](#older-than-optional)

#### One page of up to 250 messages

This will return one page of up to 250 messages and statuses. You can get either the most recent messages, or get older messages by specifying a particular notification ID in the [`older_than`](#older-than-optional) argument.

##### Most recent messages

```python
response = get_all_notifications_iterator(status="sending")
```

You must set the [`status`](#status-optional) argument to `sending`.

##### Older messages

To get older messages:

1. Get the ID of an older notification.
1. Add the following code to your application, with the older notification ID in the [`older_than`](#older-than-optional) argument.

```python
response = get_all_notifications_iterator(status="sending",older_than="NOTIFICATION ID")
```

You must set the [`status`](#status-optional) argument to `sending`.

This method will return the next oldest messages from the specified notification ID.

### Arguments

You can omit any of these arguments to ignore these filters.

#### template_type (optional)

You can filter by:

- `email`
- `sms`
- `letter`

#### status (optional)

| status              | description                                                                                                                                                                                                                                    | text | email | letter |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--- | :---- | :----- |
| `created`           | The message is queued to be sent to the provider                                                                                                                                                                                               | Yes  | Yes   |        |
| `sending`           | The message is queued to be sent to the recipient by the provider                                                                                                                                                                              | Yes  | Yes   |        |
| `delivered`         | The message was successfully delivered                                                                                                                                                                                                         | Yes  | Yes   |        |
| `failed`            | This will return all failure statuses:<br>- `permanent-failure`<br>- `temporary-failure`<br>- `technical-failure`                                                                                                                              | Yes  | Yes   |        |
| `permanent-failure` | The provider was unable to deliver message, email or phone number does not exist; remove this recipient from your list                                                                                                                         | Yes  | Yes   |        |
| `temporary-failure` | The provider was unable to deliver message, email inbox was full or phone was turned off; you can try to send the message again                                                                                                                | Yes  | Yes   |        |
| `technical-failure` | Email or text message: Notify had a technical failure; you can try to send the message again. <br><br>Letter: Notify had an unexpected error while sending to our printing provider. <br><br>You can omit this argument to ignore this filter. | Yes  | Yes   |        |
| `accepted`          | Notify is printing and posting the letter                                                                                                                                                                                                      |      |       | Yes    |
| `received`          | The provider has received the letter to deliver                                                                                                                                                                                                |      |       | Yes    |

#### reference (optional)

A unique identifier you can create if necessary. This reference identifies a single unique notification or a batch of notifications. It must not contain any personal information such as name or postal address. For example:

```python
reference='STRING' # optional string - identifies notification(s)
```

#### older_than (optional)

Input the ID of a notification into this argument. If you use this argument, the method returns the next 250 received notifications older than the given ID.

```python
older_than='740e5834-3a29-46b4-9a6f-16142fde533a' # optional string - notification ID
```

If you leave out this argument, the method returns the most recent 250 notifications.

The client only returns notifications that are 7 days old or newer. If the notification specified in this argument is older than 7 days, the client returns an empty response.

### Response

If the request to the client is successful, the client returns a `dict`.

#### All messages

```python
{"notifications":
  [
    {
      "id": "740e5834-3a29-46b4-9a6f-16142fde533a", # required string - notification ID
      "reference": "STRING", # optional string - client reference
      "email_address": "sender@something.com",  # required string for emails
      "phone_number": "+447900900123",  # required string for text messages
      "line_1": "ADDRESS LINE 1", # required string for letter
      "line_2": "ADDRESS LINE 2", # required string for letter
      "line_3": "ADDRESS LINE 3", # optional string for letter
      "line_4": "ADDRESS LINE 4", # optional string for letter
      "line_5": "ADDRESS LINE 5", # optional string for letter
      "line_6": "ADDRESS LINE 6", # optional string for letter
      "postcode": "STRING", # required for string letter
      "type": "sms / letter / email", # required string
      "status": "sending / delivered / permanent-failure / temporary-failure / technical-failure", # required string
      "template": {
        "version": INTEGER
        "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
        "uri": "/v2/template/{id}/{version}", # required
      },
      "body": "STRING", # required string - body of notification
      "subject": "STRING" # required string for email - subject of email
      "created_at": "STRING", # required string - date and time notification created
      "created_by_name": "STRING", # optional string - name of the person who sent the notification if sent manually
      "sent_at": " STRING", # optional string - date and time notification sent to provider
      "completed_at": "STRING" # optional string - date and time notification delivered or failed
    },
    …
  ],
  "links": {
    "current": "/notifications?template_type=sms&status=delivered",
    "next": "/notifications?other_than=last_id_in_list&template_type=sms&status=delivered"
  }
}
```

#### One page of up to 250 messages

```python
<generator object NotificationsAPIClient.get_all_notifications_iterator at 0x1026c7410>
```

### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code:

| error.status_code | error.message                                                                                                                                                                                    | How to fix                                                                   |
| :---------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| `400`             | `[{`<br>`"error": "ValidationError",`<br>`"message": "bad status is not one of [created, sending, delivered, pending, failed, technical-failure, temporary-failure, permanent-failure]"`<br>`}]` | Contact the Notify team                                                      |
| `400`             | `[{`<br>`"error": "ValidationError",`<br>`"message": "Apple is not one of [sms, email, letter]"`<br>`}]`                                                                                         | Contact the Notify team                                                      |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]`                                                                         | Check your system clock                                                      |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`                                                                                          | Use the correct API key. Refer to [API keys](#api-keys) for more information |

# Get a template

## Get a template by ID

### Method

This returns the latest version of the template.

```python
response = notifications_client.get_template(
  'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
)
```

### Arguments

#### template_id (required)

The ID of the template. Sign into Notify and go to the **Templates** page to find this.

### Response

If the request to the client is successful, the client returns a `dict`.

```python
{
    "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a', # required string - template ID
    "name": "STRING", # required string - template name
    "type": "sms / email / letter" , # required string
    "created_at": "STRING", # required string - date and time template created
    "updated_at": "STRING", # required string - date and time template last updated
    "version": INTEGER,
    "created_by": "someone@example.com", # required string
    "body": "STRING", # required string - body of notification
    "subject": "STRING" # required string for email - subject of email
}
```

### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code:

| error.status_code | error.message                                                                                                            | How to fix                                                                     |
| :---------------- | :----------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]` | Check your system clock                                                        |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`                  | Use the correct API key. Refer to [API keys](#api-keys) for more information   |
| `404`             | `[{`<br>`"error": "NoResultFound",`<br>`"message": "No Result Found"`<br>`}]`                                            | Check your [template ID](#get-a-template-by-id-arguments-template-id-required) |

## Get a template by ID and version

### Method

```python
response = notifications_client.get_template_version(
    'f33517ff-2a88-4f6e-b855-c550268ce08a' # required string - template ID
    'version': INTEGER,
)
```

### Arguments

#### template_id (required)

The ID of the template. Sign in to Notify and go to the **Templates** page to find this.

#### version (required)

The version number of the template.

### Response

If the request to the client is successful, the client returns a `dict`.

```python
{
    "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a', # required string - template ID
    "name": "STRING", # required string - template name
    "type": "sms / email / letter" , # required string
    "created_at": "STRING", # required string - date and time template created
    "updated_at": "STRING", # required string - date and time template last updated
    "version": INTEGER,
    "created_by": "someone@example.com", # required string
    "body": "STRING", # required string - body of notification
    "subject": "STRING" # required string for email - subject of email
}
```

### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code:

| error.status_code | error.message                                                                                                            | How to fix                                                                                                                  |
| :---------------- | :----------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]` | Check your system clock                                                                                                     |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`                  | Use the correct API key. Refer to [API keys](#api-keys) for more information                                                |
| `404`             | `[{`<br>`"error": "NoResultFound",`<br>`"message": "No Result Found"`<br>`}]`                                            | Check your [template ID](#get-a-template-by-id-and-version-arguments-template-id-required) and [version](#version-required) |

## Get all templates

### Method

This returns the latest version of all templates.

```python
response = notifications_client.get_all_templates(
    template_type="sms / letter / email" # optional string
)
```

### Arguments

#### template_type (optional)

If omitted, the method returns all templates. Otherwise you can filter by:

- `email`
- `sms`
- `letter`

### Response

If the request to the client is successful, the client returns a `dict`.

```python
{
    "templates": [
        {
            "id": 'f33517ff-2a88-4f6e-b855-c550268ce08a', # required string - template ID
            "name": "STRING", # required string - template name
            "type": "sms / email / letter" , # required string
            "created_at": "STRING", # required string - date and time template created
            "updated_at": "STRING", # required string - date and time template last updated
            "version": NUMBER, # required string - template version
            "created_by": "someone@example.com", # required string
            "body": "STRING", # required string - body of notification
            "subject": "STRING" # required string for email - subject of email
        },
        {
            ...another template
        }
    ]
}
```

If no templates exist for a template type or there no templates for a service, the client returns a `dict` with an empty `templates` list element:

```python
{
    "templates": []
}
```

## Generate a preview template

### Method

This generates a preview version of a template.

```python
response = notifications_client.post_template_preview(
    'template_id'='f33517ff-2a88-4f6e-b855-c550268ce08a', # required UUID string
    personalisation={
        'KEY': 'VALUE',
        'KEY': 'VALUE',
        ...
        }, # required dict - specifies template parameters
)
```

The parameters in the personalisation argument must match the placeholder fields in the actual template. The API notification client will ignore any extra fields in the method.

### Arguments

#### template_id (required)

The ID of the template. Sign into Notify and go to the **Templates** page.

#### personalisation (required)

If a template has placeholder fields for personalised information such as name or reference number, you need to provide their values in a dictionary with key value pairs. For example:

```python
personalisation={
    'first_name': 'Amala',
    'application_date': '2018-01-01',
}
```

### Response

If the request to the client is successful, you receive a `dict` response.

```python
{
    "id": "740e5834-3a29-46b4-9a6f-16142fde533a", # required string - notification ID
    "type": "sms / email / letter" , # required string
    "version": INTEGER,
    "body": "STRING", # required string - body of notification
    "subject": "STRING" # required string for email - subject of email
}
```

### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code:

| error.status_code | error.message                                                                                                            | Notes                                                                                               |
| :---------------- | :----------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------- |
| `400`             | `[{`<br>`"error": "BadRequestError",`<br>`"message": "Missing personalisation: [PERSONALISATION FIELD]"`<br>`}]`         | Check that the personalisation arguments in the method match the placeholder fields in the template |
| `400`             | `[{`<br>`"error": "NoResultFound",`<br>`"message": "No result found"`<br>`}]`                                            | Check the [template ID](#generate-a-preview-template-arguments-template-id-required)                |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]` | Check your system clock                                                                             |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`                  | Use the correct API key. Refer to [API keys](#api-keys) for more information                        |

# Get received text messages

This API call returns one page of up to 250 received text messages. You can get either the most recent messages, or get older messages by specifying a particular notification ID in the older_than argument.

You can only get the status of messages that are 7 days old or newer.

## Get all received text messages

This method returns a `<generator object>` with all received text messages.

### Method

```python
response = get_received_texts_iterator()
```

### Response

If the request to the client is successful, the client will return a `<generator object>` that will return all received text messages.

```python
<generator object NotificationsAPIClient.get_received_texts_iterator at 0x1026c7410>
```

## Get one page of received text messages

This will return one page of up to 250 text messages.

### Method

```python
response = client.get_received_texts(older_than)
```

You can specify which text messages to receive by inputting the ID of a received text message into the [`older_than`](#get-one-page-of-received-text-messages-arguments-older-than-optional) argument.

### Arguments

#### older_than (optional)

Input the ID of a received text message into this argument. If you use this argument, the method returns the next 250 received text messages older than the given ID.

```python
older_than='740e5834-3a29-46b4-9a6f-16142fde533a' # optional string - notification ID
```

If this argument is omitted, the method returns the most recent 250 text messages.

### Response

If the request to the client is successful, the client returns a `dict`.

```python
{
  "received_text_messages":
  [
    {
      "id": "STRING", # required string - ID of received text message
      "user_number": "STRING", # required string
      "notify_number": "STRING", # required string - receiving number
      "created_at": "STRING", # required string - date and time template created
      "service_id": "STRING", # required string - service ID
      "content": "STRING" # required string - text content
    },
    …
  ],
  "links": {
    "current": "/received-text-messages",
    "next": "/received-text-messages?other_than=last_id_in_list"
  }
}
```

### Error codes

If the request is not successful, the client returns an `HTTPError` containing the relevant error code.

| error.status_code | error.message                                                                                                            | How to fix                                                                   |
| :---------------- | :----------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------- |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Error: Your system clock must be accurate to within 30 seconds"`<br>`}]` | Check your system clock                                                      |
| `403`             | `[{`<br>`"error": "AuthError",`<br>`"message": "Invalid token: signature, api token not found"`<br>`}]`                  | Use the correct API key. Refer to [API keys](#api-keys) for more information |
