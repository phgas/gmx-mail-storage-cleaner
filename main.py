import os
import requests
from dotenv import load_dotenv
import json


def read_env():
    load_dotenv(
        override=True  # Important: Otherwise it will not read from .env-file but from user-env
    )
    global BEARER_TOKEN_TO_RETRIEVE
    global BEARER_TOKEN_TO_DELETE
    BEARER_TOKEN_TO_RETRIEVE = os.environ.get("BEARER_TOKEN_TO_RETRIEVE")
    BEARER_TOKEN_TO_DELETE = os.environ.get("BEARER_TOKEN_TO_DELETE")


def get_amountOfUsedMessages(folderType: str):
    url = "https://webmail-cats-live.gmx.net/mailbox/primary/folders?absoluteURI=false&no_cache=25e803ab-298f-8551-1563-0bbfa8c22741"
    headers = {"Authorization": BEARER_TOKEN_TO_RETRIEVE}
    response = requests.get(url, headers=headers)
    for folder in response.json()["folders"]:
        if folder["attribute"]["folderType"] == folderType:
            amountOfusedMessages = folder["quota"]["totalMessages"]
            return amountOfusedMessages


def get_mailUris(amountOfMails: int, folderType: str, offset: int = 0):
    # If offset is not working properly, just run the script twice
    url = f"https://maillist.gmx.net/Mailbox/Mail?no_cache=a8d8e12c-09c2-6167-3246-e5e390fc908b&folderTypeOrId={folderType}&offset={offset}&amount={amountOfMails}&orderBy=DATE+DESC"
    headers = {"Authorization": BEARER_TOKEN_TO_RETRIEVE}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        mailUris = [
            f'/{mail["rawData"]["mailURI"]}'
            for mail in response.json()["mailListElements"]
        ]
        print(f"[{folderType}] Got {len(mailUris)} mailListElements.")
    elif response.status_code == 500:
        print(
            f"[{folderType}] Can't get {amountOfMails} mailListElements in one go, splitting up in two parts..."
        )
        first_half = amountOfMails // 2
        second_half = amountOfMails - first_half
        mailUris_first_half = get_mailUris(first_half, folderType)
        mailUris_second_half = get_mailUris(second_half, folderType, offset=first_half)
        mailUris = mailUris_first_half + mailUris_second_half
    return mailUris


def delete_mails(mailUris: list) -> bool:
    url = "https://webmail-cats-live.gmx.net/mailbox/primary/MailBatchDelete?absoluteURI=false&no_cache=a8d8e12c-09c2-6167-3246-e5e390fc908b"
    body = json.dumps(
        {
            "moveToTrash": "false",
            "mailUris": mailUris,
        }
    )
    headers = {
        "Authorization": BEARER_TOKEN_TO_DELETE,
        "Content-Type": "application/vnd.ui.trinity.message.batchdelete+json",
    }
    response = requests.post(url, headers=headers, data=body)
    if response.status_code == 204:
        return True


def delete_allMailsFromFolder(folderType: str) -> None:
    read_env()
    amountOfUsedMessages = get_amountOfUsedMessages(folderType)
    print(f"[{folderType}] There are {amountOfUsedMessages} Mails to delete.")
    if amountOfUsedMessages == 0:
        return
    trashMailUris = get_mailUris(amountOfUsedMessages, folderType)
    isDeleted = delete_mails(trashMailUris)
    if isDeleted:
        print(f"[{folderType}] Successfully deleted {len(trashMailUris)} Mails.")


if __name__ == "__main__":
    delete_allMailsFromFolder(folderType="INBOX")
    delete_allMailsFromFolder(folderType="TRASH")
