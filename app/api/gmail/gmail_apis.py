from datetime import datetime, timezone, timedelta
from typing import Any, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId

from app.helpers import google_helper
from app.models.email_model import EmailListResponse


router = APIRouter()


@router.get("/all-emails", response_model=EmailListResponse)
async def get_all_unique_emails_last_180_days(since_days: int, token: str = Depends(google_helper.get_access_token)):
    gmail_service = await google_helper.get_gmail_service(token)
    if gmail_service is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or Unauthorized user token")

    # Calculate the date number of days as per query
    date_since_days_ago = (datetime.now(timezone.utc) - timedelta(days=since_days)).strftime('%Y-%m-%d')

    # Get emails received in the last 180 days
    messages = gmail_service.users().messages().list(userId='me', q=f'after:{date_since_days_ago}').execute()

    # Initialize dictionary to store emails and their corresponding messages
    email_messages: dict[Any, Any] = dict()

    # Extract email IDs and messages
    for message in messages.get('messages', []):
        email = gmail_service.users().messages().get(userId='me', id=message['id']).execute()
        headers = email['payload']['headers']
        from_email = None
        for header in headers:
            if header['name'] == 'From':
                from_email = header['value']
                break
        if from_email:
            if from_email in email_messages:
                email_messages[from_email].append(email)
            else:
                email_messages[from_email] = [email]

    return EmailListResponse(
        count=len(email_messages),
        emails=email_messages
    )
