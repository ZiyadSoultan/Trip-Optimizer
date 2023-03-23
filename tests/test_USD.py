from src.USD import update_USD

def test_USD():
    update_USD()
    with open("src/USD.txt", 'r') as file:
        USD = float(file.read())
    assert type(USD) == float
    assert USD > 0