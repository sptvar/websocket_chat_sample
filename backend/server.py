import asyncio
import websockets
from typing import Set

# Используем новый тип WebSocketServerProtocol
clients: Set[websockets.WebSocketServer] = set()

async def handler(websocket: websockets.WebSocketServer):
    clients.add(websocket)
    print(f"Новое подключение. Всего клиентов: {len(clients)}")
    
    try:
        async for message in websocket:
            print(f"Получено: {message}")
            # Рассылаем сообщение всем клиентам
            await asyncio.gather(
                *[client.send(f"Сообщение: {message}") for client in clients],
                return_exceptions=True
            )
    except websockets.exceptions.ConnectionClosed:
        print("Клиент отключился")
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        await asyncio.Future()  # Бесконечное выполнение

if __name__ == "__main__":
    asyncio.run(main())
