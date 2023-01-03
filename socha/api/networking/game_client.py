"""
This module handels the communication with the api and the students logic.
"""
import logging
import sys
import time
from typing import List, Union

from socha.api.networking.xmlprotocolinterface import XMLProtocolInterface
from socha.api.plugin import penguins
from socha.api.plugin.penguins import Field, GameState, Move, CartesianCoordinate
from socha.api.protocol.protocol import State, Board, Data, \
    Error, From, Join, Joined, JoinPrepared, JoinRoom, To, Team, Room, Result, MoveRequest, ObservableRoomMessage, Left
from socha.api.protocol.protocol_packet import ProtocolPacket


def _convertBoard(protocolBoard: Board) -> penguins.Board:
    """
    Converts a protocol Board to a usable game board for using in the logic.
    :rtype: object
    """
    boardList = [
        [Field(CartesianCoordinate(x, y).to_hex(), fieldsValue) for x, fieldsValue in enumerate(row.field_value)]
        for y, row in enumerate(protocolBoard.list_value)]
    return penguins.Board(boardList)


class AbstractGameClient:
    history: List[Union[GameState, Error, Result]] = []

    def calculate_move(self) -> Move:
        """
        Calculates a move that the logic wants the server to perform in the game room.
        """

    def on_update(self, state: GameState):
        """
        If the server _send a update on the current state of the game this method is called.
        :param state: The current state that server sent.
        """

    def on_game_over(self, roomMessage: Result):
        """
        If the game has ended the server will _send a result message.
        This method will called if this happens.

        :param roomMessage: The Result the server has sent.
        """

    def on_error(self, logMessage: str):
        """
        If error occurs,
        for instance when the logic sent a move that is not rule conform,
        the server will _send an error message and closes the connection.
        If this happens, this method is called.

        :param logMessage: The message, that server sent.
        """

    def on_room_message(self, data):
        """
        If the server sends a message that cannot be handelt by anny other method,
        this will be called.

        :param data: The data the Server sent.
        """

    def on_game_prepared(self, message):
        """
        If the game has been prepared by the server this method will be called.

        :param message: The message that server sends with the response.
        """

    def on_game_joined(self, room_id):
        """
        If the client has successfully joined a game room this method will be called.

        :param room_id: The room id the client has joined.
        """

    def on_game_observed(self, message):
        """
        If the client successfully joined as observer this method will be called.

        :param message: The message that server sends with the response.
        """

    def on_game_left(self):
        """
        If the server left the room, this method will be called.
        If the client is running on survive mode it'll be running until shut downed manually.
        """

    def while_disconnected(self, player_client: 'GameClient'):
        """
        The client loop will keep calling this method while there is no active connection to a game server.
        This can be used to do tasks after a game is finished and the server left.
        Please be aware, that the client has to be shut down manually if it is in survive mode.
        The return statement is used to tell the client whether to exit or not.

        :type player_client: The player client in which the logic is integrated.
        :return: True if the client should shut down. False if the client should continue to run.
        """


class GameClient(XMLProtocolInterface):
    """
    The PlayerClient handles all incoming and outgoing objects accordingly to their types.
    """

    def __init__(self, host: str, port: int, handler: AbstractGameClient, survive: bool):
        super().__init__(host, port)
        self._game_handler = handler
        self.survive = survive

    def join_game(self):
        self._send(Join())

    def join_game_room(self, room_id: str):
        self._send(JoinRoom(room_id=room_id))

    def join_game_with_reservation(self, reservation: str):
        self._send(JoinPrepared(reservation_code=reservation))

    def send_message_to_room(self, room_id: str, message):
        self._send(Room(room_id=room_id, data=message))

    def _on_object(self, message):
        # Extract room ID from the message
        room_id = message.room_id

        # Check if the message is a Joined object
        if isinstance(message, Joined):
            self._game_handler.on_game_joined(room_id=room_id)

        # Check if the message is a Left object
        elif isinstance(message, Left):
            self._game_handler.on_game_left()

        # Check if the data is a MoveRequest
        elif isinstance(message.data.class_binding, MoveRequest):
            # Calculate the move and log the time it took
            start_time = time.time()
            move_response = self._game_handler.calculate_move()
            logging.info(f"Sent {move_response} after {time.time() - start_time} seconds.")
            # If a move was found, create a Data object with the move information and send it to the room
            if move_response:
                from_pos = None
                to_pos = To(x=move_response.to_value.x, y=move_response.to_value.y)
                if move_response.from_value:
                    from_pos = From(x=move_response.from_value.x, y=move_response.from_value.y)
                response = Data(class_value="move", from_value=from_pos, to=to_pos)
                self.send_message_to_room(room_id, response)

        # Check if the data is an ObservableRoomMessage
        elif isinstance(message.data.class_binding, ObservableRoomMessage):
            # Check if the data is a State object
            if isinstance(message.data.class_binding, State):
                # Convert the board data and create a GameState object
                game_state = GameState(
                    turn=message.data.class_binding.turn,
                    start_team=Team(message.data.class_binding.start_team, [], 0),
                    board=_convertBoard(message.data.class_binding.board),
                    last_move=message.data.class_binding.last_move,
                    fishes=penguins.Fishes(message.data.class_binding.fishes.int_value[0],
                                           message.data.class_binding.fishes.int_value[1]),
                )
                # Add the game state to the history and call the on_update handler
                self._game_handler.history.append(game_state)
                self._game_handler.on_update(game_state)
            # Check if the data is a Result object
            elif isinstance(message.data.class_binding, Result):
                # Add the result to the history and call the on_game_over handler
                self._game_handler.history.append(message.data.class_binding)
                self._game_handler.on_game_over(message.data.class_binding)

            # Check if the message is a Room object
            elif isinstance(message, Room):
                self._game_handler.on_room_message(message.data.class_binding)

    def start(self):
        """
        Starts the client loop.
        """
        self._running = True
        self._client_loop()

    def _handle_left(self):
        if not self.survive:
            logging.info("The server left.")
            self.stop()
        else:
            logging.info("The server left. Client is in survive mode and keeps running.\n"
                         "Please shutdown the client manually.")
            self.disconnect()

    def _handle_other(self, response):
        logging.debug(f"Received new object: {response}")
        self._on_object(response)

    def _client_loop(self):
        """
        The client loop is the main loop, where the client waits for messages from the server
        and handles them accordingly.
        """

        while self._running:
            if self._network_interface.connected:
                response = self._receive()
                if not response:
                    continue
                elif isinstance(response, ProtocolPacket):
                    if isinstance(response, Left):
                        self._handle_left()
                    else:
                        self._handle_other(response)
                elif self._running:
                    logging.error(f"Received object of unknown class: {response}")
                    raise NotImplementedError("Received object of unknown class.")
            else:
                self._game_handler.while_disconnected(player_client=self)

        logging.info("Done.")

    def stop(self):
        """
        Disconnects from the server and stops the client loop.
        """
        logging.info("Shutting down...")
        if self._network_interface.connected:
            self.disconnect()
        self._running = False
