from typing import Any, List

from fastapi import APIRouter, Depends, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.api import deps
from app.core.celery_app import celery_app
from app.socket_models import ConnectionManager
from app.utils import send_test_email, find_in_list

router = APIRouter()


@router.post("/test-celery/", response_model=schemas.Msg, status_code=201)
def test_celery(
    msg: schemas.Msg,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test Celery worker.
    """
    celery_app.send_task("app.worker.test_celery", args=[msg.msg])
    return {"msg": "Word received"}


@router.post("/test-email/", response_model=schemas.Msg, status_code=201)
def test_email(
    email_to: EmailStr,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Test emails.
    """
    send_test_email(email_to=email_to)
    return {"msg": "Test email sent"}

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var list = ['enricfranck@gmail.com', 'test@gmail.com', 'admin@science.com'] 
            var client_id = list[Math.floor(Math.random()*list.length)];
            var ws = new WebSocket(`ws://localhost/api/v1/utils/ws/${client_id}?client_received=enricfranck@gmail.com`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
list_msg = ["test", "one", "two"]

manager = ConnectionManager()

def get_list_user(db: Session = Depends(deps.get_db),*, client_id: str='') -> List[str]:
    list_received = []
    user = crud.user.get_by_email(db=db, email=client_id)
    if user:
        all_users = crud.user.get_multi(db=db, order_by='email')
        for on_user in all_users:
            if user.uuid_mention and on_user.email != user.email:
                for uuid_mention in user.uuid_mention:
                    if (find_in_list(on_user.uuid_mention, uuid_mention) != -1 and on_user.is_admin) or \
                            (on_user.is_superuser and find_in_list(list_received, on_user.email) == -1):
                        list_received.append(on_user.email)
    return list_received

@router.get("/")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str,
    db: Session = Depends(deps.get_db),):
    client= schemas.SocketModel(**{'id':client_id, 'wb':websocket})
    invitation = crud.invitation.get_by_email(db=db, email=client_id)
    await manager.connect(client, jsonable_encoder(invitation))
    try:
        while True:
            data = await client.wb.receive_json()
            if data != '':
                user = crud.user.get_by_email(db=db, email=client_id)
                if user.is_superuser or user.is_admin:
                    users = [data['to']]
                    print(users)
                else:
                    users = get_list_user(db=db, client_id=client_id)
                for on_client in users:
                    invitations = schemas.InvitationCreate(**{'email': on_client, 'message': data['message'], 'email_from':client_id})
                    invitation = crud.invitation.create(db=db, obj_in=invitations)
                    await manager.broadcast_id(jsonable_encoder(invitation), on_client)
           # await manager.send_personal_message(f"You wrote: {data} {len(user)}", client.wb)
    except Exception as e:
        manager.disconnect(client)
        #await manager.broadcast_all(f"Client #{client_id} left the chat")