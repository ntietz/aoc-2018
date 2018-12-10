
@profile
def play(num_players: int, last_marble: int) -> None:
    marbles = [0]
    scores: Dict[int, int] = {}
    for player in range(0, num_players):
        scores[player] = 0
    player = 0
    current = 0
    for marble in range(1, last_marble+1):
        if marble % 23 == 0:
            idx = (current - 7) % len(marbles)
            scores[player] += marble + marbles[idx]
            marbles = marbles[:idx] + marbles[idx+1:]
            current = idx
        else:
            idx = (current + 1) % len(marbles)
            marbles = marbles[:idx+1] + [marble] + marbles[idx+1:]
            current = (idx + 1) % len(marbles)
        player = (player + 1) % num_players
    print(max(scores.values()))


if __name__ == '__main__':
    play(9, 25)
    play(10, 161)
    play(13, 7999)
    play(17, 1104)
    play(21, 6111)
    play(30, 5807)
    #play(403, 71920)
    #play(403, 7192000)

