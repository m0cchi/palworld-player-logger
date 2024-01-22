from mcrcon import MCRcon

import os
import io
import time
import csv
import json
import logging


logging.basicConfig(level=logging.INFO)


def fetch_login_players(mcr):
    players = []
    for _ in range(3):
        try:
            response = mcr.command("ShowPlayers")
            reader = csv.reader(io.StringIO(response))
            next(reader)  # skip header
            for row in reader:
                players.append(
                    {
                        "name": row[0],
                        "playeruid": row[1],
                        "steamid": row[2],
                    }
                )
            break
        except:
            mcr.connect()
    # filter loading players
    return [p for p in players if p['playeruid'] != '00000000']


def diff_players(new_players, old_payers):
    new_ids = {p["steamid"]: p for p in new_players}
    old_ids = {p["steamid"]: p for p in old_players}

    login_players = []
    logout_players = []

    for nid in new_ids:
        if nid not in old_ids:
            login_players.append(new_ids[nid])

    for oid in old_ids:
        if oid not in new_ids:
            logout_players.append(old_ids[oid])

    return (len(login_players) + len(logout_players)) > 0, login_players, logout_players


if __name__ == "__main__":
    rcon_address = os.environ.get("RCON_ADDRESS", "127.0.0.1")
    rcon_port = int(os.environ.get("RCON_PORT", "25575"))
    rcon_password = os.environ["RCON_PASSWORD"]

    time_window = int(os.environ.get("TIME_WINDOW", "15"))

    with MCRcon(rcon_address, rcon_password, rcon_port) as mcr:
        old_players = []
        while True:
            players = fetch_login_players(mcr)
            changed, login_players, logout_players = diff_players(players, old_players)
            if changed:
                logging.info(
                    json.dumps(
                        {
                            "message": "diff",
                            "login_players": login_players,
                            "logout_players": logout_players,
                        }
                    )
                )

            old_players = players
            time.sleep(time_window)
